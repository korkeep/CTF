## Exercise: Docker

> 문제 URL: https://dreamhack.io/wargame/challenges/876  
> Docker 실습을 위한 문제입니다. 주어진 Dockerfile을 빌드하여 이미지를 생성하고 컨테이너를 실행해 보세요!

### Solve

1. `docker build` 명령어를 통해 docker 파일 빌드

```bash
ubuntu@ubuntu:~/dreamhack/876$ sudo docker build -t 876 .
```

2. 빌드된 docker 이미지 확인

```bash
ubuntu@ubuntu:~/dreamhack/876$ sudo docker images
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
876          latest    9b85c96bc742   13 seconds ago   139MB
ubuntu       22.04     a24be041d957   4 weeks ago      77.9MB
```

3. 실행중인 컨테이너 확인

```bash
ubuntu@ubuntu:~/dreamhack/876$ sudo docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS      NAMES
fbea6f5debc9   876       "/bin/sh -c 'socat -…"   46 seconds ago   Up 44 seconds   2222/tcp   876
```

4. 실행중인 컨테이너에 접속

```bash
ubuntu@ubuntu:~/dreamhack/876$ sudo docker exec -it 876 bash
chall@fbea6f5debc9:~$ ll
total 40
drwxr-x--- 1 root chall  4096 Feb 27 12:32 ./
drwxr-xr-x 1 root root   4096 Feb 27 12:32 ../
-rw-r--r-- 1 root chall   220 Feb 27 12:32 .bash_logout
-rw-r--r-- 1 root chall  3771 Feb 27 12:32 .bashrc
-rw-r--r-- 1 root chall   807 Feb 27 12:32 .profile
-rwxr-xr-x 1 root chall 15960 Mar 31  2023 chall*
-r--r----- 1 root chall    19 Mar 31  2023 flag
chall@fbea6f5debc9:~$ cat flag
DH{docker_exercise}
```

5. 컨테이너 종료, 컨테이너 삭제, 이미지 삭제

```bash
ubuntu@ubuntu:~/dreamhack/876$ sudo docker stop 876
876
ubuntu@ubuntu:~/dreamhack/876$ sudo docker rm 876
876
ubuntu@ubuntu:~/dreamhack/876$ sudo docker rmi 876
Untagged: 876:latest
Deleted: sha256:9b85c96bc742c10ed15c32e996d36e7b0875fdc398eb97295104f269afe9af3d
Deleted: sha256:1067e7378dfddf6b9976651f37e69624496c8eef895831cd620e08dbc147aa4f
Deleted: sha256:2e54ed4ad2c588ac17e3dd3911bbff6cd6b1aad73aa4792c175a77acae9889c3
Deleted: sha256:8cb5eb2a88fc2533a90a6e0db005604c600ba7d41ced3772a4e7dd8df28a00bc
Deleted: sha256:699e9dc90da5cd2344d8df8a172a028e09925b97d505f663716aef1095d67dbc
Deleted: sha256:789144fbee538b18776145fa4e2c22f7b6cd18f3d3d38ccefdb8b476362272b2
Deleted: sha256:4396323f94378b9b7ab7f0ca50cbdac30e86ddad1927f2146ca8019a67c9d277
Deleted: sha256:c47b0b32083a09bc1cacdb39384a15d270a52a39398ef742ab1ff7d93c519076
Deleted: sha256:a35195b9c4f721c21dc9b0423cd77d1a2f7a17bc6bfd9139ab7329bdf5d4a075
Deleted: sha256:32d48eb5664e2d2847017f1911228d1842313aab04aaad06e9a93dc9d9018519
Deleted: sha256:7f0f219491231d3241a240a538b2d7fef9600d8c47957dd09df6d1a04c1ccd69
Deleted: sha256:4a3c2ccb6d3cee580b1e3e709568d2c834a80652c7d43e89410fb6166899f0e3
Deleted: sha256:89baf15575563b9727cb56fec19ddd2e3eb34baf7596a55830da72190366384d
Deleted: sha256:26c63cabfc8b5b3fba288d530a55d4025de58131bc6dce9fbfba92e3f1e8aae9
Deleted: sha256:07ff9a2e18ec6f421071d758b8c633894732d8f0ec31aabd1e0a9b42c3747064
Deleted: sha256:9fdd4758e27de30560897235b1d21324db7c73f57beaba8ae3a8fb11e3101bdd
Deleted: sha256:8ab50184ca5781ff8cf01b83bbcb63b6dd981cd8d08e3b971c063bffcd2dcab2
Deleted: sha256:c6bafb5ffd18194821c746c343f2a86c16efc16cd270bf529da082b23b2279d9
Deleted: sha256:ee80d211fcd981827298104c0dcd1c9acfb11c817dbcaef97b173459d31bfe8a
Deleted: sha256:ee35d75c7f2321844035ba2160593a2520ed8f461ff399d78aa5d46ce5f31633
Deleted: sha256:2f69604365942bfb4f7cf046e82d16cde69c9e3fcadc890b754bf1eb00a3b869
Deleted: sha256:43e30a86200335176e8cd4bbe45c35aa35f3512732291a06d515daef758b40b2
Deleted: sha256:f176ed65ef08b5a70d7e29e8b7882f5b0145aeba41319ce9b8b4c5061d93bbb6
Deleted: sha256:fa83c8b48ce671883a3925c05f6ab9602feaebefc961cf552eac20691a8e9ca4
Deleted: sha256:836a4780fb9fd0d4fc877239e63a30fcd4592e8786b3b95a906f376d54824872
Deleted: sha256:81a478641569d75ac90a5aa748af807ad17fadc76adf1b2a4ac6839cc28dcfa0
```
