## simple-operation

> 문제 URL: https://dreamhack.io/wargame/challenges/836  
> 주어진 바이너리를 분석하고 알맞은 값을 입력하면 플래그가 출력됩니다.

### Solve

1. `ghidra` 이용해서 분석된 코드

```c
undefined8 main(void)

{
  int iVar1;
  char local_42 [9];
  char local_39 [9];
  uint local_30;
  uint local_2c;
  char *local_28;
  int local_1c;
  char *local_18;
  uint local_10;
  int local_c;

  local_2c = 0;
  local_30 = 0;
  local_10 = 0;
  initialize();
  local_18 = (char *)malloc(0x45);
  local_1c = open("./flag",0);
  read(local_1c,local_18,0x45);
  close(local_1c);
  get_rand_num(&local_30);
  printf("Random number: %#x\n",(ulong)local_30);
  printf("Input? ");
  __isoc99_scanf(&DAT_00102034,&local_2c);
  local_10 = local_2c ^ local_30;
  snprintf(local_39,9,"%08x",(ulong)local_10);
  for (local_c = 0; local_c < 8; local_c = local_c + 1) {
    local_42[local_c] = local_39[7 - local_c];
  }
  printf("Result: %s\n",local_42);
  local_28 = "a0b4c1d7";
  iVar1 = strcmp(local_42,"a0b4c1d7");
  if (iVar1 == 0) {
    puts("Congrats!");
    puts(local_18);
  }
  else {
    puts("Try again");
  }
  return 0;
}
```

2. 로직 분석 후 `flag` 추출 완료

```bash
DH{cc0017076ad93f32c8aaa21bea38af5588d95d2cdc9cf48760381cc84df4668e}
```
