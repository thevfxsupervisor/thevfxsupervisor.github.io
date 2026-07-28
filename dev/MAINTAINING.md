# Maintaining the site

Internal build/deploy/content notes. Not part of the published site.

## Serving

- Live at **https://thevfxsupervisor.github.io/** (GitHub Pages, source: `main` branch, `/docs` folder).
- `docs/.nojekyll` disables Jekyll so the `docs/` tree is served exactly as built.

## Edit -> build -> publish

1. Edit markdown under `content/` (`pages/`, `projects/`, `notes/`; `draft: true` keeps a note out of the build).
2. `python build.py` (ShotGrid Python on the Windows box:
   `& "C:\Program Files\Shotgun\Python3\python.exe" build.py`) renders `content/` into `docs/`.
3. Check `docs/`, then `git add -A && git commit && git push`. GitHub Pages redeploys automatically.

## CRITICAL: no CNAME / custom domain yet

`thevfxsupervisor.com` is **parked at easyDNS and has NOT been cut over** to GitHub Pages (it
returns an easyDNS "Parked Domain" page, HTTP 200, which is NOT the site, do not mistake that 200
for the domain being live).

If `docs/CNAME` is committed, GitHub Pages auto-sets the custom domain and **301-redirects
github.io into that parked page, taking the whole site down.** This happened once: the site was
served into the dead parking lander until the CNAME was removed and the Pages custom domain cleared.

Two guards are in place, leave both alone until real cutover:
- `build.py` no longer emits `docs/CNAME` (gated behind `CUTOVER_DONE = False`).
- `.gitignore` excludes `docs/CNAME`.

**When the DNS cutover is actually done:** add the DNS records first, confirm `thevfxsupervisor.com`
serves the real site (not the parking page), then set `CUTOVER_DONE = True` in `build.py`, remove
the `docs/CNAME` line from `.gitignore`, rebuild, and push. If serving looks wrong afterward, clear
the custom domain again with:
`gh api --method PUT repos/thevfxsupervisor/thevfxsupervisor.github.io/pages -F cname=null`

## Content format

Each `.md` file opens with a `---`-delimited frontmatter block of `key: value` pairs (YAML-lite,
not full YAML), then the page body in markdown. `type:` (`page` / `project` / `note`) makes
`content/` double as an OKF-ish bundle: each file is a self-describing content unit.

The hand-written markdown converter in `build.py` (no dependencies) supports: `#`/`##`/`###`
headings, paragraphs, `**bold**`, `*italic*`, `` `code` ``, `[text](url)` links, `![alt](src)`
images, and `- ` / `1. ` lists.

For small repeating structured blocks (the home-page proof pillars, the Breakdown Studio stats
row, the course curriculum), wrap `### Title` / body pairs in an HTML-comment marker:

```markdown
<!-- pillars -->
### First pillar title
Body text for the first pillar.

### Second pillar title
Body text for the second pillar.
<!-- /pillars -->
```

`build.py` extracts everything between `<!-- name -->` and `<!-- /name -->`, splits it into
title/body pairs on the `### ` headings, and each page's renderer turns that into the matching
component (`pillars`, `stats`/`tiers`, `included`). See `build.py` for the block names each page expects.

## Links

Root paths (`/about/`, `/course/`, `/projects/breakdown-studio/`) are absolute from the site root
throughout, which is correct for a GitHub Pages user site. Do not change them to relative paths or
add a repo-name prefix.

## Hard rules (content + design)

- **No em-dashes or en-dashes** anywhere, in content or copy.
- **No client, show, or vendor names.** The only named work anywhere on the site is Breakdown Studio
  itself; everything else uses the anonymous "a real feature in production" phrasing.
- **Single dark look** (graphite / amber), no light theme, matching the Breakdown Studio site's
  design language.

## Waitlist

The course waitlist form on `/course/` falls back to a `mailto:` link until a Google Apps Script
endpoint is deployed. See [`../WAITLIST_SETUP.md`](../WAITLIST_SETUP.md), then paste the deployment
URL into `content/pages/course.md` (`waitlist_endpoint:`), rebuild, and push.
