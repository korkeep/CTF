## Flying Chars

> 문제 URL: https://dreamhack.io/wargame/challenges/850  
> 날아다니는 글자들을 멈춰서 전체 문자열을 알아내세요! 플래그 형식은 DH{전체 문자열} 입니다.

### Solve

1. `html` 내 `<script>`부분 제거하고, 아래와 같은 `js` 코드 추가

```js
let imageFiles = [
  "/static/images/10.png",
  "/static/images/17.png",
  "/static/images/13.png",
  "/static/images/7.png",
  "/static/images/16.png",
  "/static/images/8.png",
  "/static/images/14.png",
  "/static/images/2.png",
  "/static/images/9.png",
  "/static/images/5.png",
  "/static/images/11.png",
  "/static/images/6.png",
  "/static/images/12.png",
  "/static/images/3.png",
  "/static/images/0.png",
  "/static/images/19.png",
  "/static/images/4.png",
  "/static/images/15.png",
  "/static/images/18.png",
  "/static/images/1.png",
];
let imageElements = [];

// 이미지를 생성하고 화면에 추가
for (let i = 0; i < imageFiles.length; i++) {
  imageElements[i] = document.createElement("img");
  imageElements[i].src = imageFiles[i];
  imageElements[i].style.display = "block"; // 이미지를 block 요소로 설정
  imageElements[i].style.width = "100px"; // 이미지 크기 조정 (원하는 크기로 수정 가능)
  imageElements[i].style.height = "100px"; // 이미지 크기 조정
  document.getElementById("box").appendChild(imageElements[i]);
}
```

2. 멈춰진 내용에서 플래그 추출

```bash
DH{Too_H4rd_to_sEe_th3_Ch4rs_x.x}
```
