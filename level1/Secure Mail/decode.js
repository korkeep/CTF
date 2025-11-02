// alert 무시
window.alert = function () {};

const format = /([0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[1,2][0-9]|3[0,1]))/;

function BFC() {
  for (let yy = 0; yy <= 99; yy++) {
    let year = yy.toString().padStart(2, "0");

    for (let MM = 0; MM <= 12; MM++) {
      let month = MM.toString().padStart(2, "0");

      for (let DD = 0; DD <= 31; DD++) {
        let day = DD.toString().padStart(2, "0");

        let testResult = `${year}${month}${day}`;

        console.log(`테스트 중: ${testResult}`);

        // test() 메서드는 주어진 문자열이 정규 표현식을 만족하는지 판별하고, 그 여부를 true 또는 false로 반환.
        if (_0x9a220(testResult)) {
          console.log("flag:", testResult);
          return testResult;
        }
      }
    }
  }
}
