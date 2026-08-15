/**
 * waitlist.gs
 *
 * Google Apps Script backend for the course waitlist form on
 * thevfxsupervisor.com/course/.  THIS FILE IS IN A PUBLIC REPO.
 *
 * On each signup it:
 *   1. appends {timestamp, email, name, question} to the active Sheet,
 *   2. emails geoff@wanglemedia.com a notification (with the question),
 *   3. auto-emails the SIGNER the lead-magnet resource, whose copy is read
 *      from a PRIVATE Script Property (see leadMagnetHtml). The lead-magnet
 *      copy is Geoff's copyrighted content and is deliberately NOT stored in
 *      this public repo.
 * Returns {"ok": true} as JSON. See WAITLIST_SETUP.md for the deploy.
 *
 * NOTE: after editing this file you MUST redeploy the web app (Deploy >
 * Manage deployments > edit > New version) for changes to take effect.
 */

function doPost(e) {
  var result = { ok: false };
  try {
    var data = JSON.parse(e.postData.contents);
    var email = (data.email || "").toString().trim();
    var name = (data.name || "").toString().trim();
    var question = (data.note || "").toString().trim(); // the form field is still named "note"

    if (!email) {
      return jsonOutput({ ok: false, error: "missing email" });
    }

    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(["timestamp", "email", "name", "question"]);
    }
    sheet.appendRow([new Date(), email, name, question]);

    // 1) Notify the owner. Isolated so a mail failure never loses the row.
    try {
      MailApp.sendEmail(
        "geoff@wanglemedia.com",
        "New waitlist signup: " + email,
        "Email: " + email +
          "\nName: " + (name || "(none)") +
          "\nQuestion: " + (question || "(none)") +
          "\n\nRow added to the Course waitlist sheet. Lead magnet auto-sent to them."
      );
    } catch (ownerErr) {
      // swallow: the signup is captured regardless
    }

    // 2) Auto-send the lead magnet to the signer. Also isolated.
    try {
      MailApp.sendEmail({
        to: email,
        subject: "Your VFX + AI gotchas list (and you are on the waitlist)",
        htmlBody: leadMagnetHtml(),
        name: "Geoff Hancock",
        replyTo: "geoff@wanglemedia.com"
      });
    } catch (leadErr) {
      // swallow: never fail the request over a mail hiccup
    }

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

/**
 * The lead-magnet email body.
 *
 * The actual copy is Geoff's COPYRIGHTED content and is NOT kept in this public
 * repo. It lives privately in this script's Script Properties under the key
 * 'LEAD_MAGNET_HTML' (Project Settings > Script Properties). The private source
 * of that HTML is course-launch/lead-magnet-gotchas.html on Geoff's box.
 *
 * If the property is unset, a short generic note is sent instead, so the flow
 * never breaks and no copyrighted list is ever hard-coded here.
 */
function leadMagnetHtml() {
  var html = PropertiesService.getScriptProperties().getProperty("LEAD_MAGNET_HTML");
  if (html && html.replace(/\s/g, "")) {
    return html;
  }
  return '<div style="font-family:Arial,Helvetica,sans-serif;line-height:1.55;color:#17202a">' +
    '<p>Thanks for joining the waitlist. Your resource is on its way shortly.</p>' +
    '<p>Geoff Hancock<br><span style="color:#888">the vfx supervisor &middot; thevfxsupervisor.com</span></p>' +
    '<p style="color:#8a929b;font-size:12px;margin-top:18px">You joined the waitlist at thevfxsupervisor.com. Reply to unsubscribe or have your details deleted. Wangle Media ApS.</p>' +
    '</div>';
}
