#!/usr/bin/env python3
"""Generate a per-page Open Graph image for every content page.

One shared og-image.png meant every social share of this site looked identical,
so a case study, a note and the homepage were indistinguishable in a preview.
This renders a card per page carrying that page's own eyebrow and headline.

Driven by the REAL frontmatter in content/, so a new page gets a card without
anyone remembering to make one, and a retitled page cannot keep a stale card.

Run:  "C:\\Program Files\\Shotgun\\Python3\\python.exe" dev/make_og.py
Writes: static/og/<slug>.png at 1200x630, plus static/og/default.png.

Fonts are Windows system fonts, which is where this site is built. If a face is
missing the script says so and falls back rather than rendering a broken card.
"""
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
OUT = os.path.join(ROOT, "static", "og")
LOGO = os.path.join(ROOT, "static", "logo-icon.png")

W, H = 1200, 630
BG = "#131619"          # --bg
INK = "#e9e6df"         # --txt
ACCENT = "#0585f8"      # --amber, blue despite the name
MUTE = "#9aa1a8"        # --dim

BOLD = "C:/Windows/Fonts/segoeuib.ttf"
REG = "C:/Windows/Fonts/segoeui.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        print("  WARNING: missing font %s, falling back" % path)
        return ImageFont.load_default()


def frontmatter(path):
    """The YAML-lite frontmatter as a dict. Same shape build.py expects."""
    fm = {}
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return fm
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def card(eyebrow, headline, out_path):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # accent rule down the left, so the card reads as this site at a glance
    d.rectangle([0, 0, 10, H], fill=ACCENT)

    pad = 84
    y = 150

    if eyebrow:
        f_eye = font(REG, 30)
        d.text((pad, y), eyebrow.upper(), font=f_eye, fill=ACCENT)
        y += 58

    # Shrink to fit the actual BOX, not a line count. Counting lines looks like
    # a fit check and is not one: four lines at the largest size overflow into
    # the footer, which is what shipped the first time this ran.
    avail = (H - 92 - 24) - y
    for size in (76, 68, 60, 52, 46, 40, 36):
        f_head = font(BOLD, size)
        lines = wrap(d, headline, f_head, W - pad * 2 - 40)
        lh = int(size * 1.22)
        if len(lines) * lh <= avail:
            break
    else:
        lines = lines[: max(1, avail // lh)]
    for line in lines:
        d.text((pad, y), line, font=f_head, fill=INK)
        y += lh

    f_foot = font(REG, 30)
    d.text((pad, H - 92), "thevfxsupervisor.com", font=f_foot, fill=MUTE)

    if os.path.exists(LOGO):
        try:
            logo = Image.open(LOGO).convert("RGBA")
            logo.thumbnail((92, 92))
            img.paste(logo, (W - 92 - pad, H - 92 - 36), logo)
        except OSError:
            pass

    img.save(out_path, "PNG", optimize=True)
    return out_path


def headline_for(fm):
    """h1 is written for a human; title carries the SEO suffix. Prefer h1."""
    h = fm.get("h1") or fm.get("title") or ""
    return h.split(" | ")[0].strip()


def main():
    os.makedirs(OUT, exist_ok=True)
    made = 0
    for sub in ("pages", "projects", "notes"):
        d = os.path.join(CONTENT, sub)
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if not name.endswith(".md"):
                continue
            fm = frontmatter(os.path.join(d, name))
            if fm.get("draft", "").lower() == "true":
                continue
            slug = fm.get("slug") or os.path.splitext(name)[0]
            eyebrow = fm.get("eyebrow") or {"projects": "Case study",
                                            "notes": "Note"}.get(sub, "")
            headline = headline_for(fm)
            if not headline:
                print("  SKIP %s: no h1 or title" % name)
                continue
            card(eyebrow, headline, os.path.join(OUT, slug + ".png"))
            made += 1
            print("  %-28s %s" % (slug + ".png", headline[:58]))

    card("", "VFX supervision, production pipelines, and AI with guardrails",
         os.path.join(OUT, "default.png"))
    made += 1
    print("\n%d cards written to static/og/" % made)
    return 0


if __name__ == "__main__":
    sys.exit(main())
