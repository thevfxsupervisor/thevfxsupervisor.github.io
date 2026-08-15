"""
build.py: tiny static-site builder for thevfxsupervisor.com

Usage:
    & "C:\\Program Files\\Shotgun\\Python3\\python.exe" build.py

Reads markdown + YAML-lite frontmatter from content/, renders through the
templates in templates/, and writes static HTML into docs/ (the folder
GitHub Pages serves from main branch, no Actions required).

Editing workflow:
    1. Edit a .md file in content/ (or add a new one under content/notes/
       or content/projects/).
    2. Run this script.
    3. git add -A && git commit && git push.

No pip installs. Stdlib only.
"""
import html
import hashlib
import re
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
CONTENT_DIR = ROOT_DIR / "content"
TEMPLATES_DIR = ROOT_DIR / "templates"
STATIC_DIR = ROOT_DIR / "static"
DOCS_DIR = ROOT_DIR / "docs"

SITE_ROOT = "/"  # GitHub Pages USER site (thevfxsupervisor.github.io) serves at root.
SITE_NAME = "the vfx supervisor"
DOMAIN = "thevfxsupervisor.com"

BASE_TEMPLATE = (TEMPLATES_DIR / "base.html").read_text(encoding="utf-8")
# Content-hash of the stylesheet, appended to its URL so browsers refetch it whenever it changes
# (otherwise a cached style.css shows stale styling, e.g. an old text alignment, after a deploy).
CSS_VERSION = hashlib.md5((STATIC_DIR / "style.css").read_bytes()).hexdigest()[:8]


# --------------------------------------------------------------------------
# Frontmatter / content parsing
# --------------------------------------------------------------------------

def parse_frontmatter(text):
    """Split a content file into (dict frontmatter, body markdown).

    Frontmatter is YAML-lite:
        key: single line value
        key: |
          block scalar, dedented, kept verbatim until a line
          at the original indentation (or less) appears.
    """
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    fm_text = text[4:end]
    body = text[end + 5:]

    fm = {}
    lines = fm_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        m = re.match(r"^([A-Za-z0-9_]+):\s?(.*)$", line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2)
        if val.strip() == "|":
            i += 1
            block_lines = []
            while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                block_lines.append(lines[i][2:] if lines[i].startswith("  ") else "")
                i += 1
            fm[key] = "\n".join(block_lines).strip("\n")
            continue
        fm[key] = val.strip()
        i += 1
    return fm, body


def extract_block(body, name):
    """Pull out <!-- name --> ... <!-- /name --> and return (items, remaining_body).

    Items are parsed as a sequence of '### Title' headed sub-blocks, each
    item = {"title": ..., "body": "<markdown text under the heading>"}.
    """
    pattern = re.compile(
        r"<!--\s*" + re.escape(name) + r"\s*-->(.*?)<!--\s*/" + re.escape(name) + r"\s*-->",
        re.S,
    )
    m = pattern.search(body)
    if not m:
        return [], body
    block = m.group(1).strip("\n")
    remaining = body[: m.start()] + body[m.end():]
    items = []
    parts = re.split(r"(?m)^###\s+(.+)$", block)
    # parts = ['', title1, body1, title2, body2, ...]
    for idx in range(1, len(parts), 2):
        title = parts[idx].strip()
        item_body = parts[idx + 1].strip() if idx + 1 < len(parts) else ""
        items.append({"title": title, "body": item_body})
    return items, remaining


# --------------------------------------------------------------------------
# Minimal markdown -> HTML
# --------------------------------------------------------------------------

def _inline(text):
    """Apply inline markdown formatting to already-HTML-escaped text."""
    # images: ![alt](src)
    text = re.sub(
        r"!\[([^\]]*)\]\(([^)]+)\)",
        r'<img src="\2" alt="\1" loading="lazy">',
        text,
    )
    # links: [text](url)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2">\1</a>',
        text,
    )
    # inline code: `code`
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    # bold: **text**
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    # italic: *text*
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    return text


def markdown_to_html(md_text):
    md_text = md_text.strip("\n")
    if not md_text:
        return ""
    blocks = re.split(r"\n\s*\n", md_text)
    out = []
    for block in blocks:
        block = block.strip("\n")
        if not block.strip():
            continue
        lines = [l for l in block.split("\n")]

        # headings
        hm = re.match(r"^(#{1,3})\s+(.*)$", lines[0])
        if hm and len(lines) == 1:
            level = len(hm.group(1))
            content = _inline(html.escape(hm.group(2), quote=False))
            out.append(f"<h{level}>{content}</h{level}>")
            continue

        # unordered list
        if all(re.match(r"^\s*[-*]\s+", l) for l in lines if l.strip()):
            items = [re.sub(r"^\s*[-*]\s+", "", l) for l in lines if l.strip()]
            lis = "".join(f"<li>{_inline(html.escape(i, quote=False))}</li>" for i in items)
            out.append(f"<ul>{lis}</ul>")
            continue

        # ordered list
        if all(re.match(r"^\s*\d+\.\s+", l) for l in lines if l.strip()):
            items = [re.sub(r"^\s*\d+\.\s+", "", l) for l in lines if l.strip()]
            lis = "".join(f"<li>{_inline(html.escape(i, quote=False))}</li>" for i in items)
            out.append(f"<ol>{lis}</ol>")
            continue

        # image-only paragraph
        if re.match(r"^!\[[^\]]*\]\([^)]+\)$", block.strip()):
            out.append(f"<figure>{_inline(html.escape(block.strip(), quote=False))}</figure>")
            continue

        # paragraph (soft-wrap lines with a space)
        joined = " ".join(l.strip() for l in lines if l.strip())
        out.append(f"<p>{_inline(html.escape(joined, quote=False))}</p>")
    return "\n".join(out)


# --------------------------------------------------------------------------
# Shared page pieces
# --------------------------------------------------------------------------

def pillars_html(items):
    cards = []
    for it in items:
        body_html = markdown_to_html(it["body"])
        # unwrap a single <p> to keep the compact card typography
        body_html = re.sub(r"^<p>(.*)</p>$", r"\1", body_html, flags=re.S)
        cards.append(
            f'<div class="pillar"><h3>{html.escape(it["title"], quote=False)}</h3>'
            f'<p>{body_html}</p></div>'
        )
    return f'<div class="pillars">{"".join(cards)}</div>'


def tiers_html(items, win_all=False):
    rows = []
    for it in items:
        n, label = it["title"].split("::", 1) if "::" in it["title"] else ("", it["title"])
        body_html = markdown_to_html(it["body"])
        body_html = re.sub(r"^<p>(.*)</p>$", r"\1", body_html, flags=re.S)
        cls = "tier win" if win_all else "tier"
        rows.append(
            f'<div class="{cls}"><span class="n mono">{html.escape(n, quote=False)}</span>'
            f'<div><b>{html.escape(label, quote=False)}</b><span>{body_html}</span></div></div>'
        )
    return f'<div class="tiers">{"".join(rows)}</div>'


NOTE_HREF = SITE_ROOT + "notes/how-a-one-person-vfx-department-orchestrates-ai/"
NOTE_LABEL = "Note: orchestrating AI solo"


def related_section(items, eyebrow="Keep exploring"):
    """A compact cross-link strip so every page routes to the others.

    Reuses the home-page quicklinks styling (.quicklinks / .ql-row).
    items = list of (label, href). Discovery, not decoration: this is what
    lets a reader who lands on the course or a note find the tools, and back.
    """
    links = " &middot; ".join(
        f'<a href="{href}">{html.escape(label, quote=False)}</a>' for label, href in items
    )
    return f'''
<hr class="rule">

<section>
  <div class="wrap">
    <div class="quicklinks" style="margin-top:0">
      <span class="eyebrow">{html.escape(eyebrow, quote=False)}</span>
      <div class="ql-row">{links}</div>
    </div>
  </div>
</section>'''


def final_cta(h2, p, primary_label, primary_href, secondary_label, secondary_href, soon=None):
    soon_html = f'<span class="soon"><span class="dot"></span>{html.escape(soon, quote=False)}</span>' if soon else ""
    return f'''
<section id="get">
  <div class="wrap">
    <div class="final">
      {soon_html}
      <h2>{html.escape(h2, quote=False)}</h2>
      <p>{html.escape(p, quote=False)}</p>
      <div class="cta-row">
        <a class="btn btn-a" href="{primary_href}">{html.escape(primary_label, quote=False)}</a>
        <a class="btn btn-b" href="{secondary_href}">{html.escape(secondary_label, quote=False)}</a>
      </div>
    </div>
  </div>
</section>'''


# --------------------------------------------------------------------------
# Page renderers
# --------------------------------------------------------------------------

def write_feed(out_dir):
    """RSS 2.0 for content/notes/.

    WHY: the site had no feed at all. Without one, every note written for the content push only
    exists inside whatever platform it was posted to, which is precisely the asset that does NOT
    accrue to Geoff. A feed is how a note gets syndicated, subscribed to, and picked up by readers
    and aggregators he does not have to maintain a presence on.

    Deliberately hand-rolled rather than adding a dependency: the site builds with stdlib only.
    """
    from email.utils import format_datetime
    from datetime import datetime, timezone
    import xml.sax.saxutils as sx

    notes = []
    for md_path in sorted((CONTENT_DIR / "notes").glob("*.md")):
        fm, body = parse_frontmatter(md_path.read_text(encoding="utf-8"))
        if fm.get("draft", "").lower() == "true":
            continue
        slug = fm.get("slug", md_path.stem)
        try:
            d = datetime.fromisoformat(fm.get("date", "")).replace(tzinfo=timezone.utc)
        except ValueError:
            d = datetime.fromtimestamp(md_path.stat().st_mtime, tz=timezone.utc)
        notes.append((d, fm.get("title", slug), fm.get("description", ""), slug))
    notes.sort(reverse=True)

    base = SITE_CANONICAL.rstrip("/")
    items = []
    for d, title, desc, slug in notes[:30]:
        items.append(
            "    <item>\n"
            f"      <title>{sx.escape(title)}</title>\n"
            f"      <link>{base}/notes/{slug}/</link>\n"
            f"      <guid isPermaLink=\"true\">{base}/notes/{slug}/</guid>\n"
            f"      <pubDate>{format_datetime(d)}</pubDate>\n"
            f"      <description>{sx.escape(desc)}</description>\n"
            "    </item>")
    now = format_datetime(datetime.now(timezone.utc))
    (out_dir / "feed.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        f"    <title>{sx.escape(SITE_NAME)}</title>\n"
        f"    <link>{base}/</link>\n"
        "    <description>Notes on VFX supervision, breakdowns, budgets and pipeline.</description>\n"
        "    <language>en</language>\n"
        f"    <lastBuildDate>{now}</lastBuildDate>\n"
        f'    <atom:link href="{base}/feed.xml" rel="self" type="application/rss+xml"/>\n'
        + "\n".join(items) + "\n"
        "  </channel>\n</rss>\n", encoding="utf-8")
    print(f"  wrote feed.xml ({len(notes)} notes)")


def write_sitemap(paths, out_dir):
    """sitemap.xml + robots.txt. Both were 404 before 2026-08-04."""
    from datetime import date
    today = date.today().isoformat()
    urls = "\n".join(
        f"  <url><loc>{SITE_CANONICAL.rstrip('/')}/{p.lstrip('/')}</loc><lastmod>{today}</lastmod></url>"
        for p in paths)
    (out_dir / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n", encoding="utf-8")
    (out_dir / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE_CANONICAL.rstrip('/')}/sitemap.xml\n", encoding="utf-8")
    print("    wrote sitemap.xml + robots.txt")


SITE_CANONICAL = "https://thevfxsupervisor.com"  # cut over 2026-08-06; github.io now 301s here


def render_shell(title, description, content_html, nav_active=None, extra_script="", canonical_path=""):
    html_out = BASE_TEMPLATE
    html_out = html_out.replace("{{TITLE}}", html.escape(title, quote=False))
    html_out = html_out.replace("{{DESCRIPTION}}", html.escape(description, quote=False))
    html_out = html_out.replace("{{ROOT}}", SITE_ROOT)
    html_out = html_out.replace("{{CSSVER}}", CSS_VERSION)
    html_out = html_out.replace("{{SITE}}", SITE_CANONICAL.rstrip("/"))
    html_out = html_out.replace("{{CANONICAL}}", SITE_CANONICAL.rstrip("/") + "/" + canonical_path.lstrip("/"))
    for key in ("projects", "course", "notes", "about"):
        cls = " current" if key == nav_active else ""
        html_out = html_out.replace("{{NAV_%s}}" % key.upper(), cls)
    html_out = html_out.replace("{{EXTRA_SCRIPT}}", extra_script)
    html_out = html_out.replace("{{CONTENT}}", content_html)
    return html_out


def render_home():
    fm, body = parse_frontmatter((CONTENT_DIR / "pages" / "home.md").read_text(encoding="utf-8"))
    pillars, body = extract_block(body, "pillars")

    h1 = html.escape(fm["hero_h1"], quote=False)
    accent = fm.get("hero_h1_accent", "")
    if accent:
        h1 = h1.replace(html.escape(accent, quote=False), f"<span>{html.escape(accent, quote=False)}</span>")

    # Projects & links, promoted from a text row to prominent cards. Each project's tagline is its
    # own card_summary, so the deep-dive copy stays in one place.
    cards = []
    for i, slug in enumerate(PROJECT_ORDER):   # flagship first: breakdown-studio, link-session
        p = CONTENT_DIR / "projects" / f"{slug}.md"
        if not p.exists():
            continue
        pfm, _ = parse_frontmatter(p.read_text(encoding="utf-8"))
        cls = "proj-card flagship" if i == 0 else "proj-card"
        cards.append(
            f'<a class="{cls}" href="{SITE_ROOT}projects/{slug}/">'
            f'<span class="eyebrow">{html.escape(pfm.get("card_eyebrow", pfm.get("eyebrow","Case study")), quote=False)}</span>'
            f'<h2>{html.escape(pfm.get("card_title", pfm.get("h1","")), quote=False)}</h2>'
            f'<p>{html.escape(pfm.get("card_summary", pfm.get("description","")), quote=False)}</p>'
            f'<span class="proj-more mono">Read the case study &rarr;</span></a>'
        )
    cards.append(
        f'<a class="proj-card" href="{SITE_ROOT}course/">'
        f'<span class="eyebrow">Course &middot; free waitlist</span>'
        f'<h2>A course teaching the method</h2>'
        f'<p>Break down and budget a whole film solo, with an AI pair doing the grunt work. Founding cohort 325 USD.</p>'
        f'<span class="proj-more mono">See the course &rarr;</span></a>'
    )
    cards.append(
        f'<a class="proj-card" href="{SITE_ROOT}about/">'
        f'<span class="eyebrow">About &middot; 25 years</span>'
        f'<h2>Twenty five years, and a VES Award</h2>'
        f'<p>VFX for Eastwood, the Wachowskis and Affleck: Changeling (VES Award), J. Edgar, Invictus, Argo, Cloud Atlas. Work for Netflix, Pandora, LEGO, Sony. Copenhagen.</p>'
        f'<span class="proj-more mono">More about me &rarr;</span></a>'
    )
    cards_html = "".join(cards)

    utility = [
        ("Notes", SITE_ROOT + "notes/"),
        ("GitHub", "https://github.com/thevfxsupervisor"),
        ("Contact", "mailto:geoff@wanglemedia.com"),
    ]
    util_html = " &middot; ".join(f'<a href="{href}">{label}</a>' for label, href in utility)

    proof_h2 = fm.get("proof_h2", "").strip()
    proof_head = f'<div class="sec-head"><h2>{html.escape(proof_h2, quote=False)}</h2></div>' if proof_h2 else ""

    content = f'''
<section class="hero">
  <div class="wrap">
    <span class="eyebrow">{html.escape(fm.get("hero_eyebrow",""), quote=False)}</span>
    <h1 style="margin-top:18px">{h1}</h1>
    <p class="lede">{html.escape(fm.get("hero_lede",""), quote=False)}</p>
    <div class="cta-row">
      <a class="btn btn-a" href="{fm.get("cta_primary_href","")}">{html.escape(fm.get("cta_primary_label",""), quote=False)}</a>
      <a class="btn btn-b" href="{fm.get("cta_secondary_href","")}">{html.escape(fm.get("cta_secondary_label",""), quote=False)}</a>
    </div>
    <div class="cred"><span class="dot"></span><b>{html.escape(fm.get("cred",""), quote=False)}</b></div>
  </div>
</section>

<section id="projects-links">
  <div class="wrap">
    <span class="eyebrow">Projects &amp; links</span>
    <div class="proj-grid">{cards_html}</div>
    <div class="ql-row" style="margin-top:22px">{util_html}</div>
  </div>
</section>
'''
    content += final_cta(
        fm.get("final_h2", "Get the launch notice"),
        fm.get("final_p", ""),
        fm.get("final_primary_label", "See Breakdown Studio"),
        fm.get("final_primary_href", SITE_ROOT + "projects/breakdown-studio/"),
        fm.get("final_secondary_label", "Join the waitlist"),
        fm.get("final_secondary_href", SITE_ROOT + "course/"),
    )
    return render_shell(fm.get("title", SITE_NAME), fm.get("description", ""), content, nav_active=None, canonical_path="")


PROJECT_ORDER = ["breakdown-studio", "link-session"]  # flagship first


def render_project(md_path):
    """Generic case-study page for anything under content/projects/."""
    fm, body = parse_frontmatter(md_path.read_text(encoding="utf-8"))
    stats, body = extract_block(body, "stats")
    prose_html = markdown_to_html(body)
    slug = fm.get("slug", md_path.stem)

    ctas = []
    if fm.get("get_href"):
        ctas.append(f'<a class="btn btn-a" href="{fm["get_href"]}">{html.escape(fm.get("get_label","Get the tool"), quote=False)}</a>')
    ctas.append(f'<a class="btn btn-b" href="{SITE_ROOT}about/">Work with me</a>')
    cta_row = f'<div class="cta-row">{"".join(ctas)}</div>'

    stats_section = ""
    if stats:
        stats_section = f'''
<hr class="rule">

<section id="proof">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Validated, not vibes</span>
      <h2>{html.escape(fm.get("stats_h2","The numbers"), quote=False)}</h2></div>
    <div style="margin-top:26px;max-width:820px">{tiers_html(stats, win_all=True)}</div>
  </div>
</section>
'''

    content = f'''
<section class="hero">
  <div class="wrap">
    <span class="eyebrow">{html.escape(fm.get("eyebrow","Case study"), quote=False)}</span>
    <h1 style="margin-top:18px">{html.escape(fm["h1"], quote=False)}</h1>
    <p class="lede">{html.escape(fm.get("lede",""), quote=False)}</p>
    {cta_row}
    <div class="cred"><span class="dot"></span><b>{html.escape(fm.get("cred",""), quote=False)}</b></div>
  </div>
</section>

<hr class="rule">

<section>
  <div class="wrap prose">
    {prose_html}
  </div>
</section>
{stats_section}'''
    content += final_cta(
        fm.get("final_h2", "Work with me"),
        fm.get("final_p", ""),
        fm.get("final_primary_label", "Get in touch"),
        fm.get("final_primary_href", SITE_ROOT + "about/"),
        fm.get("final_secondary_label", "Join the waitlist"),
        fm.get("final_secondary_href", SITE_ROOT + "course/"),
        soon=fm.get("soon"),
    )
    # Cross-links: the sibling project, the course, the note, the projects index.
    rel = []
    for sib in PROJECT_ORDER:
        if sib == slug:
            continue
        sp = CONTENT_DIR / "projects" / f"{sib}.md"
        if sp.exists():
            sfm, _ = parse_frontmatter(sp.read_text(encoding="utf-8"))
            rel.append((sfm.get("card_title", sib), f"{SITE_ROOT}projects/{sib}/"))
    rel += [
        ("The course", SITE_ROOT + "course/"),
        (NOTE_LABEL, NOTE_HREF),
        ("All projects", SITE_ROOT + "projects/"),
    ]
    content += related_section(rel)
    return render_shell(fm.get("title", ""), fm.get("description", ""), content, nav_active="projects", canonical_path="projects/"+slug+"/"), slug


def render_projects():
    """The /projects/ index: flagship-first case-study cards."""
    cards = []
    for i, slug in enumerate(PROJECT_ORDER):
        p = CONTENT_DIR / "projects" / f"{slug}.md"
        if not p.exists():
            continue
        fm, _ = parse_frontmatter(p.read_text(encoding="utf-8"))
        cls = "proj-card flagship" if i == 0 else "proj-card"
        eyebrow = fm.get("card_eyebrow", fm.get("eyebrow", "Case study"))
        title = fm.get("card_title", fm.get("h1", ""))
        summary = fm.get("card_summary", fm.get("description", ""))
        cards.append(
            f'<a class="{cls}" href="{SITE_ROOT}projects/{slug}/">'
            f'<span class="eyebrow">{html.escape(eyebrow, quote=False)}</span>'
            f'<h2>{html.escape(title, quote=False)}</h2>'
            f'<p>{html.escape(summary, quote=False)}</p>'
            f'<span class="proj-more mono">Read the case study &rarr;</span></a>'
        )
    content = f'''
<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Projects</span>
    <h1 style="margin-top:18px">Tools I built on real productions, then open-sourced</h1>
    <p class="lede">I build the tooling a one-person VFX department needs to survive a real film, then release it. Here is what has shipped.</p>
    <div class="proj-grid">{''.join(cards)}</div>
  </div>
</section>
'''
    content += final_cta(
        "Want this kind of tooling on your show?",
        "I build and run AI-assisted VFX pipelines on real productions. If that is useful to your film, let's talk. Or book the course for the method behind the tools.",
        "Work with me", SITE_ROOT + "about/",
        "Join the waitlist", SITE_ROOT + "course/",
    )
    content += related_section(
        [
            (NOTE_LABEL, NOTE_HREF),
            ("The course", SITE_ROOT + "course/"),
            ("About", SITE_ROOT + "about/"),
        ],
        eyebrow="More on the method",
    )
    return render_shell("Projects | the vfx supervisor", "The tools I built running a feature's VFX department solo, then open-sourced: Breakdown Studio and link-session.", content, nav_active="projects", canonical_path="projects/")


def render_course():
    fm, raw_body = parse_frontmatter((CONTENT_DIR / "pages" / "course.md").read_text(encoding="utf-8"))
    included, _ = extract_block(raw_body, "included")
    # Render the method section IN PLACE (at the <!-- included --> marker), so the copy above the
    # marker ("Who it is for", the FAQ, "What it is") stays ABOVE the method, and "What you leave
    # with" etc. stay below it. Previously the method was pulled to the top of the page.
    _before, _s1, _tail = raw_body.partition("<!-- included -->")
    _blk, _s2, _after = _tail.partition("<!-- /included -->")
    prose_before = markdown_to_html(_before)
    prose_after = markdown_to_html(_after)
    prose_before_sec = f'<section><div class="wrap prose">{prose_before}</div></section>' if _before.strip() else ""
    prose_after_sec = f'<section><div class="wrap prose">{prose_after}</div></section>' if _after.strip() else ""

    included_html = ""
    if included:
        rows = "".join(
            f'<div class="method-item">'
            f'<h3 class="method-title">{html.escape(it["title"], quote=False)}</h3>'
            f'<p class="method-desc">{markdown_to_html(it["body"]).replace("<p>","").replace("</p>","")}</p>'
            f'</div>'
            for it in included
        )
        included_html = f'''
<section>
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">What the course covers</span>
      <h2>{html.escape(fm.get("included_h2","The method, end to end"), quote=False)}</h2></div>
    <div class="method-list">{rows}</div>
  </div>
</section>
<hr class="rule">'''

    waitlist_endpoint = fm.get("waitlist_endpoint", "")
    contact_email = fm.get("contact_email", "geoff@wanglemedia.com")
    # Paste a Stripe Payment Link into buy_url: in course.md and the page switches from "reserve
    # and I will invoice you" to a real Buy button. Until then the invoice path stands, so the page
    # is never in a state where a decided buyer cannot act.
    buy_url = fm.get("buy_url", "").strip()
    if buy_url:
        buy_block = (
            '<div class="cta-row" style="margin-top:28px">'
            f'<a class="btn btn-a" href="{buy_url}">Book a seat</a>'
            '</div>'
            '<p class="tiny" style="margin-top:14px">Card or invoice at checkout, with a VAT invoice'
            ' issued automatically. Prefer to be invoiced directly? Use the form below.</p>'
        )
    else:
        buy_block = ''

    seats_note = fm.get("seats_note", "")
    hero_cta = fm.get("hero_cta", "Join the free waitlist")
    reassure = (html.escape(seats_note, quote=False) + " ") if seats_note else ""
    # Selected-credits carousel (replaces the old static cred-band). Verified 2026-08-15 with Geoff,
    # IMDb (nm0995883) and web-confirmed directors. ONLY his confirmed supervisor/producer credits.
    # Permafrost is deliberately OMITTED until publicly announced (NDA). Do not add unverified credits.
    _CREDITS = [
        ("Changeling", "Clint Eastwood", "VFX Supervisor"),
        ("Vantage Point", "Pete Travis", "VFX Supervisor"),
        ("Invictus", "Clint Eastwood", "VFX Supervisor"),
        ("J. Edgar", "Clint Eastwood", "VFX Supervisor"),
        ("Argo", "Ben Affleck", "VFX Supervisor"),
        ("Cloud Atlas", "The Wachowskis", "VFX Supervisor"),
        ("Red Dawn", "Dan Bradley", "VFX Supervisor"),
        ("Skammerens datter II", "Ask Hasselbalch", "VFX Supervisor"),
        ("Atlantic Crossing", "Alexander Eik", "VFX Supervisor & Producer"),
        ("Barzakh", "Asim Abbasi", "VFX Producer"),
    ]
    _cards = "".join(
        f'<div class="credit-item"><span class="film">{html.escape(f, quote=False)}</span>'
        f'<span class="dir">{html.escape(d, quote=False)}</span>'
        f'<span class="role">{html.escape(r, quote=False)}</span></div>'
        for f, d, r in _CREDITS)
    cred_html = ('<div class="credit-carousel" aria-label="Selected credits">'
                 f'<div class="credit-track">{_cards}{_cards}</div></div>')

    content = f'''
<section class="hero course-hero">
  <div class="wrap">
    <span class="eyebrow">{html.escape(fm.get("eyebrow","Course"), quote=False)}</span>
    <h1 style="margin-top:18px">{html.escape(fm["h1"], quote=False)}</h1>
    <p class="lede">{html.escape(fm.get("lede",""), quote=False)}</p>
    {cred_html}
    <form class="form-card waitlist-form hero-form" style="margin-top:30px">
      <div class="hero-form-row">
        <input type="email" name="email" required autocomplete="email" placeholder="Your email" aria-label="Your email">
        <button type="submit" class="btn btn-a">{html.escape(hero_cta, quote=False)} &rarr;</button>
      </div>
      <div class="wl-status"></div>
      <p class="tiny" style="margin-top:12px">{reassure}No spam, unsubscribe anytime.</p>
    </form>
  </div>
</section>

<hr class="rule">
{prose_before_sec}
{included_html}
{prose_after_sec}

<hr class="rule">

<section id="waitlist">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Free waitlist &middot; The next date first</span>
      <h2>Join the free waitlist</h2>
      <p class="k">No date is set yet, and this is how you hear the next one. Join and I email you my
        "Shoots You in the Foot" list straight away: the VFX and generative-AI gotchas worth knowing
        before your next bid. Ask me a question below and I may reply. No spam.</p></div>

      {buy_block}
    <form class="form-card waitlist-form" style="margin-top:28px">
      <div class="field"><label for="wl-name">Name (optional)</label><input type="text" id="wl-name" name="name" autocomplete="name"></div>
      <div class="field"><label for="wl-email">Email</label><input type="email" id="wl-email" name="email" required autocomplete="email"></div>
      <div class="field"><label for="wl-note">Ask me a question (optional)</label>
        <textarea id="wl-note" name="note" placeholder="Anything about breaking down, budgeting or bidding VFX, or using AI on a show"></textarea></div>
      <button type="submit" class="btn btn-a">Join the waitlist</button>
      <div class="wl-status"></div>
      <p class="tiny">Your email is used to send you the gotchas list and the next course date. Nothing else. Unsubscribe anytime.</p>
    </form>
  </div>
</section>
'''
    content += related_section(
        [
            ("Breakdown Studio", SITE_ROOT + "projects/breakdown-studio/"),
            ("link-session", SITE_ROOT + "projects/link-session/"),
            (NOTE_LABEL, NOTE_HREF),
            ("Work with me", SITE_ROOT + "about/"),
        ],
        eyebrow="The tools and writing behind the method",
    )
    extra_script = f'''
<script>
const WAITLIST_ENDPOINT = "{waitlist_endpoint}"; // set after deploying waitlist.gs (see WAITLIST_SETUP.md)
(function(){{
  var CONTACT_EMAIL = "{contact_email}";
  var forms = document.querySelectorAll('.waitlist-form');
  Array.prototype.forEach.call(forms, function(form){{
    var status = form.querySelector('.wl-status');
    var submit = form.querySelector('[type=submit]');

    function setStatus(msg, cls){{
      if (!status) return;
      status.textContent = msg;
      status.className = 'wl-status ' + (cls || '');
    }}
    function val(sel){{ var el = form.querySelector(sel); return el ? el.value.trim() : ''; }}

    form.addEventListener('submit', function(e){{
      e.preventDefault();
      var email = val('[name=email]');
      var name = val('[name=name]');
      var note = val('[name=note]');
      if (!email) return;

      if (!WAITLIST_ENDPOINT) {{
        var subject = encodeURIComponent('Join the waitlist');
        var bodyLines = ['Email: ' + email];
        if (name) bodyLines.push('Name: ' + name);
        if (note) bodyLines.push('Question: ' + note);
        var mailto = 'mailto:' + CONTACT_EMAIL + '?subject=' + subject + '&body=' + encodeURIComponent(bodyLines.join('\\n'));
        if (status) {{
          status.className = 'wl-status ok';
          status.innerHTML = 'Almost there: send the email that just opened and you are on the list.'
            + '<br><span class="tiny">Nothing happened? <a href="' + mailto + '">Click here</a>'
            + ' or email <a href="mailto:' + CONTACT_EMAIL + '">' + CONTACT_EMAIL + '</a>'
            + ' with the subject "Join the waitlist".</span>';
        }}
        window.location.href = mailto;
        return;
      }}

      if (submit) submit.disabled = true;
      setStatus('Sending...', 'info');
      fetch(WAITLIST_ENDPOINT, {{
        method: 'POST',
        headers: {{'Content-Type': 'text/plain;charset=utf-8'}},
        body: JSON.stringify({{email: email, name: name, note: note}})
      }})
        .then(function(r){{ return r.json(); }})
        .then(function(data){{
          if (data && data.ok) {{
            setStatus("You're on the list. Check your inbox, the gotchas list is on its way.", 'ok');
            form.reset();
          }} else {{
            throw new Error('bad response');
          }}
        }})
        .catch(function(){{
          setStatus('Something went wrong. Emailing you instead: ', 'err');
          window.location.href = 'mailto:' + CONTACT_EMAIL + '?subject=' + encodeURIComponent('Join the waitlist') + '&body=' + encodeURIComponent('Email: ' + email + (name ? ('\\nName: ' + name) : '') + (note ? ('\\nQuestion: ' + note) : ''));
        }})
        .finally(function(){{ if (submit) submit.disabled = false; }});
    }});
  }});
}})();
</script>'''
    # Credit carousel behaviour:
    #  1) shuffle per visit so people do not always see the same first few credits (track holds the
    #     10 cards twice for the seamless loop; shuffle the originals, then re-clone both halves);
    #  2) JS-drive the slide with a gentle base loop PLUS a scroll-velocity boost that decays, so
    #     scrolling makes it slide faster and stopping eases it back to the loop. The scroll listener
    #     is passive and never calls preventDefault, so the PAGE scroll is never hijacked/pinned.
    #     prefers-reduced-motion users get the CSS static fallback and none of this runs.
    extra_script += """
<script>
(function(){
  var track=document.querySelector('.credit-track'); if(!track) return;
  var kids=Array.prototype.slice.call(track.children); var n=Math.floor(kids.length/2);
  var orig=kids.slice(0,n);
  for(var i=orig.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=orig[i];orig[i]=orig[j];orig[j]=t;}
  track.textContent='';
  for(var k=0;k<orig.length;k++){track.appendChild(orig[k]);}
  for(var m=0;m<orig.length;m++){track.appendChild(orig[m].cloneNode(true));}
  if(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  track.style.animation='none';
  var pos=0, boost=0, half=0, lastY=(window.pageYOffset||0), lastT=0;
  window.addEventListener('scroll', function(){
    var y=(window.pageYOffset||0); boost+=Math.abs(y-lastY)*0.006; lastY=y;
    if(boost>1.4){ boost=1.4; }
  }, {passive:true});
  function frame(now){
    if(!lastT){ lastT=now; }
    var dt=Math.min(60, now-lastT); lastT=now;
    if(!half){ half=track.scrollWidth/2; }
    var base = half ? half/70000 : 0.04;
    pos += (base+boost)*dt;
    boost *= Math.pow(0.92, dt/16); if(boost<0.001){ boost=0; }
    if(half){ while(pos>=half){ pos-=half; } }
    track.style.transform='translateX('+(-pos)+'px)';
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
</script>"""
    return render_shell(fm.get("title", ""), fm.get("description", ""), content, nav_active="course", extra_script=extra_script, canonical_path="course/")


def render_about():
    fm, body = parse_frontmatter((CONTENT_DIR / "pages" / "about.md").read_text(encoding="utf-8"))
    prose_html = markdown_to_html(body)
    content = f'''
<section class="hero">
  <div class="wrap">
    <span class="eyebrow">{html.escape(fm.get("eyebrow","About"), quote=False)}</span>
    <h1 style="margin-top:18px">{html.escape(fm["h1"], quote=False)}</h1>
  </div>
</section>
<hr class="rule">
<section>
  <div class="wrap prose">
    {prose_html}
  </div>
</section>
'''
    content += final_cta(
        "Get in touch",
        fm.get("final_p", "Questions, collaborations, or just say hello."),
        "Email",
        f'mailto:{fm.get("contact_email","geoff@wanglemedia.com")}',
        "See Breakdown Studio",
        SITE_ROOT + "projects/breakdown-studio/",
    )
    content += related_section(
        [
            ("Breakdown Studio", SITE_ROOT + "projects/breakdown-studio/"),
            ("link-session", SITE_ROOT + "projects/link-session/"),
            ("The course", SITE_ROOT + "course/"),
            ("Notes", SITE_ROOT + "notes/"),
        ]
    )
    return render_shell(fm.get("title", ""), fm.get("description", ""), content, nav_active="about", canonical_path="about/")


def render_notes():
    note_files = sorted((CONTENT_DIR / "notes").glob("*.md"))
    posts = []
    for f in note_files:
        fm, _ = parse_frontmatter(f.read_text(encoding="utf-8"))
        if fm.get("draft", "").lower() == "true":
            continue
        posts.append((fm, f.stem))
    posts.sort(key=lambda p: p[0].get("date", ""), reverse=True)

    rows = []
    for fm, slug in posts:
        rows.append(
            f'<a class="postrow" href="{SITE_ROOT}notes/{slug}/">'
            f'<div><h3>{html.escape(fm.get("title",""), quote=False)}</h3>'
            f'<p>{html.escape(fm.get("description",""), quote=False)}</p></div>'
            f'<span class="d mono">{html.escape(fm.get("date",""), quote=False)}</span></a>'
        )
    content = f'''
<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Notes</span>
    <h1 style="margin-top:18px">Writing on pipeline, production, and orchestrating AI</h1>
    <p class="lede">Short, practical notes from running a one-person VFX department. No client names,
      no show names, ever.</p>
    <div class="postlist">{''.join(rows)}</div>
  </div>
</section>
'''
    content += related_section(
        [
            ("Breakdown Studio", SITE_ROOT + "projects/breakdown-studio/"),
            ("link-session", SITE_ROOT + "projects/link-session/"),
            ("The course", SITE_ROOT + "course/"),
        ],
        eyebrow="The tools behind the writing",
    )
    return render_shell("Notes | the vfx supervisor", "Notes on pipeline, production and orchestrating AI, from a working VFX supervisor and producer.", content, nav_active="notes", canonical_path="notes/")


def render_note(md_path):
    fm, body = parse_frontmatter(md_path.read_text(encoding="utf-8"))
    prose_html = markdown_to_html(body)
    content = f'''
<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Notes &middot; {html.escape(fm.get("date",""), quote=False)}</span>
    <h1 style="margin-top:18px">{html.escape(fm.get("title",""), quote=False)}</h1>
  </div>
</section>
<hr class="rule">
<section>
  <div class="wrap prose">
    {prose_html}
  </div>
</section>
<section>
  <div class="wrap">
    <a class="btn btn-b" href="{SITE_ROOT}notes/">&larr; All notes</a>
  </div>
</section>
'''
    content += related_section(
        [
            ("Breakdown Studio", SITE_ROOT + "projects/breakdown-studio/"),
            ("link-session", SITE_ROOT + "projects/link-session/"),
            ("The course", SITE_ROOT + "course/"),
        ],
        eyebrow="The tools this method runs on",
    )
    _slug = fm.get("slug", md_path.stem)
    return render_shell(fm.get("title", ""), fm.get("description", ""), content, nav_active="notes", canonical_path="notes/"+_slug+"/"), _slug


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------

def write_page(rel_dir, html_out):
    out_dir = DOCS_DIR / rel_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(html_out, encoding="utf-8")
    print(f"  wrote docs/{rel_dir}/index.html" if rel_dir else "  wrote docs/index.html")


def main():
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir(parents=True)

    print("Building thevfxsupervisor.com ...")

    write_page("", render_home())
    for md_path in sorted((CONTENT_DIR / "projects").glob("*.md")):
        proj_html, slug = render_project(md_path)
        write_page(f"projects/{slug}", proj_html)
    write_page("projects", render_projects())
    write_page("course", render_course())
    write_page("about", render_about())
    write_page("notes", render_notes())

    for md_path in sorted((CONTENT_DIR / "notes").glob("*.md")):
        fm, _ = parse_frontmatter(md_path.read_text(encoding="utf-8"))
        if fm.get("draft", "").lower() == "true":
            continue
        note_html, slug = render_note(md_path)
        write_page(f"notes/{slug}", note_html)

    write_feed(DOCS_DIR)

    # static assets
    static_out = DOCS_DIR / "static"
    static_out.mkdir(parents=True, exist_ok=True)
    for f in STATIC_DIR.glob("*"):
        if f.is_file():
            shutil.copy2(f, static_out / f.name)
            print(f"  copied static/{f.name}")

    # CNAME for a GitHub Pages custom domain. DISABLED: thevfxsupervisor.com is NOT cut
    # over (parked at easyDNS). Emitting docs/CNAME makes Pages auto-set the custom domain,
    # which 301-redirects github.io into the parked lander = site DOWN. Set True ONLY after
    # the DNS cutover is real (see dev/MAINTAINING.md). .gitignore also excludes docs/CNAME.
    CUTOVER_DONE = True  # cut over 2026-08-06. build.py MUST keep emitting docs/CNAME: it wipes docs/ each build, and GitHub drops the custom domain if the file disappears.
    if CUTOVER_DONE:
        (DOCS_DIR / "CNAME").write_text(DOMAIN + "\n", encoding="utf-8")
        print(f"  wrote docs/CNAME ({DOMAIN})")

    # .nojekyll so Pages serves the docs/ tree as-is (no Jekyll processing)
    (DOCS_DIR / ".nojekyll").write_text("", encoding="utf-8")
    print("  wrote docs/.nojekyll")

    write_sitemap(["", "projects/", "course/", "notes/", "about/"], DOCS_DIR)
    print("Done.")


if __name__ == "__main__":
    main()
