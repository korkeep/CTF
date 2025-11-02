## Exercise: SSH

> 문제 URL: https://dreamhack.io/wargame/challenges/875  
> SSH 실습을 위한 문제입니다. 문제 서버에 SSH로 접속하세요!

### Solve

1. 문제에서 주어진 접속정보를 활용해 호스트에 `ssh`를 통해 접속

```bash
┌──(root💀kali)-[~/dreamhack]
└─# ssh chall@host1.dreamhack.games -p 17508                                                                     1 ⨯ 1 ⚙

The authenticity of host '[host1.dreamhack.games]:17508 ([139.99.121.66]:17508)' can't be established.
ECDSA key fingerprint is SHA256:2d9VnfCvgLWDQYj9RxnmsXtv5AlQvyMhvuWDebFbuIs.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[host1.dreamhack.games]:17508,[139.99.121.66]:17508' (ECDSA) to the list of known hosts.
chall@host1.dreamhack.games's password:
```

```bash
chall@localhost:~$ ll
total 36
drwxr-x--- 1 chall chall    4096 Feb 26 03:00 ./
drwxr-xr-x 1 root  root     4096 Apr  4  2023 ../
-rw-r--r-- 1 chall chall     220 Apr  4  2023 .bash_logout
-rw-r--r-- 1 chall chall    3771 Apr  4  2023 .bashrc
drwx------ 2 chall chall    4096 Feb 26 03:00 .cache/
-rw-r--r-- 1 chall chall     851 Apr  4  2023 .profile
drwxr-xr-x 2 root  root     4096 Apr  4  2023 bin/
-rwxr-xr-x 1 root  beginner   21 Apr  4  2023 flag*
```

2. `cat` 명령을 활용해 `flag` 획득

```bash
chall@localhost:~$ cat flag
DH{h3110_6e9inn3rs!}
```
