# Booking and the waitlist endpoint

**CURRENT as of 2026-08-07.** The course page is a dated, priced offer (Thursday 3 September 2026,
founding cohort 325 USD). **The waitlist form is now LIVE:** it posts to a deployed Google Apps Script
web app that appends each signup to a private Google Sheet in Geoff's Drive. The `mailto:` is now only
a fallback for when that POST fails. Endpoint URL lives in `waitlist_endpoint:` in
`content/pages/course.md`.

## How booking works right now, and why

**Reservations arrive by email and Geoff invoices from Wangle Media ApS.** There is no card checkout,
deliberately.

That is not a stopgap to apologise for. This audience is professional: **most attendees expense the
course**, and a finance department wants a VAT invoice from a real company, not a card receipt. It
also means no payment rail has to exist before the first seat can be sold, and the Stripe account
needs Geoff's ID, bank details and UBO information that nobody else can enter.

**The tradeoff, stated honestly:** an invoice is paid on terms, a card is paid on booking. So cash
lands later than the launch research assumed. If seats start moving, Stripe is the upgrade.

## What the form does (endpoint configured)

`waitlist_endpoint:` in `content/pages/course.md` holds the deployed web-app URL, so on submit the
form POSTs `{email, name, note}` as `text/plain` (a "simple" request, so no CORS preflight) and the
script appends a row to the bound Sheet. On success it shows a confirmation; if the POST fails it
falls back to composing a `mailto:` to `contact_email` and shows a visible fallback link, because
`window.location.href` to a `mailto:` **silently does nothing** for anyone with no mail client
configured. Verified end to end 2026-08-07: a cross-origin POST returned `{"ok":true}` and a row
landed in the Sheet.

## The deployment (LIVE, 2026-08-07)

`waitlist.gs` is deployed as a **bound** Apps Script web app (Extensions > Apps Script from inside the
Sheet, so `getActiveSpreadsheet()` resolves), Execute as **Me**, Who has access **Anyone**. Each
reservation appends `timestamp, email, name, note` AND emails geoff@wanglemedia.com a notification
(`MailApp.sendEmail`, isolated in its own try so a mail failure never loses the row). The Sheet is
private to Geoff; the web app writes to it under his authorization. Reservations still turn into
invoices by hand: this only changed HOW they arrive (a row plus an email), not the invoicing.

The `MailApp` line adds a "send email as you" scope, so editing it in requires re-authorizing the
project (run any function once, click through consent) and then redeploying a new version. Verified
end to end 2026-08-07: a test signup landed a row and delivered the notification email.

**Re-deploying after editing `waitlist.gs`:** in the Apps Script editor, **Deploy > Manage
deployments > edit (pencil) > New version > Deploy**. A plain save does NOT push new code to the live
URL. If you ever create a NEW deployment instead, its URL changes, so update `waitlist_endpoint:` in
`content/pages/course.md`, rebuild, and push.

## Open decisions that are Geoff's, not mine

Unanswered on the live page, and a buyer will ask:

- **Is it recorded, and do attendees get the recording?**
- **Refund, or transfer to a later date, if someone cannot attend?**
- **What happens if too few seats sell to run it?**

The page promises none of these, which is safer than inventing a policy. Answer them before the first
invoice goes out, not after.

## Narrowing the permissions (retrofit, 2026-08-23)

By default Apps Script asks for **"see, edit, create and delete all your Google
Sheets spreadsheets"**. This script only ever touches the sheet it is attached to
(`SpreadsheetApp.getActiveSpreadsheet`) and sends mail (`MailApp.sendEmail`), so
that grant is far wider than it needs.

`appsscript.json` in this repo pins it to two scopes:

- `spreadsheets.currentonly` - only the attached sheet, not every spreadsheet
- `script.send_mail` - unavoidable, mailing the notification is the job

### Applying it, and why the order matters

**This form is live and capturing course signups. A silent failure loses real
leads, so the test at the end is not optional.**

1. Open the script (Extensions > Apps Script from the waitlist sheet).
2. Gear icon (Project Settings) > tick **Show "appsscript.json" manifest file**.
3. Open the manifest that appears and replace it with the one from this repo.
4. **Deploy > Manage deployments**, edit the existing deployment, set Version to
   **New version**, Deploy. Editing the existing deployment keeps the SAME URL,
   so the live page keeps working. Do NOT create a new deployment: that issues a
   different URL and the site would still be posting to the old one.
5. Re-authorise if prompted. Reducing scopes usually does not re-prompt, since
   the existing grant already covers the narrower set.

### Then TEST it, before walking away

Submit a real signup through the live `/course` page and confirm BOTH:

- a row appears in the waitlist sheet
- the notification email arrives

If either is missing, the change broke it. Revert by restoring the previous
manifest and deploying a new version of the same deployment.

Delete the test row afterwards.

**Why the test matters more here than on the media kit form:** that one is new
and unused, so a failure costs nothing. This one is live ahead of the course, and
a form that silently stops recording looks exactly like a quiet week.
