### Absolute DES

1. prob.py 주요부분 분석

```python
# Flag를 읽어오고
with open("flag", "rb") as f:
    flag = f.read()

# 8Byte Key를 생성함 (DES ECB 모드)
key = os.urandom(8)
cipher = DES.new(key, DES.MODE_ECB)

while True:
    menu()
    action = int(input())

    # Encrypt 부분
    if action == 1:
        msg = bytes.fromhex(input("send your message(hex) > "))
        print(f"encrypted message > {cipher.encrypt(pad(msg, 16)).hex()}")

    # Decrypt 부분
    elif action == 2:
        print("My key is not for sell. I'll give you some dummies instead :>")

        # space를 기준으로 8개 숫자(0 < d < 256) dummy를 입력
        dummy = list(map(int, input().split()))
        assert len(dummy) == 8, "Invalid input!"
        for d in dummy:
            assert 0 < d < 256, "Invalid input!"
        key_dummy = bytes([d ^ k for d, k in zip(dummy, key)])
        cipher_dummy = DES.new(key_dummy, DES.MODE_ECB)

        msg = bytes.fromhex(input("send your message(hex) > "))
        print(f"encrypted message > {cipher_dummy.decrypt(pad(msg, 16)).hex()}")

    # flag를 Encrypt 하는 부분
    elif action == 3:
        print(f"Encrypted flag > {cipher.encrypt(pad(flag, 16)).hex()}")
```

2. flag를 Encrypt 하는 부분 결과

```bash
1. Encrypt message
2. Decrypt message
3. Encrypt flag
4. Exit
> 3
Encrypted flag > 4f910e1b92ce7d7c5f209bb7431c1ef7db11fb6783be9b29524a836c7abf9e3292065f86292eec32fa18a8c29ed288d6
```

3. 2에서 구한 hex를 이용해서, Decrypt 시도

```bash
1. Encrypt message
2. Decrypt message
3. Encrypt flag
4. Exit
> 2
My key is not for sell. I'll give you some dummies instead :>
1 1 1 1 1 1 1 1
send your message(hex) > 4f910e1b92ce7d7c5f209bb7431c1ef7db11fb6783be9b29524a836c7abf9e3292065f86292eec32fa18a8c29ed288d6
decrypted message > 44487b626333643535386236313734653764313a313275427a617a4c4b4b736559526657474d495765673d3d7d0a02028ff582e06d45a9e48ff582e06d45a9e4
```

- 이때, 1을 space 단위로 8개 한 값은 key를 0x01로 xor한 결과임
- 근데 문제에서 1byte(8-bit)가 아닌 7-bit로 DES를 돌린다고 하니까 1로 xor 한 값은 영향을 주지 않음!
- 그래서 **44487b626333643535386236313734653764313a313275427a617a4c4b4b736559526657474d495765673d3d7d0a02028ff582e06d45a9e48ff582e06d45a9e4**를 그대로 hex decode 하면 플래그 획득 가능
