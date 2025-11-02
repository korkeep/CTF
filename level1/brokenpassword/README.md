```c
undefined8 main(void)

{
  int iVar1;
  undefined8 *local_48;
  undefined8 local_40;
  char local_38 [40];
  long local_10;

  iVar1 = open("/dev/urandom",0);
  read(iVar1,password,8);
  close(iVar1);

  puts("can u guess me?");
  read_input(local_38,0x20);
  iVar1 = strncmp(password,local_38,8);

  if (iVar1 == 0) {
    system("cat flag");
  }
  else {
    puts("wrong... :p");
    puts("can you try another path? maybe impossible");
    printf("> ");
    read_input(&local_48,8);
    printf("> ");
    read_input(&local_40,8);
    *local_48 = local_40;
    puts("wish your happy sleep");
  }
  return 0;
}
```
