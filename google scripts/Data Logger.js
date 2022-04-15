// Daily function logging of old values
function daily() {
    var day = new Date();
    if (day.getDay() > 5 || day.getDay() == 0) {
      Logger.log('no weekday lol');
      Logger.log(day);
      return;
    }
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sh = ss.getSheetByName("Worksheet");
    var freeze = sh.getRange("B2:K7").getFormulas();
    sh.insertRowAfter(8);
    var value = sh.getRange("A8:L8").getValues();
    sh.getRange("A9:L9").setValues(value);
    sh.getRange("B2:K7").setFormulas(freeze);
  
    var ssb = SpreadsheetApp.getActiveSpreadsheet();
    var shb = ssb.getSheetByName("Algorithm");
    var freeze2 = shb.getRange("B2:AE2").getFormulas();
    shb.insertRowAfter(2);
    var valueb = shb.getRange("A2:AE2").getValues();
    shb.getRange("A3:AE3").setValues(valueb);
    shb.getRange("B2:AE2").setFormulas(freeze2);
  }