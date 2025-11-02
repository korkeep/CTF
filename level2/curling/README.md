### curling

1. `POST /api/v1/test/curl`

- 전달받은 url을 curl 명령어로 실행
- url이 http://dreamhack.io 또는 http://tools.dreamhack.io로 시작하지 않으면 차단
- url이 /test/internal로 끝나면 차단

2. `/api/v1/test/internal`

- 로컬 IP(127.0.0.1)에서만 접근 가능
- 접근 시 FLAG 반환

3. 아이디어

- 로컬에서 접속한 것처럼 보이게 하여 /api/v1/test/internal에 접근, 플래그를 얻기
- curl 명령어는 서버에서 실행됨 ⇒ 서버는 자기 자신(127.0.0.1)에 접근 가능

4. 명령어

```bash
curl -X POST http://host8.dreamhack.games:12879/api/v1/test/curl \
     -d 'url=http://dreamhack.io@127.0.0.1:8000/api/v1/test/internal?'
```

- `dreamhack.io@127.0.0.1`: dreamhack.io는 유저정보, 실제로는 127.0.0.1에 요청이 감
- 포트: `8000` (서버가 이 포트로 작동 중)
- 경로: `/api/v1/test/internal?` ← 끝에 ?를 붙여서 `endswith('/test/internal')` 조건을 우회함

5. 동작 요약

- Dreamhack 서버는 /api/v1/test/curl로 POST 요청을 받음
- 우리가 준 url을 이용해 내부적으로 curl http://dreamhack.io@127.0.0.1:8000/api/v1/test/internal/ 을 실행함
- curl은 실제로 127.0.0.1 (즉, 로컬서버)로 요청을 보냄
- 로컬 IP에서만 접근 가능한 /api/v1/test/internal/에 성공적으로 접근
- 해당 경로로 접근하면 플래그를 포함한 JSON 응답을 주며, 서버는 그 응답을 다시 우리에게 전달함
- SSRF 공격 유형
