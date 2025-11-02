#!/usr/bin/env python3
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
import os


def menu():
    print("1. Encrypt message")
    print("2. Decrypt message")
    print("3. Encrypt flag")
    print("4. Exit")
    print("> ", end="")


if __name__ == "__main__":
    with open("flag", "rb") as f:
        flag = f.read()

    key = os.urandom(8)

    print("DES uses 56bit-length private key. But wait, isn't that 8 byte?")
    cipher = DES.new(key, DES.MODE_ECB)
    while True:
        menu()
        action = int(input())
        if action == 1:
            msg = bytes.fromhex(input("send your message(hex) > "))
            print(f"encrypted message > {cipher.encrypt(pad(msg, 16)).hex()}")

        elif action == 2:
            print("My key is not for sell. I'll give you some dummies instead :>")
            dummy = list(map(int, input().split()))
            assert len(dummy) == 8, "Invalid input!"
            for d in dummy:
                assert 0 < d < 256, "Invalid input!"
            key_dummy = bytes([d ^ k for d, k in zip(dummy, key)])
            cipher_dummy = DES.new(key_dummy, DES.MODE_ECB)
            msg = bytes.fromhex(input("send your message(hex) > "))
            print(f"encrypted message > {cipher_dummy.decrypt(pad(msg, 16)).hex()}")

        elif action == 3:
            print(f"Encrypted flag > {cipher.encrypt(pad(flag, 16)).hex()}")

        elif action == 4:
            print("Good Bye!")
            break

        else:
            print("invalid")