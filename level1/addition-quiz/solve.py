from pwn import *

conn = remote('host1.dreamhack.games', 12322)

for _ in range(50):
    question = conn.recvline().decode().strip()
    num_str, _ = question.split('=')
    num1, num2 = map(int, num_str.split('+'))
    conn.sendline(str(num1 + num2))

#결과를 출력
print(conn.recvall().decode())