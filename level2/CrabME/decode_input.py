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
