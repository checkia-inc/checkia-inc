"""Minimal YAML-subset parser for content frontmatter.

Deliberately not a full YAML implementation. Supports exactly what the content
layer needs: nested maps, lists (of scalars and of maps), quoted and bare
scalars, block scalars (`|` and `>`), booleans, ints, null and comments.

Kept dependency-free so the site builds with a bare `python3` — no npm, no pip.
"""

import re


def _scalar(raw):
    s = raw.strip()
    if not s:
        return ""
    if s[0] in "\"'" and len(s) > 1 and s[-1] == s[0]:
        return s[1:-1]
    low = s.lower()
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
        return False
    if low in ("null", "~"):
        return None
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    if re.fullmatch(r"-?\d*\.\d+", s):
        return float(s)
    # inline flow list: [a, b, c]
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return []
        return [_scalar(p) for p in _split_flow(inner)]
    return s


def _split_flow(s):
    """Split a flow-list body on commas that are not inside quotes."""
    parts, buf, quote = [], [], None
    for ch in s:
        if quote:
            if ch == quote:
                quote = None
            buf.append(ch)
        elif ch in "\"'":
            quote = ch
            buf.append(ch)
        elif ch == ",":
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    parts.append("".join(buf))
    return [p for p in parts if p.strip()]


def _indent_of(line):
    return len(line) - len(line.lstrip(" "))


class _Reader:
    def __init__(self, lines):
        self.lines = lines
        self.i = 0

    def peek(self):
        while self.i < len(self.lines):
            line = self.lines[self.i]
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                self.i += 1
                continue
            return line
        return None

    def next(self):
        line = self.peek()
        if line is not None:
            self.i += 1
        return line


def _parse_block_scalar(reader, parent_indent, style):
    """Consume an indented block following a `|` or `>` marker."""
    out = []
    while reader.i < len(reader.lines):
        line = reader.lines[reader.i]
        if not line.strip():
            out.append("")
            reader.i += 1
            continue
        if _indent_of(line) <= parent_indent:
            break
        out.append(line)
        reader.i += 1
    if not out:
        return ""
    body = [ln for ln in out]
    # strip the common indentation
    widths = [_indent_of(ln) for ln in body if ln.strip()]
    strip = min(widths) if widths else 0
    body = [ln[strip:] if ln.strip() else "" for ln in body]
    while body and not body[-1]:
        body.pop()
    if style == "|":
        return "\n".join(body)
    # folded: blank line = paragraph break, otherwise join with a space
    paras, cur = [], []
    for ln in body:
        if ln:
            cur.append(ln)
        else:
            if cur:
                paras.append(" ".join(cur))
            cur = []
    if cur:
        paras.append(" ".join(cur))
    return "\n\n".join(paras)


def _parse_value_inline(reader, indent, raw):
    """Resolve the text after `key:` — inline scalar, block scalar, or nested."""
    raw = raw.strip()
    if raw in ("|", "|-", ">", ">-"):
        return _parse_block_scalar(reader, indent, raw[0])
    if raw:
        return _scalar(raw)
    nxt = reader.peek()
    if nxt is None or _indent_of(nxt) <= indent:
        return ""
    if nxt.strip().startswith("- "):
        return _parse_list(reader, _indent_of(nxt))
    return _parse_map(reader, _indent_of(nxt))


def _parse_list(reader, indent):
    items = []
    while True:
        line = reader.peek()
        if line is None or _indent_of(line) != indent or not line.strip().startswith("-"):
            break
        reader.next()
        body = line.strip()[1:].strip()
        if not body:
            nxt = reader.peek()
            if nxt is not None and _indent_of(nxt) > indent:
                if nxt.strip().startswith("- "):
                    items.append(_parse_list(reader, _indent_of(nxt)))
                else:
                    items.append(_parse_map(reader, _indent_of(nxt)))
            else:
                items.append("")
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):(.*)$", body)
        if m:
            # a map starts on the dash line; its keys sit at indent + 2
            key, rest = m.group(1), m.group(2)
            child_indent = indent + 2
            item = {key: _parse_value_inline(reader, child_indent, rest)}
            while True:
                nxt = reader.peek()
                if nxt is None or _indent_of(nxt) != child_indent:
                    break
                if nxt.strip().startswith("- "):
                    break
                reader.next()
                m2 = re.match(r"^([A-Za-z0-9_-]+):(.*)$", nxt.strip())
                if not m2:
                    break
                item[m2.group(1)] = _parse_value_inline(
                    reader, child_indent, m2.group(2)
                )
            items.append(item)
        else:
            items.append(_scalar(body))
    return items


def _parse_map(reader, indent):
    out = {}
    while True:
        line = reader.peek()
        if line is None or _indent_of(line) != indent:
            break
        if line.strip().startswith("- "):
            break
        reader.next()
        m = re.match(r"^([A-Za-z0-9_./-]+):(.*)$", line.strip())
        if not m:
            continue
        out[m.group(1)] = _parse_value_inline(reader, indent, m.group(2))
    return out


def parse(text):
    """Parse a frontmatter block into a dict."""
    lines = text.replace("\t", "  ").split("\n")
    reader = _Reader(lines)
    first = reader.peek()
    if first is None:
        return {}
    return _parse_map(reader, _indent_of(first))


def split(raw):
    """Split a content file into (frontmatter dict, body string)."""
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            fm = raw[raw.find("\n") + 1 : end]
            body = raw[end + 4 :].lstrip("\n")
            return parse(fm), body
    return {}, raw
