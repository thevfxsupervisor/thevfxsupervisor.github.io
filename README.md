# thevfxsupervisor.com

Source for Geoffrey Hancock's personal-brand site. Static, no framework
runtime. Markdown content in `content/`, a tiny Python build script
(`build.py`, stdlib only, no pip installs), rendered into `docs/`, which
GitHub Pages serves from the `main` branch of the public repo
`thevfxsupervisor.github.io` (a GitHub Pages **user site**, served at the
domain root, not under `/repo-name/`). No GitHub Actions needed.

## Editing workflow

1. Edit a `.md` file under `content/`.
   - `content/pages/home.md`, `about.md`, `course.md` — singleton pages.
   - `content/projects/breakdown-studio.md` — the project launch page.
   - `content/notes/*.md` — one file per note post. Copy an existing one
     for the frontmatter shape. Set `draft: true` to keep a post out of
     the build while you're writing it.
2. Run the build:
   ```powershell
   & "C:\Program Files\Shotgun\Python3\python.exe" build.py
   ```
3. Check `docs/` rendered the way you expect (open the HTML files, or
   spot-check in a browser).
4. `git add -A && git commit -m "..." && git push`.

GitHub Pages picks up the push automatically; nothing else to trigger.

## Content format

Each `.md` file starts with a `---`-delimited frontmatter block of
`key: value` pairs (YAML-lite, not full YAML), followed by the page body in
markdown. `type:` (`page` / `project` / `note`) makes the `content/`
directory double as an OKF-ish bundle: each file is a self-describing
content unit, not just a bag of prose.

The markdown converter (in `build.py`, hand-written, no dependencies)
supports:

- `#`, `##`, `###` headings
- paragraphs
- `**bold**`, `*italic*`, `` `code` ``
- `[link text](url)`
- `![alt](src)` images
- `- ` bullet lists and `1. ` numbered lists

For pages that need small repeating structured blocks (the three home-page
proof pillars, the Breakdown Studio stats row, the course curriculum list),
wrap a run of `### Title` / body pairs in an HTML-comment marker inside the
markdown body:

```markdown
<!-- pillars -->
### First pillar title
Body text for the first pillar.

### Second pillar title
Body text for the second pillar.
<!-- /pillars -->
```

`build.py` extracts anything between `<!-- name -->` and `<!-- /name -->`,
splits it into title/body pairs on the `### ` headings, and each page's
renderer turns that into the matching design component (`pillars`,
`stats`/`tiers`, `included`). See `build.py` for the exact block names each
page expects.

## Links

- Root paths (`/about/`, `/course/`, `/projects/breakdown-studio/`, etc.)
  are absolute from the site root throughout, which is correct for a
  GitHub Pages **user** site (`thevfxsupervisor.github.io`) and for the
  custom domain (`thevfxsupervisor.com`) once DNS is pointed at it. Do not
  change these to relative paths or add a repo-name prefix.
- `docs/CNAME` contains `thevfxsupervisor.com`. It's harmless before DNS is
  cut over; GitHub Pages just ignores it until the domain resolves here.

## Waitlist

The course waitlist form on `/course/` posts to a Google Apps Script
endpoint. Until that endpoint is deployed, `WAITLIST_ENDPOINT` (set from
`waitlist_endpoint:` in `content/pages/course.md`'s frontmatter) is empty,
and the form falls back to a `mailto:` link with a status note explaining
that. See `WAITLIST_SETUP.md` for the 5-click deploy of `waitlist.gs`, and
`content/pages/course.md` for where to paste the resulting URL.

## Hard rules (see the site's own CLAUDE.md for the full context)

- No em-dashes or en-dashes anywhere, in content or copy.
- No client, show or vendor names. The only named work anywhere on this
  site is Breakdown Studio itself; everything else is the anonymous
  "a real feature in production" phrasing.
- Single dark look (graphite / amber), no light theme, matching the
  Breakdown Studio product site's design language.
