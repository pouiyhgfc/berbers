"""
Fase 3, Stap 3.2 — Generator: _ai/grammatica.md  <-  nl/uitleg.html

Verliesloze herformatteerder: leest <main class="content"> uit nl/uitleg.html, loopt over de
20 <section id="hN">-blokken in documentvolgorde en reproduceert die in de bestaande
markdown-kopstructuur van _ai/grammatica.md. Tarifit komt LETTERLIJK uit elke <span class="tar">
en wordt in `backticks` gezet zodat de round-trip-check de tokens terugvindt.

Markdown-structuur per hoofdstuk (zoals de bestaande _ai/grammatica.md):
    ## <h1-titel>
    📖 Boek p. X        (alleen als er een <p class="source"> bovenaan is)
    *<lead, cursief>*    (alleen als er een lead is)
    ---
    ### <h1-titel>
    *<lead, cursief>*
    <body: <h2> → ###, <h3> → ####, alinea's, lijsten, tabellen, > box-blokken>

De koppen lopen in de body één niveau "dieper" dan in cursus.html: in uitleg.html is een
sub(hoofd)stuk een <h2> (→ ###) en een sub-subkop een <h3> (→ ####).

Banner bovenaan (stap 3.4). Round-trip-check verplicht (stap 3.2 deel 3).
Draaien:  python _project/scripts/gen_grammatica_md.py
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
SRC = ROOT / "nl/uitleg.html"
OUT = ROOT / "_ai/grammatica.md"


def render_box(div: Tag) -> str:
    """<div class="box[ tip|warn]"> → blockquote met vette titel (titel krijgt een dubbele punt)."""
    title_el = div.find("div", class_="box-title")
    title = render_inline(title_el) if title_el else ""
    body_parts: list[str] = []
    for child in div.children:
        if not isinstance(child, Tag) or child is title_el:
            continue
        if child.name == "p":
            body_parts.append(render_inline(child))
        elif child.name in ("ul", "ol"):
            body_parts.extend(render_inline(li) for li in child.find_all("li", recursive=False))
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
    return "\n".join(f"> {ln}" if ln else ">" for ln in text.split("\n"))


def render_list(lst: Tag) -> str:
    ordered = lst.name == "ol"
    out: list[str] = []
    for i, li in enumerate(lst.find_all("li", recursive=False), start=1):
        text = render_inline(li)
        out.append(f"{i}. {text}" if ordered else f"- {text}")
    return "\n".join(out)


def render_tables_in(el: Tag, doc: MarkdownDoc) -> None:
    """Render elke <table> binnen een wrapper-div (uitleg.html stopt tabellen soms in een
    <div style="overflow-x:auto;">)."""
    for tbl in el.find_all("table"):
        lines = markdown_table(tbl)
        if lines:
            doc.add("\n".join(lines))


def render_body_element(el: Tag, doc: MarkdownDoc) -> None:
    cls = el.get("class", []) or []
    name = el.name
    if name == "p" and "source" in cls:
        # Een paginareferentie midden in de body (bv. onder een subkop) → letterlijk overnemen.
        text = render_inline(el)
        if text:
            doc.add(text)
        return
    if name == "h2":
        doc.add(f"### {render_inline(el)}")
    elif name == "h3":
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
        render_tables_in(el, doc)
    # hr (sectie-afsluiter) en overige chrome: bewust niets.


def chapter_heading(section: Tag, title: str) -> str:
    """De ## kop. uitleg.html draagt de hoofdstuknaam al volledig in de <h1> ("Hoofdstuk 1 — ..."),
    dus we nemen die titel letterlijk over."""
    return f"## {title}"


def render_section(section: Tag, doc: MarkdownDoc) -> None:
    children = [c for c in section.find_all(recursive=False)]
    h1 = section.find("h1", recursive=False)
    title = render_inline(h1) if h1 else section.get("id", "")

    # Intro = de <p class="source"> (paginaref) en <p class="lead"> die vóór de eerste body-kop
    # (h2/h3) staan. Latere source/lead horen bij de body en lopen via render_body_element.
    intro_source_el = None
    intro_lead_el = None
    for child in children:
        if child is h1:
            continue
        if child.name in ("h2", "h3", "h4"):
            break  # body begint
        cls = child.get("class", []) or []
        if child.name == "p" and "source" in cls and intro_source_el is None:
            intro_source_el = child
        elif child.name == "p" and "lead" in cls and intro_lead_el is None:
            intro_lead_el = child

    source = render_inline(intro_source_el) if intro_source_el else ""
    lead = render_inline(intro_lead_el) if intro_lead_el else ""

    doc.add(chapter_heading(section, title))
    if source:
        doc.add(source)
    if lead:
        doc.add(f"*{lead}*")
    doc.add("---")
    doc.add(f"### {title}")
    if lead:
        doc.add(f"*{lead}*")

    handled = {h1, intro_source_el, intro_lead_el}
    for child in children:
        if child in handled:
            continue
        render_body_element(child, doc)


def build_markdown(main: Tag) -> tuple[str, int]:
    doc = MarkdownDoc()
    doc.add_raw(banner("nl/uitleg.html", "gen_grammatica_md.py"))
    sections = [s for s in main.find_all("section", recursive=True) if (s.get("id") or "").startswith("h")]
    for section in sections:
        render_section(section, doc)
    return doc.render(), len(sections)


def main() -> None:
    soup, main = load_main(SRC)
    md, n = build_markdown(main)
    OUT.write_text(md, encoding="utf-8")
    print(f"Geschreven: {OUT.relative_to(ROOT)}  ({n} hoofdstukken/secties)")
    roundtrip_check("grammatica", main, md)


if __name__ == "__main__":
    main()
