"""
Fase 3, Stap 3.2 — Generator: _ai/cursus.md  <-  nl/cursus.html

Verliesloze herformatteerder: leest <main class="content"> uit nl/cursus.html, loopt over de
36 <section id="les-NN">-blokken in documentvolgorde en reproduceert die in de bestaande
markdown-kopstructuur van _ai/cursus.md. Tarifit komt LETTERLIJK uit elke <span class="tar">
en wordt in `backticks` gezet zodat de round-trip-check de tokens terugvindt.

Markdown-structuur per les (zoals de bestaande _ai/cursus.md):
    ## Les NN — <titel>
    *<eyebrow>*                 (les NN · niveau N)
    <lead, plat>
    **Links:** <crosslinks>     (alleen als er crosslinks zijn)
    ---
    ### <titel>
    *<lead, cursief>*
    <body: #### subkoppen, alinea's, lijsten, tabellen, > box-blokken>

Banner bovenaan (stap 3.4). Round-trip-check verplicht (stap 3.2 deel 3).
Draaien:  python _project/scripts/gen_cursus_md.py
"""

import sys
from pathlib import Path

from bs4 import Tag

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _gen_common import (  # noqa: E402
    MarkdownDoc,
    banner,
    load_main,
    markdown_table,
    render_inline,
    roundtrip_check,
)

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "nl/cursus.html"
OUT = ROOT / "_ai/cursus.md"

# Body-elementen die GEEN inhoud zijn (chrome) en worden overgeslagen.
SKIP_CLASSES = {"crosslinks", "lesson-oef-link", "lesson-nav"}


def render_box(div: Tag) -> str:
    """<div class="box[ tip|warn]"> → blockquote met vette titel (titel krijgt een dubbele punt)."""
    lines: list[str] = []
    title_el = div.find("div", class_="box-title")
    title = render_inline(title_el) if title_el else ""
    body_parts: list[str] = []
    for child in div.children:
        if not isinstance(child, Tag):
            continue
        if child is title_el:
            continue
        if child.name == "p":
            body_parts.append(render_inline(child))
        elif child.name in ("ul", "ol"):
            body_parts.extend(render_list_inline(child))
        else:
            txt = render_inline(child)
            if txt:
                body_parts.append(txt)
    body = " ".join(p for p in body_parts if p).strip()
    if title and body:
        text = f"**{title}:** {body}"
    elif title:
        text = f"**{title}**"
    else:
        text = body
    for ln in text.split("\n"):
        lines.append(f"> {ln}" if ln else ">")
    return "\n".join(lines)


def render_list_inline(lst: Tag) -> list[str]:
    """Lijst-items als platte zinnen (voor binnen een box-blockquote)."""
    return [render_inline(li) for li in lst.find_all("li", recursive=False)]


def render_list(lst: Tag) -> str:
    ordered = lst.name == "ol"
    out: list[str] = []
    for i, li in enumerate(lst.find_all("li", recursive=False), start=1):
        text = render_inline(li)
        out.append(f"{i}. {text}" if ordered else f"- {text}")
    return "\n".join(out)


def render_body_element(el: Tag, doc: MarkdownDoc) -> None:
    """Eén body-element (binnen een les, ná de lead) → markdown-blok in `doc`."""
    cls = el.get("class", []) or []
    if any(c in SKIP_CLASSES for c in cls):
        return
    name = el.name
    if name == "h3":
        # Gewone subkop én lesson-sub ("1. ...") worden allebei een #### subkop.
        doc.add(f"#### {render_inline(el)}")
    elif name == "h4":
        doc.add(f"##### {render_inline(el)}")
    elif name == "p":
        text = render_inline(el)
        if text:
            doc.add(text)
    elif name in ("ul", "ol"):
        doc.add(render_list(el))
    elif name == "table":
        lines = markdown_table(el)
        if lines:
            doc.add("\n".join(lines))
    elif name == "div" and "box" in cls:
        doc.add(render_box(el))
    elif name in ("div", "figure"):
        # Onbekende wrapper: dook erin voor tabellen/inhoud (bv. overflow-wrappers).
        for inner in el.find_all(["table"], recursive=False):
            lines = markdown_table(inner)
            if lines:
                doc.add("\n".join(lines))
    # hr / nav / overige chrome: bewust niets.


def render_crosslinks(section: Tag) -> str:
    """<div class="crosslinks"> → '**Links:** label naam (href) · ...'."""
    block = section.find("div", class_="crosslinks")
    if not block:
        return ""
    parts: list[str] = []
    for a in block.find_all("a", recursive=False):
        href = (a.get("href") or "").strip()
        label_el = a.find("div", class_="crosslabel")
        name_el = a.find("div", class_="crossname")
        label = render_inline(label_el) if label_el else ""
        name = render_inline(name_el) if name_el else ""
        piece = " ".join(p for p in (label, name) if p)
        if href:
            piece = f"{piece} ({href})"
        parts.append(piece.strip())
    if not parts:
        return ""
    return "**Links:** " + " · ".join(parts)


def render_section(section: Tag, doc: MarkdownDoc) -> None:
    eyebrow_el = section.find("div", class_="eyebrow")
    eyebrow = render_inline(eyebrow_el) if eyebrow_el else ""
    h2 = section.find("h2")
    title = render_inline(h2) if h2 else (eyebrow or section.get("id", ""))
    lead_el = section.find("p", class_="lead")
    lead = render_inline(lead_el) if lead_el else ""

    # Koptekst van de les
    doc.add(f"## Les {section.get('id', '').replace('les-', '')} — {title}".rstrip(" —"))
    if eyebrow:
        doc.add(f"*{eyebrow}*")
    if lead:
        doc.add(lead)
    crosslinks = render_crosslinks(section)
    if crosslinks:
        doc.add(crosslinks)
    doc.add("---")
    doc.add(f"### {title}")
    if lead:
        doc.add(f"*{lead}*")

    # Body: alle directe kinderen ná de eyebrow/h2/lead, behalve chrome.
    skip_until_body = {eyebrow_el, h2, lead_el}
    for child in section.find_all(recursive=False):
        if child in skip_until_body:
            continue
        render_body_element(child, doc)


def build_markdown(main: Tag) -> str:
    doc = MarkdownDoc()
    doc.add_raw(banner("nl/cursus.html", "gen_cursus_md.py"))
    sections = main.find_all("section", recursive=True)
    lessons = [s for s in sections if (s.get("id") or "").startswith("les-")]
    for section in lessons:
        render_section(section, doc)
    return doc.render(), len(lessons)


def main() -> None:
    soup, main = load_main(SRC)
    md, n_lessons = build_markdown(main)
    OUT.write_text(md, encoding="utf-8")
    print(f"Geschreven: {OUT.relative_to(ROOT)}  ({n_lessons} lessen)")
    roundtrip_check("cursus", main, md)


if __name__ == "__main__":
    main()
