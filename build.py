#!/usr/bin/env python3
"""CheckIA site generator.

    python3 build.py            # build into the repo root (GitHub Pages serves it)
    python3 build.py --check    # build + run the integrity checks, no write

Content lives in content/ as Markdown with frontmatter. Every page declares its
URL, SEO metadata and either a list of structured `sections` (landing/hub pages)
or a Markdown body (editorial pages). This script renders them, then derives the
site-wide artefacts: navigation, breadcrumbs, JSON-LD, sitemap, robots, llms.txt
and the internal-link integrity report.

Stdlib only — no npm, no pip, no build container. `python3 build.py` is the
whole toolchain, which keeps the existing GitHub Pages branch deploy working.
"""

import argparse
import html
import json
import os
import re
import shutil
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import frontmatter, markdown as md, sections as sec

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")
SITE = os.path.join(ROOT, "site")
ORIGIN = "https://www.checkia.fr"

# Files at the repo root that the generator owns and may overwrite. Anything
# else at the root is left alone.
GENERATED_ROOT_FILES = {"index.html", "sitemap.xml", "robots.txt", "llms.txt", "404.html"}

_MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
         "août", "septembre", "octobre", "novembre", "décembre"]


def fr_date(value):
    """Render an ISO date as a French long date. Machine-readable dates stay
    ISO in JSON-LD and <time>; this is only for the visible text."""
    s = str(value)
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    if not m:
        return html.escape(s)
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    day = "1er" if d == 1 else str(d)
    return "%s %s %d" % (day, _MOIS[mo - 1], y)


# --------------------------------------------------------------------------- #
# loading
# --------------------------------------------------------------------------- #

def load_data():
    path = os.path.join(CONTENT, "_data", "site.md")
    fm, _ = frontmatter.split(open(path, encoding="utf-8").read())
    return fm


def load_pages():
    pages = []
    for dirpath, dirnames, filenames in os.walk(CONTENT):
        dirnames[:] = [d for d in dirnames if not d.startswith("_")]
        for fn in sorted(filenames):
            if not fn.endswith(".md"):
                continue
            path = os.path.join(dirpath, fn)
            fm, body = frontmatter.split(open(path, encoding="utf-8").read())
            if not fm.get("url"):
                raise ValueError("%s: frontmatter is missing `url`" % path)
            fm["_source"] = os.path.relpath(path, ROOT)
            fm["_body"] = body
            pages.append(fm)
    pages.sort(key=lambda p: p["url"])
    return pages


# --------------------------------------------------------------------------- #
# chrome
# --------------------------------------------------------------------------- #

def render_logo():
    return (
        '<a class="logo" href="/" aria-label="CheckIA — accueil">'
        '<svg viewBox="0 0 132 28" role="img" aria-hidden="true" focusable="false">'
        '<path d="M13.5 3.2a10.8 10.8 0 1 0 9.4 16.1l-3.5-2a6.8 6.8 0 1 1 0-6.6l3.5-2a10.8 '
        '10.8 0 0 0-9.4-5.5z" fill="var(--blue)"/>'
        '<path d="M19.4 9.1l3.5-2 3.6 2v4l-3.6 2-3.5-2z" fill="var(--cyan)"/>'
        "</svg><span>CheckIA</span></a>"
    )


def render_nav(data, current_url):
    groups = []
    for item in data.get("nav", []):
        if item.get("children"):
            cols = []
            for col in item["children"]:
                links = "".join(
                    '<li><a href="%s"><span class="mm-t">%s</span>'
                    '<span class="mm-d">%s</span></a></li>'
                    % (html.escape(l.get("href", "/"), quote=True),
                       html.escape(l.get("label", "")),
                       html.escape(l.get("note", "")))
                    for l in col.get("links", [])
                )
                cols.append(
                    '<div class="mm-col"><p class="mm-h">%s</p><ul>%s</ul></div>'
                    % (html.escape(col.get("title", "")), links)
                )
            groups.append(
                '<li class="has-mm"><button type="button" class="nav-btn" '
                'aria-expanded="false">%s<svg class="chev" viewBox="0 0 10 6" aria-hidden="true">'
                '<path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6" '
                'stroke-linecap="round"/></svg></button>'
                '<div class="mm"><div class="wrap mm-inner">%s</div></div></li>'
                % (html.escape(item.get("label", "")), "".join(cols))
            )
        else:
            active = " aria-current=\"page\"" if item.get("href") == current_url else ""
            groups.append(
                '<li><a href="%s"%s>%s</a></li>'
                % (html.escape(item.get("href", "/"), quote=True), active,
                   html.escape(item.get("label", "")))
            )
    return (
        '<header class="site"><div class="wrap nav">'
        '<div class="nav-left">%s<nav aria-label="Navigation principale">'
        '<ul class="nav-links">%s</ul></nav></div>'
        '<div class="nav-cta"><a class="btn btn-primary" href="/demo/">Réserver une démonstration</a>'
        '<button class="burger" type="button" aria-expanded="false" aria-controls="mnav" '
        'aria-label="Ouvrir le menu"><span></span><span></span><span></span></button></div>'
        "</div>%s</header>" % (render_logo(), "".join(groups), render_mobile_nav(data))
    )


def render_mobile_nav(data):
    out = []
    for item in data.get("nav", []):
        if item.get("children"):
            out.append('<p class="mnav-h">%s</p><ul>' % html.escape(item.get("label", "")))
            for col in item["children"]:
                for l in col.get("links", []):
                    out.append(
                        '<li><a href="%s">%s</a></li>'
                        % (html.escape(l.get("href", "/"), quote=True), html.escape(l.get("label", "")))
                    )
            out.append("</ul>")
        else:
            out.append(
                '<p class="mnav-h"><a href="%s">%s</a></p>'
                % (html.escape(item.get("href", "/"), quote=True), html.escape(item.get("label", "")))
            )
    return '<div class="mnav" id="mnav" hidden><div class="wrap">%s</div></div>' % "".join(out)


def render_footer(data):
    cols = []
    for col in data.get("footer", {}).get("columns", []):
        links = "".join(
            '<li><a href="%s">%s</a></li>'
            % (html.escape(l.get("href", "/"), quote=True), html.escape(l.get("label", "")))
            for l in col.get("links", [])
        )
        cols.append(
            '<div><p class="foot-h">%s</p><ul>%s</ul></div>'
            % (html.escape(col.get("title", "")), links)
        )
    note = data.get("footer", {}).get("note", "")
    legal = data.get("footer", {}).get("legal", "")
    return (
        '<footer class="site-foot"><div class="wrap">'
        '<div class="foot-top"><div class="foot-brand">%s<p>%s</p></div>'
        '<div class="foot-cols">%s</div></div>'
        '<div class="foot-bottom"><p>%s</p></div></div></footer>'
        % (render_logo(), md.inline(note), "".join(cols), md.inline(legal))
    )


def render_breadcrumb(page, index):
    url = page["url"]
    if url == "/":
        return "", None
    parts = [p for p in url.strip("/").split("/") if p]
    trail = [("Accueil", "/")]
    acc = ""
    for p in parts:
        acc += "/" + p
        target = acc + "/"
        label = index.get(target, {}).get("breadcrumb_label") or index.get(target, {}).get(
            "title"
        ) or p.replace("-", " ").capitalize()
        trail.append((label, target))
    li = []
    for i, (label, href) in enumerate(trail):
        last = i == len(trail) - 1
        # An intermediate segment with no page of its own is shown as plain
        # text — linking it would produce a 404 and an orphan-link report.
        if last or href not in index:
            attr = ' aria-current="page"' if last else ""
            li.append("<li%s>%s</li>" % (attr, html.escape(label)))
        else:
            li.append('<li><a href="%s">%s</a></li>' % (html.escape(href, quote=True), html.escape(label)))
    nav = (
        '<nav class="crumbs" aria-label="Fil d\'Ariane"><div class="wrap">'
        "<ol>%s</ol></div></nav>" % "".join(li)
    )
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            (
                {"@type": "ListItem", "position": i + 1, "name": label, "item": ORIGIN + href}
                if href in index
                else {"@type": "ListItem", "position": i + 1, "name": label}
            )
            for i, (label, href) in enumerate(trail)
        ],
    }
    return nav, schema


# --------------------------------------------------------------------------- #
# structured data
# --------------------------------------------------------------------------- #

def build_schema(page, data, ctx, crumb_schema):
    blocks = []
    wanted = page.get("schema") or []

    if "Organization" in wanted:
        org = data.get("organization", {})
        blocks.append({
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": org.get("name"),
            "url": ORIGIN + "/",
            "description": org.get("description"),
            "email": org.get("email"),
            "areaServed": "FR",
            "knowsLanguage": "fr-FR",
        })

    if "WebSite" in wanted:
        blocks.append({
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "CheckIA",
            "url": ORIGIN + "/",
            "inLanguage": "fr-FR",
            "publisher": {"@type": "Organization", "name": "CheckIA"},
        })

    if "SoftwareApplication" in wanted:
        blocks.append({
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "CheckIA",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web",
            "url": ORIGIN + "/",
            "inLanguage": "fr-FR",
            "description": page.get("seo", {}).get("description"),
            "audience": {
                "@type": "Audience",
                "audienceType": "Commissaires aux comptes, commissaires aux apports",
            },
        })

    if "Article" in wanted:
        art = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": page.get("title"),
            "description": page.get("seo", {}).get("description"),
            "inLanguage": "fr-FR",
            "mainEntityOfPage": ORIGIN + page["url"],
            "publisher": {"@type": "Organization", "name": "CheckIA"},
        }
        if page.get("published"):
            art["datePublished"] = str(page["published"])
        if page.get("updated"):
            art["dateModified"] = str(page["updated"])
        if page.get("author"):
            art["author"] = {"@type": "Person", "name": page["author"]}
        blocks.append(art)

    if "DefinedTerm" in wanted:
        blocks.append({
            "@context": "https://schema.org",
            "@type": "DefinedTerm",
            "name": page.get("term") or page.get("title"),
            "description": page.get("seo", {}).get("description"),
            "inDefinedTermSet": {
                "@type": "DefinedTermSet",
                "name": "Glossaire CheckIA du commissariat aux apports",
                "url": ORIGIN + "/glossaire/",
            },
        })

    # FAQPage only when FAQ items are actually rendered on the page
    if ctx.get("faq"):
        blocks.append({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in ctx["faq"]
            ],
        })

    if crumb_schema:
        blocks.append(crumb_schema)

    return "".join(
        '<script type="application/ld+json">%s</script>'
        % json.dumps(b, ensure_ascii=False, separators=(",", ":"))
        for b in blocks
    )


# --------------------------------------------------------------------------- #
# page rendering
# --------------------------------------------------------------------------- #

def render_head(page, data, schema_html):
    seo = page.get("seo", {}) or {}
    title = seo.get("title") or page.get("title")
    desc = seo.get("description", "")
    url = ORIGIN + page["url"]
    og_title = (page.get("og", {}) or {}).get("title") or title
    og_desc = (page.get("og", {}) or {}).get("description") or desc
    robots = "noindex, follow" if page.get("noindex") else "index, follow"

    meta = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>%s</title>" % html.escape(title),
        '<meta name="description" content="%s">' % html.escape(desc, quote=True),
        '<meta name="robots" content="%s">' % robots,
        '<link rel="canonical" href="%s">' % html.escape(url, quote=True),
        '<meta name="theme-color" content="#165498">',
        '<meta property="og:type" content="%s">' % ("article" if page.get("type") == "article" else "website"),
        '<meta property="og:url" content="%s">' % html.escape(url, quote=True),
        '<meta property="og:title" content="%s">' % html.escape(og_title, quote=True),
        '<meta property="og:description" content="%s">' % html.escape(og_desc, quote=True),
        '<meta property="og:locale" content="fr_FR">',
        '<meta property="og:site_name" content="CheckIA">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % html.escape(og_title, quote=True),
        '<meta name="twitter:description" content="%s">' % html.escape(og_desc, quote=True),
        '<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">',
        '<link rel="stylesheet" href="/assets/theme.css">',
    ]
    if page.get("updated"):
        meta.append('<meta name="last-modified" content="%s">' % html.escape(str(page["updated"])))
    return "".join(meta) + schema_html


def render_article_body(page, ctx):
    """Editorial page: metadata header, table of contents, prose, sources."""
    # Article bodies sit under the page h1, so `##` in the source is an h2.
    headings = []
    body = md.render(page["_body"], heading_offset=0, collect_headings=headings)
    ctx["headings"] = headings

    meta_bits = []
    if page.get("updated"):
        meta_bits.append("Mis à jour le %s" % fr_date(page["updated"]))
    if page.get("verified"):
        meta_bits.append(
            "Vérifié auprès des sources officielles le %s" % fr_date(page["verified"])
        )
    if page.get("author"):
        meta_bits.append("Par %s" % html.escape(str(page["author"])))
    if page.get("reviewer"):
        meta_bits.append("Relu par %s" % html.escape(str(page["reviewer"])))
    meta = (
        '<p class="art-meta">%s</p>' % " · ".join(meta_bits) if meta_bits else ""
    )

    toc = ""
    tops = [h for h in headings if h[0] == 2]
    if len(tops) >= 3:
        toc = (
            '<nav class="toc" aria-label="Sommaire"><p class="toc-h">Sur cette page</p>'
            "<ol>%s</ol></nav>"
            % "".join('<li><a href="#%s">%s</a></li>' % (hid, html.escape(txt)) for _, hid, txt in tops)
        )

    lede = '<p class="art-lede">%s</p>' % md.inline(page["lede"]) if page.get("lede") else ""

    answer_block = ""
    if page.get("answer"):
        answer_block = (
            '<div class="answer answer-inline"><p class="answer-k">En bref</p>%s</div>'
            % md.render(page["answer"], heading_offset=3)
        )

    return (
        '<article class="art"><div class="wrap art-grid">'
        '<div class="art-main"><header class="art-head"><h1>%s</h1>%s%s</header>'
        "%s<div class=\"prose\">%s</div>%s</div>"
        '<aside class="art-side">%s</aside>'
        "</div></article>"
        % (
            md.inline(page.get("title", "")),
            lede,
            meta,
            answer_block,
            body,
            render_page_sources(page),
            toc,
        )
    )


def render_page_sources(page):
    if not page.get("sources"):
        return ""
    items = "".join(
        '<li><a href="%s" target="_blank" rel="noopener">%s</a>%s</li>'
        % (
            html.escape(s.get("url", "#"), quote=True),
            html.escape(s.get("label", "")),
            " — <span class=\"src-note\">%s</span>" % html.escape(s["note"]) if s.get("note") else "",
        )
        for s in page["sources"]
    )
    return (
        '<section class="art-sources"><h2 id="sources">Sources</h2><ul class="sources">%s</ul>'
        '<p class="disclaimer">%s</p></section>'
        % (
            items,
            html.escape(
                page.get("disclaimer")
                or "CheckIA publie une information pédagogique. Les textes officiels et la "
                   "doctrine professionnelle font seuls foi ; le commissaire reste responsable "
                   "de l'appréciation applicable à sa mission."
            ),
        )
    )


def render_page(page, data, index):
    ctx = {"faq": [], "headings": []}
    crumb_html, crumb_schema = render_breadcrumb(page, index)

    if page.get("type") == "article":
        body = crumb_html + render_article_body(page, ctx)
        if page.get("sections"):
            body += sec.render_all(page["sections"], ctx)
    else:
        body = crumb_html + sec.render_all(page.get("sections", []), ctx)
        if page.get("_body", "").strip():
            body += sec.prose({"kind": "prose", "body": page["_body"]}, ctx)

    schema_html = build_schema(page, data, ctx, crumb_schema)
    head = render_head(page, data, schema_html)

    return (
        "<!doctype html><html lang=\"fr\"><head>%s</head><body>"
        '<a class="skip" href="#main">Aller au contenu</a>'
        '%s<main id="main">%s</main>%s'
        '<script src="/assets/site.js" defer></script>'
        "</body></html>"
    ) % (head, render_nav(data, page["url"]), body, render_footer(data))


# --------------------------------------------------------------------------- #
# site artefacts
# --------------------------------------------------------------------------- #

def build_sitemap(pages):
    urls = []
    for p in sorted(pages, key=lambda x: x["url"]):
        if p.get("noindex"):
            continue
        lastmod = str(p.get("updated") or date.today().isoformat())
        prio = p.get("priority")
        if prio is None:
            if p["url"] == "/":
                prio = "1.0"
            else:
                depth = len([s for s in p["url"].strip("/").split("/") if s])
                prio = {1: "0.8", 2: "0.6"}.get(depth, "0.5")
        urls.append(
            "  <url><loc>%s%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>"
            % (ORIGIN, p["url"], lastmod, prio)
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n'
        % "\n".join(urls)
    )


def build_robots():
    # The generator's own sources sit in the repo and GitHub Pages serves the
    # whole tree, so keep the Markdown sources out of the index to avoid
    # duplicate content competing with the rendered pages.
    return (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /content/\n"
        "Disallow: /lib/\n"
        "Disallow: /site/\n"
        "Disallow: /docs/\n"
        "Disallow: /Archive/\n\n"
        "Sitemap: %s/sitemap.xml\n" % ORIGIN
    )


def build_llms(pages, data):
    """A plain-text map of the site for answer engines.

    Not a substitute for crawlable HTML — every URL below is a real, fully
    rendered page. This just makes the structure legible at a glance.
    """
    org = data.get("organization", {})
    out = [
        "# CheckIA",
        "",
        "> %s" % org.get("description", ""),
        "",
        "CheckIA est une plateforme française de conduite et de production documentaire "
        "pour les missions de commissariat aux apports et de commissariat à la "
        "transformation. Le logiciel structure la mission et produit les documents ; "
        "le commissaire conserve le jugement, la validation et la responsabilité.",
        "",
    ]
    groups = {}
    for p in pages:
        if p.get("noindex"):
            continue
        groups.setdefault(p.get("group", "Pages"), []).append(p)
    for name in sorted(groups):
        out.append("## %s" % name)
        out.append("")
        for p in sorted(groups[name], key=lambda x: x["url"]):
            desc = (p.get("seo", {}) or {}).get("description", "")
            out.append("- [%s](%s%s): %s" % (p.get("title", ""), ORIGIN, p["url"], desc))
        out.append("")
    return "\n".join(out)


def build_redirect(target):
    """Static stub for a retired URL — GitHub Pages has no server redirects."""
    t = html.escape(target, quote=True)
    return (
        '<!doctype html><html lang="fr"><head><meta charset="utf-8">'
        '<title>Page déplacée</title><link rel="canonical" href="%s%s">'
        '<meta name="robots" content="noindex, follow">'
        '<meta http-equiv="refresh" content="0; url=%s"></head>'
        '<body><p>Cette page a été déplacée. <a href="%s">Continuer</a>.</p></body></html>'
        % (ORIGIN, t, t, t)
    )


# --------------------------------------------------------------------------- #
# integrity checks
# --------------------------------------------------------------------------- #

def check(pages, rendered, data):
    problems = []
    known = {p["url"] for p in pages}
    nav_targets = set()

    def walk_nav(items):
        for i in items:
            if i.get("href"):
                nav_targets.add(i["href"])
            for col in i.get("children", []) or []:
                for l in col.get("links", []):
                    nav_targets.add(l.get("href"))

    walk_nav(data.get("nav", []))
    for col in data.get("footer", {}).get("columns", []):
        for l in col.get("links", []):
            nav_targets.add(l.get("href"))

    # duplicate URLs and titles
    seen_url, seen_title, seen_desc = {}, {}, {}
    for p in pages:
        if p["url"] in seen_url:
            problems.append("URL en double : %s (%s / %s)" % (p["url"], seen_url[p["url"]], p["_source"]))
        seen_url[p["url"]] = p["_source"]
        t = (p.get("seo", {}) or {}).get("title")
        if t:
            if t in seen_title:
                problems.append("Title SEO en double : %r (%s / %s)" % (t, seen_title[t], p["_source"]))
            seen_title[t] = p["_source"]
        d = (p.get("seo", {}) or {}).get("description")
        if not d:
            problems.append("%s : meta description manquante" % p["_source"])
        elif d in seen_desc:
            problems.append("Meta description en double : %s / %s" % (seen_desc[d], p["_source"]))
        else:
            seen_desc[d] = p["_source"]
        if not t:
            problems.append("%s : title SEO manquant" % p["_source"])
        elif len(t) > 65:
            problems.append("%s : title SEO de %d caractères (>65)" % (p["_source"], len(t)))
        if d and len(d) > 165:
            problems.append("%s : meta description de %d caractères (>165)" % (p["_source"], len(d)))

    # internal links resolve, and one h1 per page
    inbound = {u: 0 for u in known}
    for p in pages:
        body = rendered[p["url"]]
        h1s = re.findall(r"<h1[ >]", body)
        if len(h1s) != 1:
            problems.append("%s : %d balises h1 (attendu : 1)" % (p["_source"], len(h1s)))
        for href in set(re.findall(r'href="(/[^"#?]*)"', body)):
            if href.startswith("/assets/"):
                continue
            if href not in known:
                problems.append("%s : lien interne mort → %s" % (p["_source"], href))
            elif href != p["url"]:
                inbound[href] += 1

    # noindex pages (the 404) are reached by the server, not by links.
    noindexed = {p["url"] for p in pages if p.get("noindex")}
    for url, count in sorted(inbound.items()):
        if count == 0 and url != "/" and url not in nav_targets and url not in noindexed:
            problems.append("Page orpheline (aucun lien entrant) : %s" % url)

    for target in sorted(t for t in nav_targets if t):
        if target.startswith("/") and target not in known:
            problems.append("Cible de navigation inexistante : %s" % target)

    return problems


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="run integrity checks only")
    args = ap.parse_args()

    data = load_data()
    pages = load_pages()
    index = {p["url"]: p for p in pages}

    rendered = {}
    for p in pages:
        rendered[p["url"]] = render_page(p, data, index)

    problems = check(pages, rendered, data)

    if args.check:
        _report(problems, pages)
        return 1 if problems else 0

    written = 0
    for p in pages:
        url = p["url"]
        if url == "/":
            out = os.path.join(ROOT, "index.html")
        elif url.endswith(".html"):
            # Pages that must live at an exact filename (GitHub Pages serves
            # /404.html for any unmatched path).
            out = os.path.join(ROOT, url.lstrip("/"))
            os.makedirs(os.path.dirname(out) or ROOT, exist_ok=True)
        else:
            outdir = os.path.join(ROOT, url.strip("/"))
            os.makedirs(outdir, exist_ok=True)
            out = os.path.join(outdir, "index.html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(rendered[url])
        written += 1

    # assets
    assets_src = os.path.join(SITE, "assets")
    assets_dst = os.path.join(ROOT, "assets")
    if os.path.isdir(assets_dst):
        shutil.rmtree(assets_dst)
    shutil.copytree(assets_src, assets_dst)

    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(build_sitemap(pages))
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(build_robots())
    open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write(build_llms(pages, data))

    for old, new in (data.get("redirects", {}) or {}).items():
        path = os.path.join(ROOT, old.lstrip("/"))
        os.makedirs(os.path.dirname(path) or ROOT, exist_ok=True)
        open(path, "w", encoding="utf-8").write(build_redirect(new))

    print("%d pages écrites, %d redirections, assets copiés." % (written, len(data.get("redirects", {}) or {})))
    _report(problems, pages)
    return 1 if problems else 0


def _report(problems, pages):
    if problems:
        print("\n%d problème(s) :" % len(problems))
        for p in problems:
            print("  - %s" % p)
    else:
        print("Contrôles d'intégrité : OK (%d pages)." % len(pages))


if __name__ == "__main__":
    sys.exit(main())
