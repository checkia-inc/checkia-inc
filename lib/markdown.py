"""Small Markdown renderer for editorial content.

Covers the subset the resource centre needs: headings (with auto slug anchors),
paragraphs, bold/italic/code, links, ordered and unordered lists, tables,
blockquotes, callouts, horizontal rules and fenced code. Emits semantic HTML
with heading ids so the table of contents and deep links work.

Dependency-free by design — see lib/frontmatter.py.
"""

import html
import re
import unicodedata

_INLINE_CODE = re.compile(r"`([^`]+)`")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_ITALIC = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)")


def slugify(text):
    text = re.sub(r"<[^>]+>", "", text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def inline(text):
    """Render inline markup. Escapes first, so content cannot inject HTML."""
    placeholders = []

    def stash(rendered):
        placeholders.append(rendered)
        return "\x00%d\x00" % (len(placeholders) - 1)

    def code_sub(m):
        return stash("<code>%s</code>" % html.escape(m.group(1)))

    text = _INLINE_CODE.sub(code_sub, text)
    text = html.escape(text, quote=False)

    def link_sub(m):
        label, href, title = m.group(1), m.group(2), m.group(3)
        external = href.startswith("http") and "checkia.fr" not in href
        attrs = ' target="_blank" rel="noopener"' if external else ""
        if title:
            attrs += ' title="%s"' % html.escape(title, quote=True)
        return '<a href="%s"%s>%s</a>' % (html.escape(href, quote=True), attrs, label)

    text = _LINK.sub(link_sub, text)
    text = _BOLD.sub(r"<strong>\1</strong>", text)
    text = _ITALIC.sub(r"<em>\1</em>", text)

    for i, rendered in enumerate(placeholders):
        text = text.replace("\x00%d\x00" % i, rendered)
    return text


def _table(rows):
    """rows: list of raw '| a | b |' lines, second row is the separator."""
    def cells(line):
        line = line.strip()
        if line.startswith("|"):
            line = line[1:]
        if line.endswith("|"):
            line = line[:-1]
        return [c.strip() for c in line.split("|")]

    head = cells(rows[0])
    body = [cells(r) for r in rows[2:]]
    out = ['<div class="table-scroll"><table>', "<thead><tr>"]
    out += ["<th>%s</th>" % inline(c) for c in head]
    out.append("</tr></thead><tbody>")
    for r in body:
        out.append("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def render(text, heading_offset=0, collect_headings=None):
    """Render markdown to HTML.

    heading_offset shifts heading levels (article bodies start at h2 under the
    page h1). collect_headings, if given a list, receives (level, id, text)
    tuples for building a table of contents.
    """
    lines = text.split("\n")
    out = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # fenced code
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            cls = ' class="lang-%s"' % html.escape(lang, quote=True) if lang else ""
            out.append(
                "<pre><code%s>%s</code></pre>" % (cls, html.escape("\n".join(buf)))
            )
            continue

        # horizontal rule
        if re.fullmatch(r"(-{3,}|\*{3,})", stripped):
            out.append("<hr>")
            i += 1
            continue

        # heading
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            level = min(6, len(m.group(1)) + heading_offset)
            raw = m.group(2).strip()
            hid = slugify(raw)
            if collect_headings is not None:
                collect_headings.append((level, hid, raw))
            out.append(
                '<h%d id="%s">%s</h%d>' % (level, hid, inline(raw), level)
            )
            i += 1
            continue

        # table
        if stripped.startswith("|") and i + 1 < n and re.match(
            r"^\|[\s:\-|]+\|$", lines[i + 1].strip()
        ):
            buf = []
            while i < n and lines[i].strip().startswith("|"):
                buf.append(lines[i])
                i += 1
            out.append(_table(buf))
            continue

        # blockquote / callout
        if stripped.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip())
                i += 1
            inner = render("\n".join(buf), heading_offset)
            first = buf[0] if buf else ""
            cm = re.match(r"^\[!(\w+)\]\s*(.*)$", first)
            if cm:
                kind = cm.group(1).lower()
                rest = buf[1:]
                if cm.group(2):
                    rest = [cm.group(2)] + rest
                inner = render("\n".join(rest), heading_offset)
                out.append(
                    '<aside class="callout callout-%s">%s</aside>' % (kind, inner)
                )
            else:
                out.append("<blockquote>%s</blockquote>" % inner)
            continue

        # ordered list
        if re.match(r"^\d+[.)]\s+", stripped):
            items = []
            while i < n and re.match(r"^\d+[.)]\s+", lines[i].strip()):
                items.append(re.sub(r"^\d+[.)]\s+", "", lines[i].strip()))
                i += 1
                # continuation lines
                while i < n and lines[i].startswith("   ") and lines[i].strip() and not re.match(r"^\d+[.)]\s+", lines[i].strip()):
                    items[-1] += " " + lines[i].strip()
                    i += 1
            out.append(
                "<ol>" + "".join("<li>%s</li>" % inline(x) for x in items) + "</ol>"
            )
            continue

        # unordered list
        if re.match(r"^[-*+]\s+", stripped):
            items = []
            while i < n and re.match(r"^[-*+]\s+", lines[i].strip()):
                items.append(re.sub(r"^[-*+]\s+", "", lines[i].strip()))
                i += 1
                while i < n and lines[i].startswith("  ") and lines[i].strip() and not re.match(r"^[-*+]\s+", lines[i].strip()):
                    items[-1] += " " + lines[i].strip()
                    i += 1
            out.append(
                "<ul>" + "".join("<li>%s</li>" % inline(x) for x in items) + "</ul>"
            )
            continue

        # paragraph
        buf = []
        while i < n and lines[i].strip() and not re.match(
            r"^(#{1,6}\s|[-*+]\s|\d+[.)]\s|>|\||```|---)", lines[i].strip()
        ):
            buf.append(lines[i].strip())
            i += 1
        if buf:
            out.append("<p>%s</p>" % inline(" ".join(buf)))

    return "\n".join(out)


def plain(text, limit=None):
    """Strip markup — used for meta descriptions and AI answer blocks."""
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = _LINK.sub(r"\1", text)
    text = re.sub(r"[*_#>|]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    if limit and len(text) > limit:
        cut = text[:limit].rsplit(" ", 1)[0]
        return cut + "…"
    return text
