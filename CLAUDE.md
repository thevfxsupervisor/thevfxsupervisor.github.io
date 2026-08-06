# CLAUDE.md, thevfxsupervisor.github.io

Guidance for Claude Code working in this repo. **This file is the project context; read `STATE.md`
first for what is true right now.**

Fleet-wide rules (persona, no em-dashes, autonomy, secrets, leak-gate) come from the global
`C:\Users\geoff\.claude\CLAUDE.md`, which includes `geoff-agents/shared-config/wintermute-persona.md`.
Do not restate them here.

## What this is

Geoff's personal brand site: portfolio, case studies for the open-source tools, a course waitlist,
and short notes. **LIVE at https://thevfxsupervisor.github.io/**.

**This repo is PUBLIC.** Everything in it is world-readable, including git history. No client names,
no project names, no shot codes, no sheet IDs, no personal paths. Geoff's own name and credits are
intentional, it is his portfolio. See `geoff-agents/knowledge/repo-visibility.md`.

## Build and deploy

Static site generator, stdlib only, no pip installs:

    & "C:\Program Files\Shotgun\Python3\python.exe" build.py

Reads `content/` (markdown + YAML-lite frontmatter), renders through `templates/base.html`, writes
static HTML into `docs/`. GitHub Pages serves `main:/docs`, so deploy is just commit and push. Always
rebuild before committing, or `docs/` drifts from `content/`.

## The one thing that can take the site down

`thevfxsupervisor.com` is **parked at easyDNS and has never been cut over.** If `docs/CNAME` is ever
committed, Pages auto-sets the custom domain and 301-redirects github.io into the parked lander, so
the site goes dark. That happened on 2026-07-29.

Two gates prevent it: `build.py` has `CUTOVER_DONE = False` so it does not emit the file, and
`.gitignore` excludes `docs/CNAME`. **Do not remove either** until DNS actually points at GitHub.
The full cutover procedure is in `dev/DOMAIN-CUTOVER.md`.

## Brand tokens (shared with the Breakdown Studio site)

Defined in `static/style.css` `:root`. Keep both sites identical.

- Accent `--amber: #0585f8`, hover `--amber-soft: #3aa3f5`. Despite the variable name it is **blue**:
  it is sampled from the pure-blue blades of the logo. It was orange historically, hence the name.
  Do not "correct" the accent by averaging logo pixels, that pulls toward the green end and gives a
  duller colour; sample the saturated blue blades only.
- Status green `--green: #5ad3c0`, a cooler mint chosen so status does not read as brand. The old
  sage `#5bbf8f` sat only 9 degrees off the logo green.
- Ground `--bg: #131619`, text `--txt: #e9e6df`.
- Button ink on the accent is dark (`#06131d`). Light ink only reaches 3.06:1 and fails AA.
- Logo: `static/logo-icon.png` (the aperture mark, icon only, no wordmark). `static/favicon.png` is a
  simplified aperture with no text or drips, because the full mark turns to mush at 16px. Source
  artwork is "Logo mockup 03" under `N:\projects\thevfxsupervisor.com\2022 The VFX Supervisor\Logo\`.
  Mockup 03 is the bluer variant; 04 is greener. They are not interchangeable.

## Cross-linking

`related_section()` in `build.py` renders a "Keep exploring" strip on every content page so each page
reaches the others. Add new pages to it. The header and footer nav in `templates/base.html` cover
the section indexes. Nav must not hide sections on mobile: it tightens instead, and only the header
CTA drops under 560px.

## Content conventions

- `content/pages/` home, about, course. `content/projects/` case studies. `content/notes/` posts.
- Frontmatter is YAML-lite. `draft: true` excludes a note.
- Resolve nothing by position; the builder keys on frontmatter names.
- Notes carry no client or show names, ever.

## Working rules that bite here

- **Another agent edits content concurrently.** Pushes get rejected regularly. The routine is: fetch,
  rebase, re-run `build.py` (that regenerates `docs/` and resolves the generated-file conflicts),
  `git add -A`, `git rebase --continue`. Only `templates/`, `static/`, `build.py` and `content/` are
  real conflicts; everything under `docs/` is generated.
- **Claims about Geoff's credentials need his confirmation, and when sources disagree publish the
  lower claim.** A seat once published "two award wins" from a summarised web fetch; the truth is one
  VES win (Changeling, 2008) and one Robert nomination (2020). He is the authority on himself.
- **Verify after deploying.** Pages build status lags; the served asset is the truth. Check with
  `curl -s https://thevfxsupervisor.github.io/static/style.css | grep amber` rather than trusting the
  build API, and cache-bust with a query string.
