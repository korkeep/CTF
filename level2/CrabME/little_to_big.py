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