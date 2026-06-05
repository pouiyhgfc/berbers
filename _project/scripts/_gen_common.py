"""
Gedeelde machinerie voor de HTML→markdown-generatoren (stap 3.2):
gen_cursus_md.py en gen_grammatica_md.py.

Bevat:
  * BANNER_TEMPLATE en banner()        — de "niet met de hand bewerken"-kop (stap 3.4).
  * tar_tokens()                       — de canonieke Tarifit-tokenizer (één definitie voor
                                         zowel de bron-HTML als de gegenereerde markdown), zodat
                                         de round-trip-check appels met appels vergelijkt.
  * tar_tokens_from_html()             — tokens uit alle <span class="tar"> in <main class="content">.
  * tar_tokens_from_markdown()         — tokens uit alle `inline-code`-backticks in de markdown.
  * roundtrip_check()                  — vergelijkt beide verzamelingen; faalt (SystemExit) bij verschil.
  * render_inline()                    — inline-HTML → platte tekst, met Tarifit in `backticks`.
  * markdown_table()                   — een <table> → markdown-tabel.
  * MarkdownDoc                         — kleine builder voor blokken met nette lege regels.

Harde regel (plan + conventies): een generator is een verliesloze herformatteerder. Hij neemt
elke `tar`-vorm LETTERLIJK over uit de span en synthetiseert nooit Tarifit. Verdwijnt of verschijnt
een token, dan faalt de round-trip-check.
"""

import re
import sys
import unicodedata

from bs4 import BeautifulSoup, NavigableString, Tag

# ---------------------------------------------------------------------------
# Banner (stap 3.4)
# ---------------------------------------------------------------------------

BANNER_TEMPLATE = (
    "<!-- AUTO-GEGENEREERD uit {src} door _project/scripts/{script}\n"
    "     NIET met de hand bewerken. Bewerk de bron en draai `make build`. "
    "Zie WIJZIGINGEN.md. -->"
)


def banner(src: str, script: str) -> str:
    return BANNER_TEMPLATE.format(src=src, script=script)


# ---------------------------------------------------------------------------
# Tarifit-tokenizer — één definitie voor beide kanten van de round-trip
# ---------------------------------------------------------------------------

# Edge-leestekens die we van de RAND van een token strippen. Bewust géén '(' ')' '/' '-' :
# die zitten binnenin echte Tarifit-vormen (bv. xa(d), m(u)-, bu-/m(u)-, ad-) en mogen niet weg.
# '[' en ']' zijn groeperingshaken om frasen heen → wél van de rand strippen.
_EDGE_PUNCT = set('"“”„‘’,.;:?!…·→—–~[]')


def _strip_edges(token: str) -> str:
    return token.strip("".join(_EDGE_PUNCT))


def tar_tokens(text: str) -> set[str]:
    """
    Canonieke Tarifit-tokenverzameling uit een stuk tekst (inhoud van één of meer tar-spans,
    of de tekst tussen backticks in de markdown). Splitst op whitespace, normaliseert
    rand-leestekens en Unicode (NFC), laat lege/puur-leesteken-tokens vallen.

    Deze functie is met OPZET identiek voor HTML en markdown — alleen zo vergelijkt de
    round-trip-check dezelfde normalisatie aan beide kanten.
    """
    tokens: set[str] = set()
    for raw in text.split():
        tok = _strip_edges(unicodedata.normalize("NFC", raw))
        if tok and any(ch.isalpha() for ch in tok):
            tokens.add(tok)
    return tokens


def tar_tokens_from_html(main: Tag) -> set[str]:
    """Alle Tarifit-tokens uit <span class="tar"> binnen het meegegeven <main>-element."""
    tokens: set[str] = set()
    for span in main.find_all("span", class_="tar"):
        tokens |= tar_tokens(span.get_text())
    return tokens


# Inline-code in de gegenereerde markdown: `...` (geen drie-backtick codeblokken in onze output).
_BACKTICK_RE = re.compile(r"`([^`\n]+)`")
# De banner is een HTML-commentaar en bevat zelf backticks (`make build`); die tellen NIET mee.
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


def tar_tokens_from_markdown(md: str) -> set[str]:
    """Alle Tarifit-tokens uit `inline-code`-backticks in de gegenereerde markdown.

    De banner-commentaar wordt eerst verwijderd zodat de backticks daarin (`make build`)
    geen valse tokens opleveren.
    """
    body = _HTML_COMMENT_RE.sub("", md)
    tokens: set[str] = set()
    for m in _BACKTICK_RE.finditer(body):
        tokens |= tar_tokens(m.group(1))
    return tokens


def roundtrip_check(label: str, src_main: Tag, generated_md: str) -> None:
    """
    Verplichte round-trip-check (stap 3.2 deel 3): de Tarifit-tokenverzameling uit de bron-HTML
    moet exact gelijk zijn aan die uit de gegenereerde markdown. Bij verschil: print het verschil
    en faal hard (SystemExit), zodat een verdwenen of bijgekomen token de build stopt.
    """
    src = tar_tokens_from_html(src_main)
    out = tar_tokens_from_markdown(generated_md)
    only_src = src - out
    only_out = out - src
    print(f"  [{label}] Tarifit-tokens — bron-HTML: {len(src)} · gegenereerde md: {len(out)}")
    if src == out:
        print(f"  [{label}] ✓ round-trip OK — tokenverzamelingen identiek")
        return
    print(f"  [{label}] ✗ Tarifit-MISMATCH")
    if only_src:
        print(f"      alleen in bron ({len(only_src)}): {sorted(only_src)}")
    if only_out:
        print(f"      alleen in output ({len(only_out)}): {sorted(only_out)}")
    sys.exit(
        f"FOUT [{label}]: Tarifit round-trip mislukt "
        f"(alleen-bron={len(only_src)}, alleen-output={len(only_out)})."
    )


# ---------------------------------------------------------------------------
# Inline-rendering: HTML-fragment → platte tekst, Tarifit in `backticks`
# ---------------------------------------------------------------------------

_INLINE_DROP = {"em", "strong", "u", "code", "abbr", "i", "b"}  # markup strippen, tekst behouden


_SPACE_BEFORE_PUNCT_RE = re.compile(r"\s+([,.;:!?])")


def _clean(text: str) -> str:
    text = " ".join(text.split())
    # Cosmetisch: geen spatie vóór gewone zinsleestekens (ontstaat door spatie-gepadde inline-tags).
    # Tarifit zelf wordt niet aangeraakt — dit raakt alleen prozaleestekens buiten de backticks.
    return _SPACE_BEFORE_PUNCT_RE.sub(r"\1", text)


def render_inline(node) -> str:
    """
    Zet de inline-inhoud van een element om naar platte tekst:
      * <span class="tar">...</span>  → `...`  (Tarifit letterlijk, in inline-code-backticks)
      * <br>                          → spatie
      * <em>/<strong>/<u>/<code>      → markup weg, tekst behouden (huidige _ai-stijl)
      * <a>                           → linktekst + (href) als de href naar een pagina wijst
      * losse tekstknopen             → letterlijk
    Whitespace wordt genormaliseerd naar enkele spaties.
    """
    parts: list[str] = []
    for child in getattr(node, "children", []):
        if isinstance(child, NavigableString):
            parts.append(str(child))
        elif isinstance(child, Tag):
            cls = child.get("class", []) or []
            if child.name == "span" and "tar" in cls:
                # Tarifit LETTERLIJK; backticks maken het token terugvindbaar voor de round-trip.
                inner = _clean(child.get_text())
                parts.append(f" `{inner}` " if inner else "")
            elif child.name == "br":
                parts.append(" ")
            elif child.name == "a":
                parts.append(_render_anchor(child))
            elif child.name in _INLINE_DROP:
                parts.append(" " + render_inline(child) + " ")
            else:
                parts.append(render_inline(child))
    return _clean("".join(parts))


def _render_anchor(a: Tag) -> str:
    text = _clean(render_inline(a))
    href = (a.get("href") or "").strip()
    if href and not href.startswith("#") and href != "#":
        return f" {text} ({href}) "
    return f" {text} "


# ---------------------------------------------------------------------------
# Tabellen
# ---------------------------------------------------------------------------


def markdown_table(table: Tag) -> list[str]:
    """Een <table> → markdown-tabelregels. Cellen via render_inline (Tarifit in backticks)."""
    header: list[str] = []
    thead = table.find("thead")
    if thead:
        hr = thead.find("tr")
        if hr:
            header = [_cell(c) for c in hr.find_all(["th", "td"])]

    body_rows: list[list[str]] = []
    body = table.find("tbody") or table
    for tr in body.find_all("tr"):
        if thead and tr.find_parent("thead"):
            continue
        cells = [_cell(c) for c in tr.find_all(["th", "td"])]
        if cells:
            body_rows.append(cells)

    if not header and body_rows:
        # Geen thead: gebruik de eerste rij als kop (komt zelden voor, maar houdt de tabel geldig).
        header, body_rows = body_rows[0], body_rows[1:]

    width = max([len(header)] + [len(r) for r in body_rows], default=0)
    if width == 0:
        return []

    def pad(row: list[str]) -> list[str]:
        return row + [""] * (width - len(row))

    lines = ["| " + " | ".join(pad(header)) + " |"]
    lines.append("| " + " | ".join(["---"] * width) + " |")
    for r in body_rows:
        lines.append("| " + " | ".join(pad(r)) + " |")
    return lines


def _cell(c: Tag) -> str:
    return render_inline(c).replace("|", "\\|")


# ---------------------------------------------------------------------------
# Markdown-builder
# ---------------------------------------------------------------------------


class MarkdownDoc:
    """Verzamelt blokken en plakt ze met precies één lege regel ertussen aan elkaar."""

    def __init__(self) -> None:
        self._blocks: list[str] = []

    def add(self, block: str) -> None:
        block = block.rstrip("\n")
        if block:
            self._blocks.append(block)

    def add_raw(self, block: str) -> None:
        """Voeg toe zonder lege regel te forceren (de builder doet de scheiding alsnog)."""
        self._blocks.append(block.rstrip("\n"))

    def render(self) -> str:
        return "\n\n".join(self._blocks).rstrip() + "\n"


def load_main(path) -> tuple[BeautifulSoup, Tag]:
    """Parse een HTML-bestand en geef (soup, <main class="content">). Faalt als main ontbreekt."""
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "lxml")
    main = soup.find("main", class_="content")
    if main is None:
        sys.exit(f"FOUT: geen <main class=\"content\"> in {path}")
    return soup, main
