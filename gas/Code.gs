// 文字起こしもじもじくん：スプレッドシート保存用
// 使い方は README.md の「スプシ保存の設定」を参照

const SHEET_ID = '1-oGi7CDuMkXB6D6SEtllv9eqK8OEAeqOUM9krrqc8u8';

function doPost(e) {
  const data = JSON.parse(e.postData.contents);
  const token = PropertiesService.getScriptProperties().getProperty('TOKEN');
  if (!token || data.token !== token) {
    return ContentService.createTextOutput('NG');
  }
  const sheet = SpreadsheetApp.openById(SHEET_ID).getSheets()[0];
  sheet.appendRow([
    Utilities.formatDate(new Date(), 'Europe/Berlin', 'yyyy-MM-dd HH:mm'),
    data.mode || '',
    data.link || '',
    data.text || '',
    data.memo || ''
  ]);
  return ContentService.createTextOutput('OK');
}
