## 🌱 simple-web-request

> 문제 URL: https://dreamhack.io/wargame/challenges/830  
> STEP 1~2를 거쳐 FLAG 페이지에 도달하면 플래그가 출력됩니다. 플래그는 flag.txt 파일과 FLAG 변수에 있습니다.

### Solve

1. `app.py`에 있는 코드 분석해서 `step 1` 통과

```python
if prm1 == "getget" and prm2 == "rerequest":
    return redirect(url_for("step2", prev_step_num = step1_num))
```

2. `app.py`에 있는 코드 분석해서 `step 2` 통과

```python
if prm1 == "pooost" and prm2 == "requeeest":
    return render_template("flag.html", flag_txt=FLAG)
```

3. `flag` 추출

```bash
DH{c46b414ddba26adfa4606c59655bda0a18fbe260606b042b52d865e0160eea0e}
```
