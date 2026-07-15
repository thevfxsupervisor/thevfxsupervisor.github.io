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

def render_shell(title, description, content_html, nav_active=None, extra_script=""):
    html_out = BASE_TEMPLATE
    html_out = html_out.replace("{{TITLE}}", html.escape(title, quote=False))
    html_out = html_out.replace("{{DESCRIPTION}}", html.escape(description, quote=False))
    html_out = html_out.replace("{{ROOT}}", SITE_ROOT)
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

    quicklinks = [
        ("Breakdown Studio", SITE_ROOT + "projects/breakdown-studio/"),
        ("Course waitlist", SITE_ROOT + "course/"),
        ("Notes", SITE_ROOT + "notes/"),
        ("GitHub", "https://github.com/thevfxsupervisor"),
        ("Contact", "mailto:geoff@thevfxsupervisor.com"),
    ]
    ql_html = " &middot; ".join(f'<a href="{href}">{label}</a>' for label, href in quicklinks)

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
    <div class="cred mono" style="margin-top:6px">{ql_html}</div>
  </div>
</section>

<hr class="rule">

<section id="proof">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Proof, not promises</span>
      <h2>{html.escape(fm.get("proof_h2","What the work has actually done"), quote=False)}</h2></div>
    {pillars_html(pillars)}
  </div>
</section>
'''
    content += final_cta(
        fm.get("final_h2", "Get the launch notice"),
        fm.get("final_p", ""),
        fm.get("final_primary_label", "See Breakdown Studio"),
        fm.get("final_primary_href", SITE_ROOT + "projects/breakdown-studio/"),
        fm.get("final_secondary_label", "Join the course waitlist"),
        fm.get("final_secondary_href", SITE_ROOT + "course/"),
    )
    return render_shell(fm.get("title", SITE_NAME), fm.get("description", ""), content, nav_active=None)


def render_breakdown_studio():
    fm, body = parse_frontmatter((CONTENT_DIR / "projects" / "breakdown-studio.md").read_text(encoding="utf-8"))
    stats, body = extract_block(body, "stats")
    prose_html = markdown_to_html(body)

    content = f'''
<section class="hero">
  <div class="wrap">
    <span class="eyebrow">{html.escape(fm.get("eyebrow","Project launch"), quote=False)}</span>
    <h1 style="margin-top:18px">{html.escape(fm["h1"], quote=False)}</h1>
    <p class="lede">{html.escape(fm.get("lede",""), quote=False)}</p>
    <div class="cta-row">
      <a class="btn btn-a" href="{fm.get("live_url","")}">Open Breakdown Studio</a>
      <a class="btn btn-b" href="{fm.get("repo_url","")}">Source on GitHub</a>
      <a class="btn btn-b" href="{fm.get("release_url","")}">v1.0.0 release</a>
    </div>
    <div class="cred"><span class="dot"></span><b>{html.escape(fm.get("cred",""), quote=False)}</b></div>
  </div>
</section>

<hr class="rule">

<section>
  <div class="wrap prose">
    {prose_html}
  </div>
</section>

<hr class="rule">

<section id="proof">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Validated, not vibes</span>
      <h2>{html.escape(fm.get("stats_h2","The numbers"), quote=False)}</h2></div>
    <div style="margin-top:26px;max-width:820px">{tiers_html(stats, win_all=True)}</div>
  </div>
</section>
'''
    content += final_cta(
        fm.get("final_h2", "Star it, and follow along"),
        fm.get("final_p", ""),
        "Star on GitHub",
        fm.get("repo_url", ""),
        "Back to the waitlist",
        SITE_ROOT + "course/",
        soon=fm.get("soon", "Open source · MIT · on GitHub"),
    )
    return render_shell(fm.get("title", ""), fm.get("description", ""), content, nav_active="projects")


def render_course():
    fm, body = parse_frontmatter((CONTENT_DIR / "pages" / "course.md").read_text(encoding="utf-8"))
    included, body = extract_block(body, "included")
    prose_html = markdown_to_html(body)

    included_html = ""
    if included:
        rows = "".join(
            f'<li>{html.escape(it["title"], quote=False)}'
            f'<br><span style="color:var(--dim);font-size:13.5px">{markdown_to_html(it["body"]).replace("<p>","").replace("</p>","")}</span></li>'
            for it in included
        )
        included_html = f'''
<section>
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">What the course covers</span>
      <h2>{html.escape(fm.get("included_h2","The method, end to end"), quote=False)}</h2></div>
    <div class="rd now" style="margin-top:26px;max-width:820px"><ul style="list-style:none;padding:0;display:grid;gap:14px">{rows}</ul></div>
  </div>
</section>
<hr class="rule">'''

    waitlist_endpoint = fm.get("waitlist_endpoint", "")
    contact_email = fm.get("contact_email", "geoff@thevfxsupervisor.com")

    content = f'''
<section class="hero">
  <div class="wrap">
    <span class="eyebrow">{html.escape(fm.get("eyebrow","Course · waitlist open"), quote=False)}</span>
    <h1 style="margin-top:18px">{html.escape(fm["h1"], quote=False)}</h1>
    <p class="lede">{html.escape(fm.get("lede",""), quote=False)}</p>
  </div>
</section>

<hr class="rule">
{included_html}
<section>
  <div class="wrap prose">
    {prose_html}
  </div>
</section>

<hr class="rule">

<section id="waitlist">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">No pricing yet, no course yet</span>
      <h2>Join the waitlist</h2>
      <p class="k">Leave your email and I will send one note when enrollment opens. No spam, no drip
        sequence, one message when it is real.</p></div>

    <form class="form-card" id="waitlist-form" style="margin-top:28px">
      <div class="field"><label for="wl-name">Name (optional)</label><input type="text" id="wl-name" name="name" autocomplete="name"></div>
      <div class="field"><label for="wl-email">Email</label><input type="email" id="wl-email" name="email" required autocomplete="email"></div>
      <div class="field"><label for="wl-note">What film are you breaking down? (optional)</label>
        <textarea id="wl-note" name="note" placeholder="e.g. an indie feature, a short, a series pilot"></textarea></div>
      <button type="submit" class="btn btn-a" id="wl-submit">Join the waitlist</button>
      <div id="wl-status"></div>
      <p class="tiny">Your email is used only to send the one launch note. Nothing else.</p>
    </form>
  </div>
</section>
'''
    extra_script = f'''
<script>
const WAITLIST_ENDPOINT = "{waitlist_endpoint}"; // set after deploying waitlist.gs (see WAITLIST_SETUP.md)
(function(){{
  var form = document.getElementById('waitlist-form');
  var status = document.getElementById('wl-status');
  var submit = document.getElementById('wl-submit');
  var CONTACT_EMAIL = "{contact_email}";

  function setStatus(msg, cls){{
    status.textContent = msg;
    status.className = cls || '';
  }}

  form.addEventListener('submit', function(e){{
    e.preventDefault();
    var email = document.getElementById('wl-email').value.trim();
    var name = document.getElementById('wl-name').value.trim();
    var note = document.getElementById('wl-note').value.trim();
    if (!email) return;

    if (!WAITLIST_ENDPOINT) {{
      var subject = encodeURIComponent('Course waitlist');
      var bodyLines = ['Email: ' + email];
      if (name) bodyLines.push('Name: ' + name);
      if (note) bodyLines.push('Film: ' + note);
      var mailto = 'mailto:' + CONTACT_EMAIL + '?subject=' + subject + '&body=' + encodeURIComponent(bodyLines.join('\\n'));
      setStatus('Waitlist form is not wired up yet. Opening an email instead.', 'info');
      window.location.href = mailto;
      return;
    }}

    submit.disabled = true;
    setStatus('Sending...', 'info');
    fetch(WAITLIST_ENDPOINT, {{
      method: 'POST',
      headers: {{'Content-Type': 'text/plain;charset=utf-8'}},
      body: JSON.stringify({{email: email, name: name, note: note}})
    }})
      .then(function(r){{ return r.json(); }})
      .then(function(data){{
        if (data && data.ok) {{
          setStatus("You're on the list. I'll send one note when it launches.", 'ok');
          form.reset();
        }} else {{
          throw new Error('bad response');
        }}
      }})
      .catch(function(){{
        setStatus('Something went wrong. Emailing you instead: ', 'err');
        window.location.href = 'mailto:' + CONTACT_EMAIL + '?subject=' + encodeURIComponent('Course waitlist') + '&body=' + encodeURIComponent('Email: ' + email + (name ? ('\\nName: ' + name) : '') + (note ? ('\\nFilm: ' + note) : ''));
      }})
      .finally(function(){{ submit.disabled = false; }});
  }});
}})();
</script>'''
    return render_shell(fm.get("title", ""), fm.get("description", ""), content, nav_active="course", extra_script=extra_script)


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
        f'mailto:{fm.get("contact_email","geoff@thevfxsupervisor.com")}',
        "See Breakdown Studio",
        SITE_ROOT + "projects/breakdown-studio/",
    )
    return render_shell(fm.get("title", ""), fm.get("description", ""), content, nav_active="about")


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
    return render_shell("Notes | the vfx supervisor", "Notes on pipeline, production and orchestrating AI, from a working VFX supervisor and producer.", content, nav_active="notes")


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
    return render_shell(fm.get("title", ""), fm.get("description", ""), content, nav_active="notes"), fm.get("slug", md_path.stem)


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
    write_page("projects/breakdown-studio", render_breakdown_studio())
    write_page("course", render_course())
    write_page("about", render_about())
    write_page("notes", render_notes())

    for md_path in sorted((CONTENT_DIR / "notes").glob("*.md")):
        fm, _ = parse_frontmatter(md_path.read_text(encoding="utf-8"))
        if fm.get("draft", "").lower() == "true":
            continue
        note_html, slug = render_note(md_path)
        write_page(f"notes/{slug}", note_html)

    # static assets
    static_out = DOCS_DIR / "static"
    static_out.mkdir(parents=True, exist_ok=True)
    for f in STATIC_DIR.glob("*"):
        if f.is_file():
            shutil.copy2(f, static_out / f.name)
            print(f"  copied static/{f.name}")

    # CNAME for GitHub Pages custom domain (harmless before DNS cutover)
    (DOCS_DIR / "CNAME").write_text(DOMAIN + "\n", encoding="utf-8")
    print(f"  wrote docs/CNAME ({DOMAIN})")

    # .nojekyll so Pages serves the docs/ tree as-is (no Jekyll processing)
    (DOCS_DIR / ".nojekyll").write_text("", encoding="utf-8")
    print("  wrote docs/.nojekyll")

    print("Done.")


if __name__ == "__main__":
    main()
