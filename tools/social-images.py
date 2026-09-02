#!/usr/bin/env python3
"""Generate the OG image and the social visual set for a blog post.

Usage:
  python3 tools/social-images.py <serie> <slug> --source generated
  python3 tools/social-images.py <serie> <slug> --source image:path/to/photo.jpg
  python3 tools/social-images.py <serie> <slug> --source video:YOUTUBE_ID
  Options: --title "…"  --line "…"   (default: the article's <h1> and first
           « L'essentiel » bullet)
           --only og|instagram-feed|instagram-square|story

Output in images/blog/<slug>/ :
  og.jpg              1200×630   Open Graph, LinkedIn, Facebook, X
  instagram-feed.png  1080×1350  Instagram feed (4:5)
  instagram-square.png 1080×1080 Instagram square, LinkedIn square
  story.png           1080×1920  Instagram / Facebook stories

Requires: pip3 install playwright && python3 -m playwright install chromium
All text rendered on the cards is French (taken from the article).
"""

import base64
import html as htmlmod
import mimetypes
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://checkia.fr"

SERIES = {
    "nouveautes-produit": "Nouveautés produit",
    "futur-de-l-audit": "Le futur de l'audit",
    "vie-de-l-entreprise": "Vie de l'entreprise",
    "temoignages-clients": "Témoignages clients",
}

FORMATS = {
    "og": (1200, 630, "jpeg"),
    "instagram-feed": (1080, 1350, "png"),
    "instagram-square": (1080, 1080, "png"),
    "story": (1080, 1920, "png"),
}


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(str(path))[0] or "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def clean(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)
    s = htmlmod.unescape(s).replace(" ", " ").replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


def read_article(serie: str, slug: str):
    path = ROOT / "blog" / serie / slug / "index.html"
    if not path.exists():
        sys.exit(f"Article introuvable : {path}")
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.S)
    title = clean(h1.group(1)) if h1 else slug
    line = ""
    tldr = re.search(r'class="tldr"(.*?)</(?:div|aside|section)>', text, re.S)
    if tldr:
        li = re.search(r"<li[^>]*>(.*?)</li>", tldr.group(1), re.S)
        if li:
            line = clean(li.group(1))
    if not line:
        d = re.search(r'<meta name="description" content="([^"]*)"', text)
        line = clean(d.group(1)) if d else ""
    return title, line


def fetch_youtube_thumbnail(video_id: str, dest: Path) -> Path:
    for name in ("maxresdefault", "sddefault", "hqdefault"):
        url = f"https://img.youtube.com/vi/{video_id}/{name}.jpg"
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                data = r.read()
            if len(data) > 5000:  # YouTube returns a tiny placeholder on 404-ish
                dest.write_bytes(data)
                return dest
        except urllib.error.URLError:
            continue
    sys.exit(f"Miniature YouTube introuvable pour {video_id}")


def build_html(w: int, h: int, title: str, line: str, series: str, logo: str, photo=None) -> str:
    u = w / 1200  # width-driven scale
    tall = h > w
    t = 64 * u * (1.2 if tall else 1)
    if len(title) > 70:
        t *= 0.86
    if len(title) > 95:
        t *= 0.84
    pad = 72 * u
    logo_h = 44 * u
    eb = 22 * u
    l = (30 if tall else 27) * u
    f = 24 * u
    maxw = (w - 2 * pad) * (0.9 if not tall else 1)
    aura = 0.95 * min(w, h)
    g = 48 * u
    title_e = htmlmod.escape(title)
    line_e = htmlmod.escape(line)
    series_e = htmlmod.escape(series)

    if photo:
        bg = f'<img class="bg" src="{photo}" alt=""><div class="shade"></div>'
        text_color, line_color, eyebrow_color, foot_color = "#fff", "rgba(255,255,255,.88)", "#55e2fa", "#fff"
        deco = ""
    else:
        bg = ""
        text_color, line_color, eyebrow_color, foot_color = "#0e0f12", "#3b3f48", "#0f62dc", "#0a47a0"
        deco = '<div class="aura"></div><div class="grid"></div>'

    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap">
<style>
html,body{{margin:0;width:{w}px;height:{h}px;overflow:hidden}}
body{{font-family:Inter,-apple-system,"Segoe UI",Roboto,sans-serif;background:#f7f8fa;color:{text_color};position:relative;-webkit-font-smoothing:antialiased}}
.bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.shade{{position:absolute;inset:0;background:linear-gradient(to top,rgba(8,20,48,.92) 0%,rgba(8,20,48,.62) 45%,rgba(8,20,48,.25) 100%)}}
.aura{{position:absolute;width:{aura:.0f}px;height:{aura:.0f}px;border-radius:50%;right:{-aura*0.35:.0f}px;top:{-aura*0.35:.0f}px;background:radial-gradient(circle,#55e2fa 0%,#ebf3ff 52%,rgba(235,243,255,0) 72%);opacity:.95}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(#e2e4e9 1px,transparent 1px),linear-gradient(90deg,#e2e4e9 1px,transparent 1px);background-size:{g:.0f}px {g:.0f}px;opacity:.55;-webkit-mask-image:linear-gradient(to bottom,rgba(0,0,0,.8),transparent 85%)}}
.card{{position:absolute;inset:0;padding:{pad:.0f}px;display:flex;flex-direction:column;justify-content:space-between}}
.logo img{{height:{logo_h:.0f}px;display:block;{"filter:brightness(0) invert(1);" if photo else ""}}}
.eyebrow{{color:{eyebrow_color};font-weight:600;font-size:{eb:.0f}px;letter-spacing:.06em;text-transform:uppercase;display:flex;align-items:center;gap:.6em;margin:0}}
.eyebrow::before{{content:"";width:.55em;height:.55em;border-radius:50%;background:{eyebrow_color}}}
h1{{font-size:{t:.0f}px;line-height:1.08;font-weight:700;letter-spacing:-.022em;margin:.4em 0 .45em;max-width:{maxw:.0f}px;text-wrap:balance}}
.line{{font-size:{l:.0f}px;line-height:1.38;color:{line_color};max-width:{maxw:.0f}px;margin:0}}
.foot{{display:flex;justify-content:space-between;align-items:center;font-size:{f:.0f}px;color:{foot_color};font-weight:600}}
</style></head><body>
{bg}{deco}
<div class="card">
  <div class="logo"><img src="{logo}" alt=""></div>
  <div>
    <p class="eyebrow">{series_e}</p>
    <h1>{title_e}</h1>
    <p class="line">{line_e}</p>
  </div>
  <div class="foot"><span>checkia.fr</span><span>Blog CheckIA</span></div>
</div>
</body></html>"""


def main():
    argv = sys.argv[1:]
    args, opts = [], {}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--"):
            key = a[2:]
            if "=" in key:
                key, val = key.split("=", 1)
            else:
                i += 1
                val = argv[i] if i < len(argv) else ""
            opts[key] = val
        else:
            args.append(a)
        i += 1
    if len(args) < 2 or "source" not in opts:
        sys.exit(__doc__)
    serie, slug = args[0], args[1]
    if serie not in SERIES:
        sys.exit(f"Série inconnue : {serie}. Choix : {', '.join(SERIES)}")

    title, line = read_article(serie, slug)
    title = opts.get("title") or title
    line = opts.get("line") or line

    out_dir = ROOT / "images" / "blog" / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    source = opts["source"]
    photo = None
    if source == "generated":
        pass
    elif source.startswith("image:"):
        p = Path(source[6:]).expanduser()
        if not p.is_absolute():
            p = (Path.cwd() / p).resolve()
        if not p.exists():
            sys.exit(f"Image introuvable : {p}")
        photo = data_uri(p)
    elif source.startswith("video:"):
        tmp = out_dir / "source-youtube.jpg"
        fetch_youtube_thumbnail(source[6:], tmp)
        photo = data_uri(tmp)
    else:
        sys.exit("--source : generated | image:<chemin> | video:<ID_YOUTUBE>")

    logo = data_uri(ROOT / "images" / "logo_coor.png")
    wanted = [opts["only"]] if opts.get("only") else list(FORMATS)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("Playwright manquant : pip3 install playwright && python3 -m playwright install chromium")

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for name in wanted:
            w, h, kind = FORMATS[name]
            page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
            page.set_content(build_html(w, h, title, line, SERIES[serie], logo, photo))
            try:
                page.wait_for_load_state("networkidle", timeout=8000)
            except Exception:
                pass  # offline: system font fallback
            page.wait_for_timeout(300)
            ext = "jpg" if kind == "jpeg" else "png"
            out = out_dir / f"{name}.{ext}"
            if kind == "jpeg":
                page.screenshot(path=str(out), type="jpeg", quality=88, full_page=False)
            else:
                page.screenshot(path=str(out), type="png", full_page=False)
            page.close()
            print(f"✓ {out.relative_to(ROOT)}  ({w}×{h})")
        browser.close()

    og_url = f"{SITE}/images/blog/{slug}/og.jpg"
    print("\nÀ reporter dans le <head> et le JSON-LD de l'article :")
    print(f'  <meta property="og:image" content="{og_url}">')
    print('  <meta property="og:image:width" content="1200">')
    print('  <meta property="og:image:height" content="630">')
    print(f'  <meta property="og:image:alt" content="{htmlmod.escape(title)}">')
    print(f'  <meta name="twitter:image" content="{og_url}">')
    print(f'  JSON-LD BlogPosting "image": "{og_url}"')
    print("  Bloc checkia-meta : og-image: dedicated")


if __name__ == "__main__":
    main()
