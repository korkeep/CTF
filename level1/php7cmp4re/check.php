<html>
<head>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
<title>php7cmp4re</title>
</head>
<body>
    <!-- Fixed navbar -->
    <nav class="navbar navbar-default navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <a class="navbar-brand" href="/">php7cmp4re</a>
        </div>
        <div id="navbar">
          <ul class="nav navbar-nav">
            <li><a href="/">Index page</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>
    <div class="container">
    <?php
    require_once('flag.php');
    error_reporting(0);
    // POST request
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
      $input_1 = $_POST["input1"] ? $_POST["input1"] : "";
      $input_2 = $_POST["input2"] ? $_POST["input2"] : "";
      sleep(1);

      if($input_1 != "" && $input_2 != ""){
        if(strlen($input_1) < 4){
          if($input_1 < "8" && $input_1 < "7.A" && $input_1 > "7.9"){
            if(strlen($input_2) < 3 && strlen($input_2) > 1){
              if($input_2 < 74 && $input_2 > "74"){
                echo "</br></br></br><pre>FLAG\n";
                echo $flag;
                echo "</pre>";
              } else echo "<br><br><br><h4>Good try.</h4>";
            } else echo "<br><br><br><h4>Good try.</h4><br>";
          } else echo "<br><br><br><h4>Try again.</h4><br>";
        } else echo "<br><br><br><h4>Try again.</h4><br>";
      } else{
        echo '<br><br><br><h4>Fill the input box.</h4>';
      }
    } else echo "<br><br><br><h3>WHat??!</h3>";
    ?> 
    </div> 
</body>
</html>