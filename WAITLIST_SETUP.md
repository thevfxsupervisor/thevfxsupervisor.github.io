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
reservation appends `timestamp, email, name, note`. The Sheet is private to Geoff; the web app writes
to it under his authorization. Reservations still turn into invoices by hand: deploying this only
changed HOW they arrive (rows, not email), not the invoicing.

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
