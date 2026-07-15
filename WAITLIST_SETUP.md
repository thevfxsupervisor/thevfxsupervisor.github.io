# Waitlist endpoint setup

Until this is done, the course waitlist form on `/course/` falls back to a
`mailto:` link, gracefully, with a status note telling the visitor the form
isn't wired up yet. Nothing breaks if you skip this step; it just means you
get emails instead of Sheet rows until you deploy it.

## The 5 clicks

1. Go to [script.google.com](https://script.google.com/), click **New project**.
2. Delete the placeholder code and paste in the contents of `waitlist.gs`
   (in this folder). Rename the project (top left) to something like
   `thevfxsupervisor-waitlist`.
3. Click **Deploy > New deployment**. Click the gear next to "Select type"
   and choose **Web app**. Set:
   - Execute as: **Me**
   - Who has access: **Anyone**
4. Click **Deploy**, authorize the script when prompted (it's your own
   script, so this is safe), and copy the **Web app URL** it gives you.
5. Paste that URL into the `waitlist_endpoint:` field in
   `content/pages/course.md`'s frontmatter, then run
   `& "C:\Program Files\Shotgun\Python3\python.exe" build.py` and push.

## Where the data lands

The script appends rows to whatever spreadsheet the Apps Script project is
bound to. If you created the project from script.google.com directly (not
"Extensions > Apps Script" inside a Sheet), it has no bound spreadsheet, and
`SpreadsheetApp.getActiveSpreadsheet()` will fail. Easiest fix: create a new
Google Sheet first, then go to **Extensions > Apps Script** from inside that
Sheet, and paste `waitlist.gs` there instead of starting from
script.google.com. That binds the script to the Sheet automatically, and
every waitlist signup appends a row: `timestamp, email, name, note`.

## Re-deploying after an edit

If you change `waitlist.gs` later, use **Deploy > Manage deployments >
edit (pencil) > New version > Deploy**. A plain save does not push the new
code to the live web app URL.
