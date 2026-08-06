# STATE, thevfxsupervisor.github.io

**Read this first.** What is true right now, what is stale, what is unverified.
Last updated 2026-08-06 by the `windows` seat.

## Status: LIVE and healthy, on the custom domain

**https://thevfxsupervisor.com/** serves from `main:/docs` (cut over 2026-08-06). All pages, both logo assets,
`sitemap.xml` and `robots.txt` verified 200 on 2026-08-05.

Pages: `/`, `/projects/`, `/projects/breakdown-studio/`, `/projects/link-session/`, `/course/`,
`/notes/`, `/notes/how-a-one-person-vfx-department-orchestrates-ai/`, `/about/`.

## Landed recently (all verified live)

- **Cross-page backlinks.** Every content page routes to the others via `related_section()`. The
  course page used to be a dead end.
- **Logo + favicon.** The aperture mark replaced a placeholder. Header mark is 40px.
- **Accent is the logo blue `#0585f8`.** Went orange, then a mis-sampled duller blue `#1595e0`, then
  the correct value. Status green moved to the cooler mint `#5ad3c0`.
- **Accessibility fixes** from a design audit: primary button ink darkened (the light-on-blue
  combination failed AA at 3.06:1), mobile nav no longer hides Course/Notes/About, and a `<main>`
  landmark plus a skip link were added.
- Open Graph, canonical tags, sitemap and robots were added by another seat; `og:image` now points at
  the logo through a `{{SITE}}` token that respects `SITE_CANONICAL`.

## Open items

1. ~~Domain cutover~~ **DONE 2026-08-06.** Live at https://thevfxsupervisor.com with HTTPS; www 301s to apex and the old github.io 301s to the new domain. Google MX records survived untouched. `dev/DOMAIN-CUTOVER.md` is kept as the record of how it was done and how to roll back.
   both resolve to `64.68.200.44`. Full runbook in `dev/DOMAIN-CUTOVER.md`. Needs Geoff to change the
   easyDNS records first. **Do not flip `CUTOVER_DONE` or remove the `.gitignore` line before DNS
   actually resolves to GitHub**, that takes the site down.
2. **Waitlist endpoint not deployed.** `waitlist.gs` needs deploying as a Google Apps Script web app
   per `WAITLIST_SETUP.md`, then paste the URL into `content/pages/course.md` `waitlist_endpoint:`,
   rebuild, push. Until then the form falls back to a mailto. Geoff-gated.
3. **A Sunsama task for the domain steps was requested but not created**, because the Sunsama MCP
   needs an interactive OAuth click. Content is ready in `dev/DOMAIN-CUTOVER.md`.

## Gotchas that have already cost time

- **CRLF noise.** Git reports whole files as changed when only line endings differ. A huge-looking
  diff is usually not a huge change. Do not panic that a redesign is undeployed.
- **Concurrent editor.** Another seat edits `content/` while this seat edits `build.py`, `templates/`
  and `static/`. Expect rejected pushes; rebase and re-run `build.py`.
- **Pages build API lags.** It reported an older commit as "built" while the new CSS was already
  being served. Trust the served file, not the API.
