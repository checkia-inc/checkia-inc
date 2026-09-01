#!/usr/bin/env python3
"""Génère la couche LLM du site à partir des articles publiés :

  - blog/<serie>/<slug>/index.md : version markdown de chaque article
    (titre, méta, « L'essentiel », corps, FAQ, transcription) ;
  - llms-full.txt : concaténation de tous les articles indexables, pour les
    crawlers d'IA qui suivent le lien depuis llms.txt.

À relancer après chaque publication ou modification d'article :
  python3 tools/build-llms.py
"""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://checkia.fr"


def clean(s):
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', r"[\2](\1)", s, flags=re.S)
    s = re.sub(r"\]\(/", f"]({SITE}/", s)
    s = re.sub(r"<(strong|b)>(.*?)</\1>", r"**\2**", s, flags=re.S)
    s = re.sub(r"<(em|i)>(.*?)</\1>", r"*\2*", s, flags=re.S)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s).replace(" ", " ").replace(" ", " ")
    return re.sub(r"[ \t]+", " ", s).strip()


def block_to_md(seg):
    """Convertit une portion de .prose en markdown."""
    out = []
    pattern = re.compile(
        r"<(h2|h3|p|blockquote|ol|ul)[^>]*>(.*?)</\1>", re.S)
    for m in pattern.finditer(seg):
        tag, body = m.group(1), m.group(2)
        if tag == "h2":
            out.append("## " + clean(body))
        elif tag == "h3":
            out.append("### " + clean(body))
        elif tag == "p":
            out.append(clean(body))
        elif tag == "blockquote":
            inner = clean(re.sub(r"<footer>(.*?)</footer>", r" \1", body, flags=re.S))
            out.append("> " + inner)
        elif tag in ("ol", "ul"):
            items = re.findall(r"<li[^>]*>(.*?)</li>", body, re.S)
            mark = "1." if tag == "ol" else "-"
            out.extend(f"{mark} {clean(i)}" for i in items)
    return "\n\n".join(out)


def article_to_md(path):
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    if re.search(r'<meta name="robots" content="[^"]*noindex', text):
        return None

    rel = path.relative_to(ROOT).parent
    url = f"{SITE}/{rel}/"
    title = clean(re.search(r"<h1[^>]*>(.*?)</h1>", text, re.S).group(1))
    desc = re.search(r'<meta name="description" content="([^"]*)"', text)
    desc = clean(desc.group(1)) if desc else ""
    pub = re.search(r'article:published_time" content="([^"]{10})', text)
    serie = re.search(r'article:section" content="([^"]*)"', text)
    lead = re.search(r'<p class="lead[^"]*"[^>]*>(.*?)</p>', text, re.S)

    md = [f"# {title}", ""]
    meta = [f"Source : {url}"]
    if serie:
        meta.append(f"Série : {clean(serie.group(1))}")
    if pub:
        meta.append(f"Publié : {pub.group(1)}")
    md.append(" — ".join(meta))
    md += ["", desc, ""]
    if lead:
        md += [clean(lead.group(1)), ""]

    tldr = re.search(r'<aside class="tldr[^"]*".*?<ul>(.*?)</ul>', text, re.S)
    if tldr:
        md.append("## L'essentiel")
        md.append("")
        for li in re.findall(r"<li[^>]*>(.*?)</li>", tldr.group(1), re.S):
            md.append(f"- {clean(li)}")
        md.append("")

    prose = re.search(r'<div class="prose">(.*?)</div>\s*(?:</div>|<div class="share")', text, re.S)
    if prose:
        seg = prose.group(1)
        faq_split = seg.split('<div class="faq">')
        md += [block_to_md(faq_split[0]), ""]
        if len(faq_split) > 1:
            for q, a in re.findall(
                    r"<details>\s*<summary>(.*?)</summary>\s*<p>(.*?)</p>\s*</details>",
                    faq_split[1], re.S):
                md += [f"### {clean(q)}", "", clean(a), ""]

    tr = re.search(r'<details class="transcript">.*?<div>(.*?)</div>', text, re.S)
    if tr:
        md += ["## Transcription de la vidéo", "", block_to_md(tr.group(1)), ""]

    return "\n".join(md).strip() + "\n"


def main():
    articles = sorted(ROOT.glob("blog/*/*/index.html"))
    full = ["# CheckIA — articles complets du blog",
            "",
            f"> Version intégrale des articles de {SITE}/blog/ pour les assistants et moteurs d'IA. "
            f"Index court : {SITE}/llms.txt", ""]
    n = 0
    for a in articles:
        md = article_to_md(a)
        if md is None:
            continue
        (a.parent / "index.md").write_text(md, encoding="utf-8")
        print(f"écrit : {a.parent.relative_to(ROOT)}/index.md")
        full += ["---", "", md]
        n += 1
    (ROOT / "llms-full.txt").write_text("\n".join(full), encoding="utf-8")
    print(f"écrit : llms-full.txt ({n} article(s))")


if __name__ == "__main__":
    main()
