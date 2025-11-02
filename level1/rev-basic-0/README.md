## rev-basic-0
> 문제 URL: https://dreamhack.io/wargame/challenges/14  
> 이 문제는 사용자에게 문자열 입력을 받아 정해진 방법으로 입력값을 검증하여 correct 또는 wrong을 출력하는 프로그램이 주어집니다. 해당 바이너리를 분석하여 correct를 출력하는 입력값을 찾으세요!

### Solve
1. `ghidra` 이용 실행파일 정적 분석, 아래와 같은 함수 확인
```c
bool FUN_140001000(char *param_1)

{
  int iVar1;
  
  iVar1 = strcmp(param_1,"Compar3_the_str1ng");
  return iVar1 == 0;
}
```

2. 위 코드에서 `FUN_140001000`에서 strcmp를 통해 input과 비교하는 것 확인, 즉 정답은 `Compar3_the_str1ng`임