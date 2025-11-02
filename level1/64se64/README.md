## 64se64
> 문제 URL: https://dreamhack.io/wargame/challenges/872  
> "Welcome! 👋"을 출력하는 html 페이지입니다. 소스 코드를 확인하여 문제를 풀고 플래그를 획득하세요.

### Solve
1. `html`에 아래와 같은 value 숨겨져 있었음
```html
<input type="hidden" name="64se64_encoding" value="IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwphc2M9WzY4LCA3MiwgMTIzLCA5OCwgMTAxLCA0OCwgNTIsIDU0LCA5OCwgNTUsIDUzLCA1MCwgNTAsIDk3LCA5NywgNTAsIDEwMSwgNTAsIDU2LCAxMDIsIDUwLCA1NSwgNTQsIDEwMSwgNDgsIDk5LCA1NywgNDksIDQ4LCA1MywgNTAsIDQ5LCAxMDIsIDUwLCA1MSwgOTcsIDQ4LCA1MywgNTYsIDU1LCA0OCwgNDgsIDUzLCA5NywgNTYsIDUxLCA1NSwgNTUsIDUxLCA1NSwgNDgsIDk3LCA0OSwgNDksIDEwMSwgNTMsIDEwMSwgNTIsIDEwMCwgOTksIDQ5LCA1MywgMTAyLCA5OCwgNTAsIDk3LCA5OCwgMTI1XQphcnI9WzAgZm9yIGkgaW4gcmFuZ2UoNjgpXQpmb3IgaSBpbiByYW5nZSgwLDY4KToKICAgIGFycltpXT1jaHIoYXNjW2ldKQpmbGFnPScnLmpvaW4oYXJyKQpwcmludChmbGFnKQ==">
```

2. 해당 내용을 Base64로 디코딩하면 결과는 다음과 같은 파이썬 코드
```py
#!/usr/bin/env python3
asc=[68, 72, 123, 98, 101, 48, 52, 54, 98, 55, 53, 50, 50, 97, 97, 50, 101, 50, 56, 102, 50, 55, 54, 101, 48, 99, 57, 49, 48, 53, 50, 49, 102, 50, 51, 97, 48, 53, 56, 55, 48, 48, 53, 97, 56, 51, 55, 55, 51, 55, 48, 97, 49, 49, 101, 53, 101, 52, 100, 99, 49, 53, 102, 98, 50, 97, 98, 125]
arr=[0 for i in range(68)]
for i in range(0,68):
    arr[i]=chr(asc[i])
flag=''.join(arr)
print(flag)
```

3. 파이썬 파일 실행 결과
```bash
$ python ./result.py
DH{be046b7522aa2e28f276e0c910521f23a0587005a8377370a11e5e4dc15fb2ab}
```