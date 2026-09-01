#!/usr/bin/env python3
"""Vérification SEO du site CheckIA.

Contrôle, pour chaque article du blog et pour les pages d'index :
  - <title> (50-60 car.) et meta description (140-160 car.)
  - canonical en https://checkia.fr/… avec slash final, cohérent avec le chemin
  - un seul <h1>, hiérarchie h2/h3 sans saut
  - FAQ visible == bloc FAQPage du JSON-LD (mot pour mot)
  - chapitres vidéo (data-start) == Clip du JSON-LD (startOffset)
  - dates ISO 8601 dans datetime/OG/JSON-LD
  - placeholders oubliés (REMPLACER_…)
  - présence dans sitemap.xml, feed.xml et llms.txt (pages indexables)
  - lastmod du sitemap == dateModified de l'article

Usage : python3 tools/check-seo.py   (exit 1 si erreurs)
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://checkia.fr"

errors, warnings = [], []


def err(page, msg):
    errors.append(f"[ERREUR] {page}: {msg}")


def warn(page, msg):
    warnings.append(f"[attention] {page}: {msg}")


def norm(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = s.replace(" ", " ").replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


def get_jsonld(text, page):
    blocks = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
        try:
            blocks.append(json.loads(m.group(1)))
        except json.JSONDecodeError as e:
            err(page, f"JSON-LD invalide : {e}")
    return blocks


def graph_items(blocks):
    for b in blocks:
        items = b.get("@graph", [b]) if isinstance(b, dict) else []
        for it in items:
            yield it


def check_page(path):
    rel = path.relative_to(ROOT)
    page = str(rel)
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)

    is_noindex = re.search(r'<meta name="robots" content="[^"]*noindex', text)

    # Title / description
    m = re.search(r"<title>([^<]*)</title>", text)
    if not m:
        err(page, "pas de <title>")
    else:
        t = norm(m.group(1))
        if not 40 <= len(t) <= 65:
            warn(page, f"<title> de {len(t)} caractères (cible 50-60) : « {t} »")
    m = re.search(r'<meta name="description" content="([^"]*)"', text)
    if not m:
        err(page, "pas de meta description")
    else:
        d = norm(m.group(1))
        if not 120 <= len(d) <= 170:
            warn(page, f"description de {len(d)} caractères (cible 140-160)")

    # Canonical
    m = re.search(r'<link rel="canonical" href="([^"]*)"', text)
    canonical = m.group(1) if m else None
    if not canonical:
        err(page, "pas de canonical")
    else:
        if not canonical.startswith(SITE) or not canonical.endswith("/"):
            err(page, f"canonical invalide (https://checkia.fr/… + slash final) : {canonical}")
        expected = SITE + "/" + str(rel.parent).replace("\\", "/") + "/"
        expected = expected.replace("/./", "/")
        if rel == Path("index.html"):
            expected = SITE + "/"
        if canonical != expected:
            err(page, f"canonical {canonical} ≠ chemin {expected}")

    # H1 / hiérarchie
    h1s = re.findall(r"<h1[\s>]", text)
    if len(h1s) != 1:
        err(page, f"{len(h1s)} balises <h1> (attendu : 1)")
    levels = [int(m.group(1)) for m in re.finditer(r"<h([1-6])[\s>]", text)]
    prev = 1
    for lv in levels:
        if lv > prev + 1:
            err(page, f"saut de hiérarchie : h{prev} → h{lv}")
        prev = lv

    # Placeholders
    for ph in set(re.findall(r"REMPLACER_[A-Z_]+", text)):
        (warn if is_noindex else err)(page, f"placeholder restant : {ph}")

    # Dates ISO
    for dt in re.findall(r'datetime="([^"]+)"', text):
        if not re.match(r"^(P|\d{4}-\d{2}-\d{2})", dt):
            (warn if is_noindex else err)(page, f"datetime non ISO 8601 : {dt}")

    blocks = get_jsonld(text, page)
    items = list(graph_items(blocks))

    # FAQ visible vs FAQPage
    faq_ld = next((it for it in items if it.get("@type") == "FAQPage"), None)
    faq_html = re.findall(
        r'<details>\s*<summary>(.*?)</summary>\s*<p>(.*?)</p>\s*</details>',
        re.search(r'<div class="faq">(.*?)</div>', text, re.S).group(1) if '<div class="faq">' in text else "",
        re.S,
    )
    if faq_ld or faq_html:
        ld_pairs = [
            (norm(q.get("name", "")), norm(q.get("acceptedAnswer", {}).get("text", "")))
            for q in (faq_ld or {}).get("mainEntity", [])
        ]
        html_pairs = [(norm(q), norm(a)) for q, a in faq_html]
        if not faq_ld:
            err(page, "FAQ visible sans bloc FAQPage dans le JSON-LD")
        elif not html_pairs:
            err(page, "FAQPage dans le JSON-LD sans FAQ visible")
        elif ld_pairs != html_pairs:
            err(page, "FAQ visible ≠ FAQPage JSON-LD (mot pour mot)")

    # Chapitres vs Clip
    starts_html = [int(s) for s in re.findall(r'data-start="(\d+)"', text)]
    video = next((it for it in items if it.get("@type") == "VideoObject"), None)
    if starts_html or (video and video.get("hasPart")):
        clips = [c.get("startOffset") for c in (video or {}).get("hasPart", [])]
        if starts_html != clips:
            err(page, f"chapitres HTML {starts_html} ≠ Clip JSON-LD {clips}")

    # BlogPosting : dates + auteur
    post = next((it for it in items if it.get("@type") == "BlogPosting"), None)
    date_mod = None
    if post:
        date_mod = post.get("dateModified")
        og_mod = re.search(r'article:modified_time" content="([^"]+)"', text)
        if og_mod and date_mod and og_mod.group(1) != date_mod:
            err(page, "article:modified_time ≠ dateModified (JSON-LD)")

    return canonical, is_noindex, date_mod


def main():
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    feed = (ROOT / "blog" / "feed.xml").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_urls = dict(
        re.findall(r"<loc>([^<]+)</loc>\s*(?:<lastmod>([^<]*)</lastmod>)?", sitemap)
    )

    pages = sorted(p for p in ROOT.rglob("index.html")
                   if ".git" not in p.parts and "_templates" not in p.parts and "demo" not in p.parts)
    for p in pages:
        canonical, noindex, date_mod = check_page(p)
        page = str(p.relative_to(ROOT))
        if not canonical:
            continue
        is_article = len(p.relative_to(ROOT).parts) == 4  # blog/<serie>/<slug>/index.html
        if noindex:
            if canonical in sitemap_urls:
                err(page, "page noindex présente dans sitemap.xml")
            continue
        if canonical not in sitemap_urls:
            err(page, "absente de sitemap.xml")
        elif date_mod and sitemap_urls.get(canonical):
            if sitemap_urls[canonical][:10] != date_mod[:10]:
                err(page, f"lastmod sitemap ({sitemap_urls[canonical]}) ≠ dateModified ({date_mod[:10]})")
        if is_article:
            if canonical not in feed:
                err(page, "absente de blog/feed.xml")
            if canonical not in llms:
                err(page, "absente de llms.txt")
            md = p.parent / "index.md"
            if not md.exists():
                warn(page, "pas d'alternate markdown (index.md) pour les LLM")

    llmsfull = ROOT / "llms-full.txt"
    if not llmsfull.exists():
        warnings.append("[attention] llms-full.txt absent (version longue pour les LLM)")

    for w in warnings:
        print(w)
    for e in errors:
        print(e)
    print(f"\n{len(pages)} pages vérifiées — {len(errors)} erreur(s), {len(warnings)} avertissement(s).")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
