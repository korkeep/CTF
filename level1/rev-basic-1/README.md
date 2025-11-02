## rev-basic-1
> 문제 URL: https://dreamhack.io/wargame/challenges/15  
> 이 문제는 사용자에게 문자열 입력을 받아 정해진 방법으로 입력값을 검증하여 correct 또는 wrong을 출력하는 프로그램이 주어집니다. 해당 바이너리를 분석하여 correct를 출력하는 입력값을 찾으세요!

### Solve
1. `ghidra` 이용 실행파일 정적 분석, 아래와 같은 함수 확인
```c
undefined8 FUN_140001000(char *param_1)

{
  undefined8 uVar1;
  
  if (*param_1 == 'C') {
    if (param_1[1] == 'o') {
      if (param_1[2] == 'm') {
        if (param_1[3] == 'p') {
          if (param_1[4] == 'a') {
            if (param_1[5] == 'r') {
              if (param_1[6] == '3') {
                if (param_1[7] == '_') {
                  if (param_1[8] == 't') {
                    if (param_1[9] == 'h') {
                      if (param_1[10] == 'e') {
                        if (param_1[0xb] == '_') {
                          if (param_1[0xc] == 'c') {
                            if (param_1[0xd] == 'h') {
                              if (param_1[0xe] == '4') {
                                if (param_1[0xf] == 'r') {
                                  if (param_1[0x10] == 'a') {
                                    if (param_1[0x11] == 'c') {
                                      if (param_1[0x12] == 't') {
                                        if (param_1[0x13] == '3') {
                                          if (param_1[0x14] == 'r') {
                                            if (param_1[0x15] == '\0') {
                                              uVar1 = 1;
                                            }
                                            else {
                                              uVar1 = 0;
                                            }
                                          }
                                          else {
                                            uVar1 = 0;
                                          }
                                        }
                                        // 생략...
  return uVar1;
}

```

2. 위 코드에서 `FUN_140001000`에서 각 인덱스 char 비교를 통해 input과 비교하는 것 확인, 즉 정답은 `DH{Compar3_the_ch4ract3r}`임