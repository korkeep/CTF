### CrabME

1. Docker 또는 chroot로 환경 맞추기

```bash
# Docker 설치되어 있다고 가정
# --rm: 컨테이너가 종료되면 자동 삭제
# -it: 인터랙티브 모드, 터미널 할당 (셸 환경 제공)
# -v $(pwd):/chal: 호스트($(pwd))와 컨테이너(:/chal)를 바인드
# ubuntu:22.04: 사용하려는 도커 이미지
docker run --rm -it -v $(pwd):/chal ubuntu:22.04

# 컨테이너 안에서 필요한 도구 설치
apt update
apt install -y build-essential gdb ltrace strace patchelf

# 실행
cd /chal
./chal
```

2. main 함수 흐름 분석

```c
std::io::stdio::_print(...) // 사용자에게 입력을 요청하는 메시지를 출력

std::io::stdio::stdin::read_line(...) // 표준 입력으로 문자열(플래그)을 입력받음

core::str::_$LT$impl$u20$str$GT$::trim_matches(...) // 개행 문자 제거 등 트리밍

if (v3 != 64) goto fail; // 입력 문자열 길이가 정확히 64 바이트인지 확인

while (v5 != 64) { UTF-8 디코딩, if (문자가 숫자(0~9) 또는 a~f가 아니면 fail) } // 플래그 문자열이 hex 문자 (0-9, a-f)만 포함하고 있는지 확인

chal::hex_to_u32_vec::hc1b549ac35b36e7d(&v16, v4); // 64 hex characters → 32 bytes → 32 / 4 = 8개의 u32 값으로 변환하는 함수, 예: "deadbeef" → [0xdeadbeef]

if (__OFSUB__(0LL, v16)) goto fail; // 변환 결과가 없거나 문제가 있으면 종료

if (!chal::flagchecker::hcd4f696ca0582a82(&v16)) goto fail; // 가장 핵심. 변환된 u32[] 배열을 바탕으로 검증하는 로직

chal::success::h815dd63f4db175f9(v4); // 성공 시 메시지 출력
```

3. hcd4f696ca0582a82 함수 실행 흐름 분석

```c
if (a1[2] != 32) chal::fail::h17a611a0a5b7ce46(); // **32개의 u32 (== 4바이트 정수)**가 있어야 통과

(((((8 * v5 & 8 | (v5 >> 1) & 1) + 4 * (v5 & 4)) | (v5 >> 2) & 2 | 8 * v5 & 0x80)
+ 2 * (v5 & 0x20)) | (v5 >> 4) & 4 | (v5 >> 2) & 0x20) ^ 0x63) + 34 // v5의 각 비트들에 대해 마스킹, 쉬프팅, AND/OR 연산, 마지막에 ^ 0x63 하고 + 34
```

4. IDA Pro에서 메모리 덤프 (Python 입력 사용)

```python
import ida_bytes
import binascii

start = 0x49000
size = 128
data = ida_bytes.get_bytes(start, size)

# 안전하게 hex 출력
if data:
    print(binascii.hexlify(data))
else:
    print("Failed to read memory at 0x49000")
```

```bash
Python>
ae0000006d0000009b00000092000000130000002b000000c6000000c9000000e5000000fa000000960000000b0000006400000031000000b800000008000000c800000048000000d2000000300000006000000004000000fa0000007b00000088000000b00000002f0000007c000000b3000000b30000005800000061000000
```

5. 빅엔디언으로 결과 변환 (little_to_big.py)

```python
import binascii

# IDA에서 읽은 덤프 데이터 (바이너리 or hex string)
hex_data = "ae0000006d0000009b00000092000000130000002b000000c6000000c9000000e5000000fa000000960000000b0000006400000031000000b800000008000000c800000048000000d2000000300000006000000004000000fa0000007b00000088000000b00000002f0000007c000000b3000000b30000005800000061000000"

data = bytes.fromhex(hex_data)
expected_bytes = []

for i in range(0, len(data), 4):
    chunk = data[i:i+4]
    val = int.from_bytes(chunk, byteorder='little')
    expected_bytes.append(val & 0xFF)  # 하위 1바이트만 사용

# 출력
print("expected_bytes = [")
for i in range(0, len(expected_bytes), 8):
    print("    " + ', '.join(f"0x{b:02X}" for b in expected_bytes[i:i+8]) + ',')
print("]")
```

```bash
expected_bytes = [
    0xAE, 0x6D, 0x9B, 0x92, 0x13, 0x2B, 0xC6, 0xC9,
    0xE5, 0xFA, 0x96, 0x0B, 0x64, 0x31, 0xB8, 0x08,
    0xC8, 0x48, 0xD2, 0x30, 0x60, 0x04, 0xFA, 0x7B,
    0x88, 0xB0, 0x2F, 0x7C, 0xB3, 0xB3, 0x58, 0x61,
]
```

6. 디코드 스크립트 실행 (little_to_big.py)

```python
# 주어진 expected 값 리스트 (xmmword 각 4바이트의 하위 바이트로 채움)
expected_bytes = [
    0xAE, 0x6D, 0x9B, 0x92, 0x13, 0x2B, 0xC6, 0xC9,
    0xE5, 0xFA, 0x96, 0x0B, 0x64, 0x31, 0xB8, 0x08,
    0xC8, 0x48, 0xD2, 0x30, 0x60, 0x04, 0xFA, 0x7B,
    0x88, 0xB0, 0x2F, 0x7C, 0xB3, 0xB3, 0x58, 0x61,
]

def check_v5(v5, expected):
    # 주어진 C 코드 비트 연산을 Python으로 표현
    part = (
        (
            (
                ((8 * v5) & 8) | ((v5 >> 1) & 1)
            ) + 4 * (v5 & 4)
        ) | (((v5 >> 2) & 2) | ((8 * v5) & 0x80))
    ) + 2 * (v5 & 0x20)
    part = part | ((v5 >> 4) & 4) | ((v5 >> 2) & 0x20)
    actual = ((part ^ 0x63) + 34) & 0xFF  # 8비트 마스크
    return actual == expected

flag_bytes = []

for expected in expected_bytes:
    found = False
    for v5 in range(256):  # v5를 8비트 값으로 가정, 0~255 전수 탐색
        if check_v5(v5, expected):
            flag_bytes.append(v5)
            found = True
            break
    if not found:
        print(f"해당 expected 값 {expected:#02x} 에 맞는 v5를 찾지 못했습니다!")
        flag_bytes.append(0)

print("Recovered flag bytes (hex):", ''.join(f'{b:02x}' for b in flag_bytes))
print("Recovered flag ASCII:", ''.join(chr(b) if 32 <= b < 127 else '.' for b in flag_bytes))

```
