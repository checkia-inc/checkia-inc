#!/usr/bin/env python3
"""SEO validation for the CheckIA site (output messages are in French).

For every blog post and index page:
  - <title> (50-60 chars) and meta description (140-160 chars)
  - canonical https://checkia.fr/… with trailing slash, matching the path
  - single <h1>, h2/h3 hierarchy without skipped levels
  - visible FAQ == JSON-LD FAQPage (word for word)
  - video chapters (data-start) == JSON-LD Clip (startOffset)
  - ISO 8601 dates in datetime/OG/JSON-LD; article:modified_time == dateModified
  - leftover placeholders (REMPLACER_…)
  - og:image present, file exists on disk, og:image:alt and twitter:site set
  - every <img> inside <article> has an alt attribute
  - JSON-LD wordCount within 25 % of the real count
  - Organization has sameAs (social profiles)
Indexed articles only (checkia-meta block required):
  - og-image decision: dedicated (must not be the generic image) | default
  - target query: every word present in <title>, query should open it
  - named author: matching Person in JSON-LD and in the visible byline
  - present in sitemap.xml (lastmod == dateModified), feed.xml, llms.txt
  - at least 2 incoming internal links from other pages
  - social visual set in images/blog/<slug>/ and social.md next to the post (warnings)

Usage: python3 tools/check-seo.py   (exit 1 on errors)
"""

import html
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://checkia.fr"
GENERIC_OG = SITE + "/images/og-image.jpg"
TEAM = "L'équipe CheckIA"
SOCIAL_FILES = ["og.jpg", "instagram-feed.png", "instagram-square.png", "story.png"]

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


def fold(s):
    """Lowercase, strip accents, keep letters/digits only (for query matching)."""
    s = unicodedata.normalize("NFKD", norm(s))
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


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


def parse_meta(raw):
    m = re.search(r"<!--\s*checkia-meta\s*(.*?)-->", raw, re.S)
    if not m:
        return None
    d = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if ":" in line:
            k, v = line.split(":", 1)
            d[k.strip().lower()] = re.sub(r"\s*\(.*\)\s*$", "", v).strip()
    return d


def check_page(path):
    rel = path.relative_to(ROOT)
    page = str(rel)
    raw = path.read_text(encoding="utf-8")
    meta = parse_meta(raw)
    text = re.sub(r"<!--.*?-->", "", raw, flags=re.S)

    is_noindex = bool(re.search(r'<meta name="robots" content="[^"]*noindex', text))
    is_article = len(rel.parts) == 4 and rel.parts[0] == "blog"

    # Title / description
    title = None
    m = re.search(r"<title>([^<]*)</title>", text)
    if not m:
        err(page, "pas de <title>")
    else:
        title = norm(m.group(1))
        if not 40 <= len(title) <= 65:
            warn(page, f"<title> de {len(title)} caractères (cible 50-60) : « {title} »")
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

    # H1 / hierarchy
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

    # ISO dates
    for dt in re.findall(r'datetime="([^"]+)"', text):
        if not re.match(r"^(P|\d{4}-\d{2}-\d{2})", dt):
            (warn if is_noindex else err)(page, f"datetime non ISO 8601 : {dt}")

    blocks = get_jsonld(text, page)
    items = list(graph_items(blocks))
    by_id = {it.get("@id"): it for it in items if isinstance(it, dict) and it.get("@id")}

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

    # Chapters vs Clip
    starts_html = [int(s) for s in re.findall(r'data-start="(\d+)"', text)]
    video = next((it for it in items if it.get("@type") == "VideoObject"), None)
    if starts_html or (video and video.get("hasPart")):
        clips = [c.get("startOffset") for c in (video or {}).get("hasPart", [])]
        if starts_html != clips:
            err(page, f"chapitres HTML {starts_html} ≠ Clip JSON-LD {clips}")

    # BlogPosting: dates
    post = next((it for it in items if it.get("@type") == "BlogPosting"), None)
    date_mod = None
    if post:
        date_mod = post.get("dateModified")
        og_mod = re.search(r'article:modified_time" content="([^"]+)"', text)
        if og_mod and date_mod and og_mod.group(1) != date_mod:
            err(page, "article:modified_time ≠ dateModified (JSON-LD)")

    # Organization sameAs
    org = next((it for it in items if it.get("@type") == "Organization"), None)
    if org and not org.get("sameAs"):
        warn(page, "Organization sans sameAs (profils sociaux)")

    # OG image
    og = re.search(r'property="og:image" content="([^"]*)"', text)
    og_url = og.group(1) if og else None
    if is_article:
        if not og_url:
            err(page, "pas d'og:image")
        else:
            if og_url.startswith(SITE + "/"):
                f = ROOT / og_url[len(SITE) + 1:]
                if not f.exists():
                    (warn if is_noindex else err)(page, f"og:image introuvable sur le disque : {og_url}")
            if not re.search(r'property="og:image:alt"', text):
                warn(page, "pas d'og:image:alt")
        if not re.search(r'name="twitter:site"', text):
            warn(page, "pas de twitter:site")

    # <img> alt inside <article>
    art = re.search(r"<article[\s>].*?</article>", text, re.S)
    if art:
        for tag in re.findall(r"<img\b[^>]*>", art.group(0)):
            if not re.search(r"\salt=", tag):
                (warn if is_noindex else err)(page, f"image sans attribut alt : {tag[:80]}")
        if post and isinstance(post.get("wordCount"), int):
            words = len(norm(art.group(0)).split())
            wc = post["wordCount"]
            if abs(words - wc) > 0.25 * max(wc, 1):
                warn(page, f"wordCount JSON-LD {wc} vs {words} mots réels")

    # Meta block (indexed articles)
    if is_article and not is_noindex:
        if meta is None:
            err(page, "bloc checkia-meta absent (format / query / author / og-image)")
        else:
            ogv = meta.get("og-image", "pending").lower()
            if ogv == "pending":
                err(page, "og-image: pending — décider dedicated (image dédiée) ou default (validé par l'auteur)")
            elif ogv == "default":
                warn(page, "image OG générique (og-image: default, validé par l'auteur)")
            elif ogv == "dedicated":
                if og_url == GENERIC_OG:
                    err(page, "og-image: dedicated mais og:image est l'image générique")
            else:
                err(page, f"og-image inconnu : {ogv}")

            q = meta.get("query", "none")
            if q.lower() != "none" and title:
                qw = fold(q).split()
                tw = fold(title).split()
                missing = [w for w in qw if w not in tw]
                if missing:
                    err(page, f"requête cible « {q} » : mots absents du <title> : {', '.join(missing)}")
                elif tw[: len(qw)] != qw:
                    warn(page, f"la requête cible « {q} » n'ouvre pas le <title>")

            author = meta.get("author", TEAM)
            if author != TEAM:
                a = post.get("author") if post else None
                if isinstance(a, dict) and "@id" in a and "@type" not in a:
                    a = by_id.get(a["@id"])
                if not (isinstance(a, dict) and a.get("@type") == "Person" and norm(a.get("name", "")) == norm(author)):
                    err(page, f"auteur « {author} » sans Person correspondant dans le JSON-LD")
                if norm(author) not in norm(text):
                    err(page, f"auteur « {author} » absent de la signature visible")

    return {
        "page": page, "path": path, "canonical": canonical, "noindex": is_noindex,
        "date_mod": date_mod, "is_article": is_article, "text": text,
    }


def main():
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    feed = (ROOT / "blog" / "feed.xml").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_urls = dict(
        re.findall(r"<loc>([^<]+)</loc>\s*(?:<lastmod>([^<]*)</lastmod>)?", sitemap)
    )

    pages = sorted(p for p in ROOT.rglob("index.html")
                   if ".git" not in p.parts and "_templates" not in p.parts and "demo" not in p.parts)
    results = [check_page(p) for p in pages]

    for r in results:
        page, canonical, date_mod = r["page"], r["canonical"], r["date_mod"]
        if not canonical:
            continue
        if r["noindex"]:
            if canonical in sitemap_urls:
                err(page, "page noindex présente dans sitemap.xml")
            continue
        if canonical not in sitemap_urls:
            err(page, "absente de sitemap.xml")
        elif date_mod and sitemap_urls.get(canonical):
            if sitemap_urls[canonical][:10] != date_mod[:10]:
                err(page, f"lastmod sitemap ({sitemap_urls[canonical]}) ≠ dateModified ({date_mod[:10]})")
        if r["is_article"]:
            if canonical not in feed:
                err(page, "absente de blog/feed.xml")
            if canonical not in llms:
                err(page, "absente de llms.txt")
            md = r["path"].parent / "index.md"
            if not md.exists():
                warn(page, "pas d'alternate markdown (index.md) pour les LLM")

            # Incoming internal links
            rel_path = canonical[len(SITE):]
            incoming = sum(
                1 for o in results
                if o["path"] != r["path"]
                and (f'href="{rel_path}"' in o["text"] or f'href="{canonical}"' in o["text"])
            )
            if incoming < 2:
                err(page, f"{incoming} lien(s) internes entrants (minimum 2 : hub /blog/ + page de série)")

            # Social copy
            if not (r["path"].parent / "social.md").exists():
                warn(page, "pas de social.md (tweet, Instagram, LinkedIn/Facebook)")

            # Social visual set
            slug = r["path"].parent.name
            sdir = ROOT / "images" / "blog" / slug
            if not sdir.is_dir():
                warn(page, f"pas de visuels réseaux sociaux (images/blog/{slug}/ — tools/social-images.py)")
            else:
                for f in SOCIAL_FILES:
                    if not (sdir / f).exists():
                        warn(page, f"visuel manquant : images/blog/{slug}/{f}")

    if not (ROOT / "llms-full.txt").exists():
        warnings.append("[attention] llms-full.txt absent (version longue pour les LLM)")

    for w in warnings:
        print(w)
    for e in errors:
        print(e)
    print(f"\n{len(pages)} pages vérifiées — {len(errors)} erreur(s), {len(warnings)} avertissement(s).")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
