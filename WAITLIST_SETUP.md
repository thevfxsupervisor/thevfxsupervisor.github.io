# Booking and the waitlist endpoint

**CURRENT as of 2026-08-05.** The course page changed from a waitlist into a dated, priced offer
(Thursday 3 September 2026, 450 USD), so this document changed with it.

## How booking works right now, and why

**Reservations arrive by email and Geoff invoices from Wangle Media ApS.** There is no card checkout,
deliberately.

That is not a stopgap to apologise for. This audience is professional: **most attendees expense the
course**, and a finance department wants a VAT invoice from a real company, not a card receipt. It
also means no payment rail has to exist before the first seat can be sold, and the Stripe account
needs Geoff's ID, bank details and UBO information that nobody else can enter.

**The tradeoff, stated honestly:** an invoice is paid on terms, a card is paid on booking. So cash
lands later than the launch research assumed. If seats start moving, Stripe is the upgrade.

## What the form does with no endpoint configured

`waitlist_endpoint:` in `content/pages/course.md` is empty, so the form composes a `mailto:` to
`contact_email` with the subject "Reserve a seat: 3 September workshop" and the details in the body.

**It used to announce "Waitlist form is not wired up yet. Opening an email instead."** That told
every visitor, at the exact moment they had decided to sign up, that the operation was amateur. Zero
signups were ever captured. It now confirms confidently and shows a visible fallback link, because
`window.location.href` to a `mailto:` **silently does nothing** for anyone with no mail client
configured, and on desktop that is a lot of people who were getting no feedback at all.

## If you later want rows in a Sheet instead of emails

`waitlist.gs` in this folder still works and is unchanged. It needs a browser OAuth consent only
Geoff can give, which is why it has never been deployed.

1. [script.google.com](https://script.google.com/), then **New project**.
2. Paste in `waitlist.gs`, rename the project to something like `thevfxsupervisor-booking`.
3. **Deploy > New deployment**, gear next to "Select type" > **Web app**.
   Execute as **Me**, Who has access **Anyone**.
4. **Deploy**, authorize the script (it is your own), copy the **Web app URL**.
5. Paste it into `waitlist_endpoint:` in `content/pages/course.md`, run `python3 build.py`, push.

**The bound-spreadsheet trap:** if you create the project from script.google.com directly it has no
bound spreadsheet, and `SpreadsheetApp.getActiveSpreadsheet()` fails. Create the Google Sheet first,
then **Extensions > Apps Script** from inside it, and paste `waitlist.gs` there. That binds it
automatically, and each reservation appends `timestamp, email, name, note`.

**Re-deploying after an edit:** **Deploy > Manage deployments > edit (pencil) > New version >
Deploy**. A plain save does NOT push new code to the live web app URL.

**Deploying this does not change the invoicing.** It only changes reservations from arriving as email
to arriving as rows. Someone still sends the invoice.

## Open decisions that are Geoff's, not mine

Unanswered on the live page, and a buyer will ask:

- **Is it recorded, and do attendees get the recording?**
- **Refund, or transfer to a later date, if someone cannot attend?**
- **What happens if too few seats sell to run it?**

The page promises none of these, which is safer than inventing a policy. Answer them before the first
invoice goes out, not after.
