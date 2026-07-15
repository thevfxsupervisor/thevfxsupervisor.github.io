/**
 * waitlist.gs
 *
 * Google Apps Script backend for the course waitlist form on
 * thevfxsupervisor.com/course/.
 *
 * Appends {timestamp, email, name, note} to the active Sheet and returns
 * {"ok": true} as JSON. See WAITLIST_SETUP.md for the 5-click deploy.
 */

function doPost(e) {
  var result = { ok: false };
  try {
    var data = JSON.parse(e.postData.contents);
    var email = (data.email || "").toString().trim();
    var name = (data.name || "").toString().trim();
    var note = (data.note || "").toString().trim();

    if (!email) {
      return jsonOutput({ ok: false, error: "missing email" });
    }

    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(["timestamp", "email", "name", "note"]);
    }
    sheet.appendRow([new Date(), email, name, note]);

    result.ok = true;
  } catch (err) {
    result.ok = false;
    result.error = err.toString();
  }
  return jsonOutput(result);
}

function jsonOutput(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
