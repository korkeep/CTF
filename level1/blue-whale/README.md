## blue-whale

> 문제 URL: https://dreamhack.io/wargame/challenges/853  
> Docker의 Dive 기능을 이용해서 이미지를 분석하여 플래그를 획득하세요.

### Solve

1. `snap`으로 `Dive`설치

```bash
ubuntu@ubuntu:~/dreamhack/853$ snap install dive
```

2. `Docker` 이미지 빌드

```bash
ubuntu@ubuntu:~/dreamhack/853$ sudo docker pull dreamhackofficial/blue-whale
```

3. `Dive`로 이미지 분석

```bash
ubuntu@ubuntu:~/dreamhack/853$ dive dreamhackofficial/blue-whale:1
```

4. 플래그 획득

```bash
DH{b06cb27a502a831822f927562258c6f69b5996a9916206cdb8755cc90ebf3b9f}
```

5. 이미지 삭제

```bash
ubuntu@ubuntu:~/dreamhack/853$ sudo docker rmi dreamhackofficial/blue-whale:1
```
