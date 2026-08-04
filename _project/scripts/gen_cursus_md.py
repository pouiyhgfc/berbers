"""
Fase 3, Stap 3.2 — Generator: _ai/cursus.md  <-  nl/blok-1.html … nl/blok-8.html

Aangepast in fase F8 (bouwplan-cursus-uitvoering): de 38 lessen staan sinds de cutover
verspreid over acht blokpagina's (nl/blok-N.html), niet meer in nl/cursus.html (dat is nu
het gegenereerde overzicht — zie CLAUDE.md §"Bronmodel cursus"). Deze generator leest de
acht bestanden in blokvolgorde, vindt elke <section class="lesson"> en haalt het lesnummer
uit de <h2 id="les-NN">-anker daarbinnen (in plaats van een id op de section zelf).

Verliesloze herformatteerder: Tarifit komt LETTERLIJK uit elke <span class="tar"> en wordt
in `backticks` gezet zodat de round-trip-check de tokens terugvindt. De round-trip-check
loopt nu over de vereniging van alle acht bron-bestanden tegen de ene gegenereerde markdown.

Markdown-structuur per les:
    ## Les NN — <titel>
    *<eyebrow>*
    <lead, plat>
    <boekpagina, plat>
    #### <contextkop> / #### Kernwoorden / #### Dialoog / #### Verdieping: <titel>
    <zinnen als markdown-tabel `Tarifit | Nederlands`, kernwoorden als lijst>

Banner bovenaan (stap 3.4). Draaien:  python _project/scripts/gen_cursus_md.py
"""

import sys
from pathlib import Path

from bs4 import NavigableString, Tag

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _gen_common import (  # noqa: E402
    MarkdownDoc,
    banner,
    load_main,
    markdown_table,
    render_inline,
    tar_tokens_from_html,
    tar_tokens_from_markdown,
)

ROOT = Path(__file__).resolve().parents[2]
BLOK_BESTANDEN = [ROOT / "nl" / f"blok-{n}.html" for n in range(1, 9)]
OUT = ROOT / "_ai/cursus.md"

# Body-elementen die GEEN inhoud zijn (chrome) en worden overgeslagen.
SKIP_CLASSES = {"lesson-nav", "oefeningen"}


def render_zinnentabel_binnen(el: Tag) -> list[str]:
    """Zoekt de eerste <table> binnen el (evt. genest in een .tabelwrapper) en zet 'm om."""
    tabel = el.find("table")
    return markdown_table(tabel) if tabel else []


def render_zinnenblok(div: Tag, doc: MarkdownDoc) -> None:
    """.zinnenblok / .dialoog / .leesregels / .couplet: h3-kopjes + tabellen, of losse
    <p class="tar">/<p class="nl">-parenrijen (dialoog/leesregels/couplet hebben geen
    tabel)."""
    for child in div.find_all(recursive=False):
        if isinstance(child, Tag) and child.name == "h3":
            doc.add(f"#### {render_inline(child)}")
        elif isinstance(child, Tag) and child.name == "div" and "tabelwrapper" in (child.get("class") or []):
            lines = render_zinnentabel_binnen(child)
            if lines:
                doc.add("\n".join(lines))
        elif isinstance(child, Tag) and child.name == "table":
            lines = markdown_table(child)
            if lines:
                doc.add("\n".join(lines))
        elif isinstance(child, Tag) and child.name == "div" and (
            "dialoog-regel" in (child.get("class") or [])
        ):
            tar_p = child.find("p", class_="tar")
            nl_p = child.find("p", class_="nl")
            if tar_p and nl_p:
                doc.add(f"- {render_inline(tar_p)} — {render_inline(nl_p)}")
        elif isinstance(child, Tag) and child.name == "p" and "tar" in (child.get("class") or []):
            nl_p = child.find_next_sibling("p", class_="nl")
            if nl_p:
                doc.add(f"- {render_inline(child)} — {render_inline(nl_p)}")
        elif isinstance(child, Tag) and child.name == "div" and "couplet-scheiding" in (child.get("class") or []):
            doc.add_raw("")


def render_kernwoorden(div: Tag, doc: MarkdownDoc) -> None:
    h3 = div.find("h3")
    doc.add(f"#### {render_inline(h3) if h3 else 'Kernwoorden'}")
    for ul in div.find_all("ul", class_="kernwoorden-lijst", recursive=True):
        items = [f"- {render_inline(li)}" for li in ul.find_all("li", recursive=False)]
        if items:
            doc.add("\n".join(items))


def render_verdieping(details: Tag, doc: MarkdownDoc) -> None:
    summary = details.find("summary")
    doc.add(f"#### Verdieping: {render_inline(summary)}" if summary else "#### Verdieping")
    binnenblok = details.find("div", class_="zinnenblok")
    if binnenblok:
        render_zinnenblok(binnenblok, doc)


def render_body_element(el: Tag, doc: MarkdownDoc) -> None:
    if isinstance(el, NavigableString):
        return
    cls = el.get("class", []) or []
    if any(c in SKIP_CLASSES for c in cls):
        return
    name = el.name
    if name in ("!--",):
        return
    if name == "p":
        # Zowel de boekpagina-regel (class="source") als gewone proza-alinea's uit de
        # geschreven lesbody (schrijffase) — beide vlak overnemen, Tarifit in backticks.
        text = render_inline(el)
        if text:
            doc.add(text)
    elif name == "h3":
        doc.add(f"#### {render_inline(el)}")
    elif name == "h4":
        doc.add(f"##### {render_inline(el)}")
    elif name in ("ul", "ol"):
        ordered = name == "ol"
        items = []
        for i, li in enumerate(el.find_all("li", recursive=False), start=1):
            text = render_inline(li)
            items.append(f"{i}. {text}" if ordered else f"- {text}")
        if items:
            doc.add("\n".join(items))
    elif name == "table":
        lines = markdown_table(el)
        if lines:
            doc.add("\n".join(lines))
    elif name == "div" and "box" in cls:
        titel_el = el.find("div", class_="box-title")
        titel = render_inline(titel_el) if titel_el else ""
        delen = []
        for p in el.find_all("p", recursive=False):
            tekst = render_inline(p)
            if tekst:
                delen.append(tekst)
        inhoud = " ".join(delen)
        if titel and inhoud:
            doc.add(f"> **{titel}** — {inhoud}")
        elif inhoud:
            doc.add(f"> {inhoud}")
    elif name == "div" and "tabelwrapper" in cls:
        lines = render_zinnentabel_binnen(el)
        if lines:
            doc.add("\n".join(lines))
    elif name == "div" and "zinnenblok" in cls:
        render_zinnenblok(el, doc)
    elif name == "div" and cls and cls[0] in ("dialoog", "leesregels", "couplet"):
        render_zinnenblok(el, doc)
    elif name == "div" and "kernwoorden" in cls:
        render_kernwoorden(el, doc)
    elif name == "details" and "verdieping" in cls:
        render_verdieping(el, doc)
    # lesson-nav / oefeningen-container / overige chrome: bewust niets.


def render_section(section: Tag, doc: MarkdownDoc) -> bool:
    h2 = section.find("h2")
    les_id = (h2.get("id") or "").replace("les-", "") if h2 else ""
    if not les_id:
        return False
    eyebrow_el = section.find("div", class_="eyebrow")
    eyebrow = render_inline(eyebrow_el) if eyebrow_el else ""
    title = render_inline(h2) if h2 else les_id
    lead_el = section.find("p", class_="lead")
    lead = render_inline(lead_el) if lead_el else ""

    doc.add(f"## Les {les_id} — {title}".rstrip(" —"))
    if eyebrow:
        doc.add(f"*{eyebrow}*")
    if lead:
        doc.add(lead)
    doc.add("---")

    skip_until_body = {eyebrow_el, h2, lead_el}
    for child in section.find_all(recursive=False):
        if child in skip_until_body:
            continue
        render_body_element(child, doc)
    return True


def build_markdown(mains: list[Tag]) -> tuple[str, int]:
    doc = MarkdownDoc()
    doc.add_raw(banner("nl/blok-1.html … nl/blok-8.html", "gen_cursus_md.py"))
    n_lessons = 0
    for main in mains:
        for section in main.find_all("section", class_="lesson", recursive=True):
            if render_section(section, doc):
                n_lessons += 1
    return doc.render(), n_lessons


def roundtrip_check_multi(label: str, mains: list[Tag], generated_md: str) -> None:
    src: set[str] = set()
    for main in mains:
        src |= tar_tokens_from_html(main)
    out = tar_tokens_from_markdown(generated_md)
    print(f"  [{label}] Tarifit-tokens — bron-HTML: {len(src)} · gegenereerde md: {len(out)}")
    if src == out:
        print(f"  [{label}] ✓ round-trip OK — tokenverzamelingen identiek")
        return
    only_src = src - out
    only_out = out - src
    print(f"  [{label}] ✗ Tarifit-MISMATCH")
    if only_src:
        print(f"      alleen in bron ({len(only_src)}): {sorted(only_src)}")
    if only_out:
        print(f"      alleen in output ({len(only_out)}): {sorted(only_out)}")
    sys.exit(
        f"FOUT [{label}]: Tarifit round-trip mislukt "
        f"(alleen-bron={len(only_src)}, alleen-output={len(only_out)})."
    )


def main() -> None:
    mains = []
    for pad in BLOK_BESTANDEN:
        if not pad.exists():
            sys.exit(f"FOUT: {pad} ontbreekt (draai eerst `make bouw`)")
        _soup, m = load_main(pad)
        mains.append(m)
    md, n_lessons = build_markdown(mains)
    OUT.write_text(md, encoding="utf-8")
    print(f"Geschreven: {OUT.relative_to(ROOT)}  ({n_lessons} lessen)")
    roundtrip_check_multi("cursus", mains, md)


if __name__ == "__main__":
    main()
