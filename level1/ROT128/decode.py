hex_list = [(hex(i)[2:].zfill(2).upper()) for i in range(256)]

# 암호화된 문자열을 읽음
with open('encfile', 'r', encoding='utf-8') as f:
    enc_data = f.read()

# 2자리씩 잘라서 리스트로 나눔 (ex: ['80', '12', 'FF', ...])
enc_list = [enc_data[i:i+2] for i in range(0, len(enc_data), 2)]

# 복호화 리스트
plain_list = []

for hex_b in enc_list:
    index = hex_list.index(hex_b)
    dec_index = (index - 128) % len(hex_list)
    plain_list.append(hex_list[dec_index])

# 16진 문자열을 바이트로 변환
plain_bytes = bytes([int(h, 16) for h in plain_list])

# 복호화된 내용을 저장
with open('decode.png', 'wb') as f:
    f.write(plain_bytes)