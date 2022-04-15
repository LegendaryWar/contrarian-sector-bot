// Regex handler for scraping PEs
function pe10Finder(sector) {
    var url = "https://www.gurufocus.com/sector_shiller_pe.php";
    const html = UrlFetchApp.fetch(url).getContentText();
  
    if (sector == "energy") {
      return html.match(/84e35ac2b496fca6fd0?>[0-9][0-9]<\/a><\/b><\/u><\/td><td class='text_center'>([0-9]{1,2}\.[0-9]{1,2})<\/td>/)[1].trim();
    }
    if (sector == "financial") {
      return html.match(/73293cbe24953b?>[0-9][0-9]<\/a><\/b><\/u><\/td><td class='text_center'>([0-9]{1,2}\.[0-9]{1,2})<\/td>/)[1].trim();
    }
    if (sector == "industrials") {
      return html.match(/e0a6a8a55d73?>[0-9][0-9]<\/a><\/b><\/u><\/td><td class='text_center'>([0-9]{1,2}\.[0-9]{1,2})<\/td>/)[1].trim();
    }
    if (sector == "consumerd") {
      return html.match(/491bc7cb5559?>[0-9][0-9]<\/a><\/b><\/u><\/td><td class='text_center'>([0-9]{1,2}\.[0-9]{1,2})<\/td>/)[1].trim();
    }
    if (sector == "materials") {
      return html.match(/220080af48899b728a9?>[0-9][0-9]<\/a><\/b><\/u><\/td><td class='text_center'>([0-9]{1,2}\.[0-9]{1,2})<\/td>/)[1].trim();
    }
    if (sector == "healthcare") {
      return html.match(/8dfe6e07e54baf40b?>[0-9][0-9]<\/a><\/b><\/u><\/td><td class='text_center'>([0-9]{1,2}\.[0-9]{1,2})<\/td>/)[1].trim();
    }
    if (sector == "technology") {
      return html.match(/123b1cfcdeba7b3cf5?>[0-9][0-9]<\/a><\/b><\/u><\/td><td class='text_center'>([0-9]{1,2}\.[0-9]{1,2})<\/td>/)[1].trim();
    }
    if (sector == "consumerc") {
      return html.match(/d02de2fee6ff209a5e6c?>[0-9][0-9]<\/a><\/b><\/u><\/td><td class='text_center'>([0-9]{1,2}\.[0-9]{1,2})<\/td>/)[1].trim();
    }
    if (sector == "communication") {
      return html.match(/4bb37360c09ba?>[0-9][0-9]<\/a><\/b><\/u><\/td><td class='text_center'>([0-9]{1,2}\.[0-9]{1,2})<\/td>/)[1].trim();
    }
    if (sector == "realestate") {
      return html.match(/\/mrkg753?>[0-9][0-9]<\/a><\/b><\/u><\/td><td class='text_center'>([0-9]{1,2}\.[0-9]{1,2})<\/td>/)[1].trim();
    }
    if (sector == "utilities") {
      return html.match(/cc371c4802b?>[0-9][0-9]<\/a><\/b><\/u><\/td><td class='text_center'>([0-9]{1,2}\.[0-9]{1,2})<\/td>/)[1].trim();
    }
    if (sector == "snpaverage") {
      var url = "https://www.multpl.com/shiller-pe";
      const html = UrlFetchApp.fetch(url).getContentText();
      return html.match(/<td class="left">Mean: <\/td>\n<td>([0-9][0-9].[0-9][0-9])/)[1].trim();
    }
    if (sector == "snpcurrent") {
      var url = "https://www.multpl.com/shiller-pe";
      const html = UrlFetchApp.fetch(url).getContentText();
      return html.match(/Shiller PE Ratio<\/span>:<\/b>\n([0-9][0-9].[0-9][0-9])/)[1].trim();
  
    }
    else {
      return "null"
    }
  }
  