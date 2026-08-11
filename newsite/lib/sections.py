"""Section renderers for structured (landing / hub) pages.

A page's frontmatter declares an ordered list of sections; each has a `kind`
that maps to one function here. Adding a new layout means adding one function
and one registry entry — no page template is ever copy-pasted.
"""

import html as _html

from . import markdown as md
from . import visuals


def _esc(s):
    return _html.escape(str(s or ""), quote=True)


def _rich(s):
    """Inline markdown for short strings (titles, ledes, cell text)."""
    return md.inline(str(s or ""))


def _ctas(items, align=""):
    if not items:
        return ""
    out = []
    for c in items:
        style = c.get("style", "primary")
        cls = {
            "primary": "btn btn-primary",
            "ghost": "btn btn-ghost",
            "white": "btn btn-white",
            "link": "btn-link",
        }.get(style, "btn btn-primary")
        out.append(
            '<a class="%s" href="%s">%s</a>' % (cls, _esc(c.get("href", "/demo/")), _rich(c.get("label", "")))
        )
    return '<div class="btn-row %s">%s</div>' % (align, "".join(out))


def _section(inner, s, extra_cls=""):
    cls = ["sec"]
    if s.get("tone"):
        cls.append("sec-%s" % s["tone"])
    if extra_cls:
        cls.append(extra_cls)
    if s.get("class"):
        cls.append(s["class"])
    sid = ' id="%s"' % _esc(s["id"]) if s.get("id") else ""
    return '<section class="%s"%s><div class="wrap">%s</div></section>' % (
        " ".join(cls),
        sid,
        inner,
    )


def _head(s, centered=False):
    """Eyebrow + heading + lede, shared by most sections."""
    parts = []
    if s.get("eyebrow"):
        parts.append('<p class="eyebrow">%s</p>' % _rich(s["eyebrow"]))
    if s.get("title"):
        parts.append("<h2>%s</h2>" % _rich(s["title"]))
    if s.get("lede"):
        parts.append('<p class="lede">%s</p>' % _rich(s["lede"]))
    if not parts:
        return ""
    return '<div class="sec-head%s">%s</div>' % (
        " sec-head-c" if centered else "",
        "".join(parts),
    )


# --------------------------------------------------------------------------- #
# sections
# --------------------------------------------------------------------------- #

def hero(s, ctx):
    parts = ['<div class="hero-copy">']
    if s.get("eyebrow"):
        parts.append('<p class="badge">%s</p>' % _rich(s["eyebrow"]))
    parts.append("<h1>%s</h1>" % _rich(s.get("title", "")))
    if s.get("lede"):
        parts.append('<p class="hero-lede">%s</p>' % _rich(s["lede"]))
    if s.get("note"):
        parts.append('<p class="hero-note">%s</p>' % _rich(s["note"]))
    parts.append(_ctas(s.get("ctas")))
    if s.get("proof"):
        parts.append(
            '<ul class="hero-proof">%s</ul>'
            % "".join("<li>%s</li>" % _rich(p) for p in s["proof"])
        )
    parts.append("</div>")
    if s.get("visual"):
        parts.append('<div class="hero-visual">%s</div>' % visuals.get(s["visual"]))
    return '<section class="hero"><div class="wrap hero-grid">%s</div></section>' % "".join(parts)


def trust(s, ctx):
    items = "".join('<li>%s</li>' % _rich(i) for i in s.get("items", []))
    return '<section class="trust"><div class="wrap"><ul class="trust-list">%s</ul></div></section>' % items


def answer(s, ctx):
    """Answer-first block: the direct response an answer engine can lift."""
    inner = []
    q = s.get("question")
    if q:
        inner.append("<h2>%s</h2>" % _rich(q))
    inner.append('<div class="answer-body">%s</div>' % md.render(s.get("body", ""), heading_offset=2))
    if s.get("points"):
        inner.append(
            '<ul class="answer-points">%s</ul>'
            % "".join("<li>%s</li>" % _rich(p) for p in s["points"])
        )
    return _section('<div class="answer">%s</div>' % "".join(inner), s, "sec-answer")


def cards(s, ctx):
    cols = s.get("columns", 3)
    out = []
    for c in s.get("items", []):
        body = ['<article class="card">']
        if c.get("eyebrow"):
            body.append('<p class="card-eyebrow">%s</p>' % _rich(c["eyebrow"]))
        if c.get("title"):
            body.append("<h3>%s</h3>" % _rich(c["title"]))
        if c.get("body"):
            body.append("<p>%s</p>" % _rich(c["body"]))
        if c.get("points"):
            body.append(
                "<ul>%s</ul>" % "".join("<li>%s</li>" % _rich(p) for p in c["points"])
            )
        if c.get("href"):
            body.append(
                '<a class="card-link" href="%s">%s</a>'
                % (_esc(c["href"]), _rich(c.get("link_label", "En savoir plus")))
            )
        body.append("</article>")
        out.append("".join(body))
    grid = '<div class="grid grid-%d">%s</div>' % (cols, "".join(out))
    return _section(_head(s) + grid, s)


def steps(s, ctx):
    out = []
    for idx, st in enumerate(s.get("items", []), 1):
        out.append(
            '<li class="step"><span class="step-n" aria-hidden="true">%d</span>'
            '<div class="step-body"><h3>%s</h3><p>%s</p>%s</div></li>'
            % (
                idx,
                _rich(st.get("title", "")),
                _rich(st.get("body", "")),
                '<p class="step-meta">%s</p>' % _rich(st["meta"]) if st.get("meta") else "",
            )
        )
    return _section(_head(s) + '<ol class="steps">%s</ol>' % "".join(out), s)


def split(s, ctx):
    left = ['<div class="split-copy">', _head(s)]
    if s.get("body"):
        left.append(md.render(s["body"], heading_offset=2))
    if s.get("points"):
        left.append(
            '<ul class="ticks">%s</ul>'
            % "".join("<li>%s</li>" % _rich(p) for p in s["points"])
        )
    left.append(_ctas(s.get("ctas")))
    left.append("</div>")
    right = ""
    if s.get("visual"):
        right = '<div class="split-visual">%s</div>' % visuals.get(s["visual"])
    elif s.get("panel"):
        p = s["panel"]
        rows = "".join(
            "<li><span>%s</span><span>%s</span></li>" % (_rich(r.get("k", "")), _rich(r.get("v", "")))
            for r in p.get("rows", [])
        )
        right = (
            '<div class="split-visual"><div class="panel">'
            '<p class="panel-title">%s</p><ul class="panel-rows">%s</ul></div></div>'
            % (_rich(p.get("title", "")), rows)
        )
    order = " split-rev" if s.get("reverse") else ""
    return _section('<div class="split%s">%s%s</div>' % (order, "".join(left), right), s)


def visual(s, ctx):
    cap = '<p class="fig-cap">%s</p>' % _rich(s["caption"]) if s.get("caption") else ""
    return _section(
        _head(s, centered=True) + '<figure class="fig">%s%s</figure>' % (visuals.get(s.get("name", "")), cap),
        s,
    )


def table(s, ctx):
    head = "".join("<th>%s</th>" % _rich(h) for h in s.get("head", []))
    rows = "".join(
        "<tr>%s</tr>" % "".join("<td>%s</td>" % _rich(c) for c in r)
        for r in s.get("rows", [])
    )
    t = (
        '<div class="table-scroll"><table><thead><tr>%s</tr></thead>'
        "<tbody>%s</tbody></table></div>" % (head, rows)
    )
    note = '<p class="table-note">%s</p>' % _rich(s["note"]) if s.get("note") else ""
    return _section(_head(s) + t + note, s)


def prose(s, ctx):
    body = md.render(s.get("body", ""), heading_offset=1, collect_headings=ctx.get("headings"))
    return _section(_head(s) + '<div class="prose">%s</div>' % body, s)


def faq(s, ctx):
    out = []
    for item in s.get("items", []):
        out.append(
            "<details class=\"faq-item\"><summary><span>%s</span></summary>"
            '<div class="faq-a">%s</div></details>'
            % (_rich(item.get("q", "")), md.render(item.get("a", ""), heading_offset=3))
        )
        ctx.setdefault("faq", []).append(
            (md.plain(item.get("q", "")), md.plain(item.get("a", "")))
        )
    return _section(_head(s) + '<div class="faq">%s</div>' % "".join(out), s)


def links(s, ctx):
    out = []
    for l in s.get("items", []):
        out.append(
            '<a class="linkcard" href="%s"><span class="linkcard-k">%s</span>'
            "<span class=\"linkcard-t\">%s</span><span class=\"linkcard-d\">%s</span></a>"
            % (
                _esc(l.get("href", "/")),
                _rich(l.get("eyebrow", "")),
                _rich(l.get("title", "")),
                _rich(l.get("body", "")),
            )
        )
    return _section(
        _head(s) + '<div class="linkgrid">%s</div>' % "".join(out), s
    )


def quote(s, ctx):
    return _section(
        '<figure class="pull"><blockquote>%s</blockquote>'
        '<figcaption>%s</figcaption></figure>'
        % (_rich(s.get("body", "")), _rich(s.get("source", ""))),
        s,
    )


def cta(s, ctx):
    inner = ['<div class="ctablock">']
    if s.get("eyebrow"):
        inner.append('<p class="eyebrow">%s</p>' % _rich(s["eyebrow"]))
    inner.append("<h2>%s</h2>" % _rich(s.get("title", "")))
    if s.get("lede"):
        inner.append("<p>%s</p>" % _rich(s["lede"]))
    inner.append(_ctas(s.get("ctas") or [{"label": "Réserver une démonstration", "href": "/demo/"}]))
    inner.append("</div>")
    return _section("".join(inner), s, "sec-cta")


def sources(s, ctx):
    out = []
    for src in s.get("items", []):
        label = _rich(src.get("label", ""))
        url = src.get("url")
        note = ' — <span class="src-note">%s</span>' % _rich(src["note"]) if src.get("note") else ""
        if url:
            out.append(
                '<li><a href="%s" target="_blank" rel="noopener">%s</a>%s</li>'
                % (_esc(url), label, note)
            )
        else:
            out.append("<li>%s%s</li>" % (label, note))
    return _section(
        _head(s) + '<ul class="sources">%s</ul>' % "".join(out), s, "sec-sources"
    )


REGISTRY = {
    "hero": hero,
    "trust": trust,
    "answer": answer,
    "cards": cards,
    "steps": steps,
    "split": split,
    "visual": visual,
    "table": table,
    "prose": prose,
    "faq": faq,
    "links": links,
    "quote": quote,
    "cta": cta,
    "sources": sources,
}


def render_all(section_list, ctx):
    out = []
    for s in section_list or []:
        fn = REGISTRY.get(s.get("kind"))
        if not fn:
            raise ValueError("unknown section kind: %r" % s.get("kind"))
        out.append(fn(s, ctx))
    return "\n".join(out)
