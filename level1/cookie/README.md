## cookie
> 문제 URL: https://dreamhack.io/wargame/challenges/6  
> 자바스크립트는 `document.cookie` 속성을 이용하여 쿠키를 `create`, `delete`할 수 있음  

### create
```js
// 쿠키 스트링: name=user, value=admin
// 속성값: path, expires
let currentDate = new Date();
currentDate.setHours(currentDate.getHours() + 1);
let expires = currentDate.toUTCString();
document.cookie = "user=admin; expires="+expires+"; path=/";
```

### delete
```js
// 만료 기간을 과거로 바꾸면 쿠키 만료되어 소멸
// 이때 속성값인 path를 확인해서 맞추어야 함
document.cookie = "user=admin; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
```

### cookie의 쿠키 스트링과 속성값을 확인하는 방법
1. 개발자 도구: chrome에서 F12 키를 누르거나 Ctrl + Shift + I
2. Application 탭 선택: 개발자 도구에서 "Application" 탭을 클릭
3. 쿠키 확인: 왼쪽 사이드바에서 "Cookies" 항목을 찾아 클릭
4. 쿠키 정보 확인: 쿠키 목록에서 각 쿠키를 선택하면 해당 쿠키의 상세 정보를 볼 수 있는데, 여기서 "Path" 항목을 확인할 수 있음