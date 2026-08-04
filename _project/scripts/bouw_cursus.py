#!/usr/bin/env python3
"""
bouw_cursus.py — genereert nl/blok-N.html + nl/lezen.html en en/blok-N.html + en/lezen.html
uit bron/lessen/, bron/kaarten/ en bron/sjablonen/pagina-{nl,en}.html
(plan/BOUWPLAN-CURSUS-UITVOERING.md §6 + fase F7).

Implementeert §6 stappen 1 t/m 7, voor beide talen (stap 4/5 draaien twee keer — eenmaal
per taal — stap 1/2/6/7 zijn taalonafhankelijk: dezelfde claims/les-kolom gelden voor
NL en EN):
  1. lessen, kaarten en zinnen/woordenlijst/morfemen inlezen
  2. claims resolven -> zinnenlijst, kernwoorden, boekpagina per les
  3. (sjablonen zijn al bron: bron/sjablonen/pagina-nl.html, pagina-en.html)
  4. per blok+taal één pagina {taal}/blok-N.html renderen (§4.8-weergave, incl.
     dialoog/regel/couplet voor les 36/37/38 en een auto-verdieping-blok voor manifests
     met verdieping_zinnen). EN-lesbody komt uit bron/lessen/en/{id}.md; ontbreekt dat
     bestand, dan wordt de NL-body hergebruikt met een "vertaling volgt"-banner erboven
     (fase F7 — "pariteit van data is per constructie": dezelfde zinnen/kernwoorden,
     alleen de prozatekst kan achterlopen).
  5. {taal}/lezen.html + sidebar renderen
  6. zinnen.csv terugschrijven — alléén de kolom 'les' wijzigt (§4.5)
  7. bouwrapport naar stdout

R1/R2: dit script verzint geen Tarifit en kopieert alleen wat in de bron staat. De
EN-kolommen (zinnen.csv `en`, woordenlijst.csv `en`) zijn zelf al onderdeel van de bron —
er wordt niets vertaald, alleen een andere bestaande kolom gebruikt.
"""
from __future__ import annotations

import csv
import html.parser
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _bron_data import (  # noqa: E402
    ZINNEN_CSV,
    boekpagina,
    kernwoorden_auto,
    laad_morfemen,
    laad_woordenlijst,
    laad_zinnen,
    parse_tags,
    resolve_zinnen_grouped,
    woordenlijst_lemma_index,
)
from _manifest import Manifest, load_kaarten, load_lessen  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
LESSEN_DIR = REPO_ROOT / "bron" / "lessen"
LESSEN_EN_DIR = REPO_ROOT / "bron" / "lessen" / "en"
KAARTEN_DIR = REPO_ROOT / "bron" / "kaarten"
SJABLONEN_DIR = REPO_ROOT / "bron" / "sjablonen"

KERNWOORDEN_ZICHTBAAR = 12
VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

# Alle taalafhankelijke UI-labels (chrome, geen lescontent) op één plek. De contextstrings
# zelf (sectiekopjes in het zinnenblok) blijven bewust ongewijzigd tussen talen — dat zijn
# technische identifiers uit §5, geen proza.
LABELS = {
    "nl": {
        "dir": "nl",
        "overzicht_bestand": "cursus.html",
        "sidebar_titel": "De Cursus",
        "blok": "Blok",
        "les": "Les",
        "kaarten": "Kaarten",
        "naslagwerk": "Naslagwerk",
        "lezen": "Lezen",
        "woordenlijst": "Woordenlijst",
        "kernwoorden_kop": "Kernwoorden",
        "meer_kernwoorden": "Meer kernwoorden",
        "vorige_les": "← Vorige les",
        "volgende_les": "Volgende les",
        "boek_prefix": "boek p.",
        "verdieping": "Verdieping",
        "uitleg_bestand": "uitleg.html",
        "uitleg_label": "Uitleg",
        "vertaling_banner": None,
        "titel_blok": "Blok {blok} · Cursus · Tarifit",
        "titel_lezen": "Lezen · Cursus · Tarifit",
    },
    "en": {
        "dir": "en",
        "overzicht_bestand": "course.html",
        "sidebar_titel": "The Course",
        "blok": "Block",
        "les": "Lesson",
        "kaarten": "Reference cards",
        "naslagwerk": "Reference work",
        "lezen": "Reading",
        "woordenlijst": "Wordlist",
        "kernwoorden_kop": "Key words",
        "meer_kernwoorden": "More key words",
        "vorige_les": "← Previous lesson",
        "volgende_les": "Next lesson",
        "boek_prefix": "book p.",
        "verdieping": "In depth",
        "uitleg_bestand": "grammar.html",
        "uitleg_label": "Grammar",
        "vertaling_banner": "Translation pending — this lesson has not been translated into English yet.",
        "titel_blok": "Block {blok} · Course · Tarifit",
        "titel_lezen": "Reading · Course · Tarifit",
    },
}

# §9 F8 — cutover: oud-lesnummer (nl/cursus.html vóór de herstructurering) -> nieuw
# lesnummer, verbatim uit de "Oud→nieuw"-tabel in het plan. Bij een oude les die over
# meerdere nieuwe lessen verdeeld is, staat er de gekozen canonieke bestemming (§9: "kies").
OUD_NAAR_NIEUW = {
    "01": "02", "02": "03", "03": "03", "04": "05", "05": "01",
    "06": "06", "07": "06", "08": "06", "09": "07", "10": "09",
    "11": "08", "12": "11", "13": "12", "14": "14", "15": "15",
    "16": "13", "17": "19", "18": "23", "19": "13", "20": "17",
    "21": "21", "22": "22", "23": "29", "24": "25", "25": "26",
    "26": "27", "27": "09", "28": "16", "29": "18", "30": "17",
    "31": "04", "32": "32", "33": "33", "34": "30", "35": "31",
    "36": "37", "37": "36", "38": "37",
}


# ---------------------------------------------------------------------------
# §4.8 — zinnenblok
# ---------------------------------------------------------------------------

def humaniseer_context(waarde: str) -> str:
    """koppeltekens -> spaties, aanhalingstekens/apostrofs blijven staan (§4.8)."""
    return waarde.replace("-", " ")


def render_zinnen_tabel(rows: list[dict], taal: str) -> str:
    kop_vertaling = "Nederlands" if taal == "nl" else "English"
    regels = [
        '<div class="tabelwrapper">',
        '<table class="zinnen-tabel">',
        f"<thead><tr><th>Tarifit</th><th>{kop_vertaling}</th></tr></thead>",
        "<tbody>",
    ]
    for row in rows:
        tar = row.get("tarifit", "")
        vertaling = row.get(taal, "")
        regels.append(f'<tr><td class="tar">{tar}</td><td>{vertaling}</td></tr>')
    regels.append("</tbody></table>")
    regels.append("</div>")
    return "\n".join(regels)


def render_zinnen_dialoog(rows: list[dict], taal: str) -> str:
    """Les 36: dialoogweergave — om-en-om, sprekersregels, geen tabel (§4.8)."""
    delen = ['<div class="dialoog">']
    for i, row in enumerate(rows):
        spreker = "spreker-a" if i % 2 == 0 else "spreker-b"
        delen.append(f'<div class="dialoog-regel {spreker}">')
        delen.append(f'<p class="tar">{row.get("tarifit", "")}</p>')
        delen.append(f'<p class="nl">{row.get(taal, "")}</p>')
        delen.append("</div>")
    delen.append("</div>")
    return "\n".join(delen)


def render_zinnen_regel(rows: list[dict], taal: str) -> str:
    """Les 37: regel-voor-regel-weergave (§4.8)."""
    delen = ['<div class="leesregels">']
    for row in rows:
        delen.append(f'<p class="tar">{row.get("tarifit", "")}</p>')
        delen.append(f'<p class="nl">{row.get(taal, "")}</p>')
    delen.append("</div>")
    return "\n".join(delen)


def render_zinnen_couplet(rows: list[dict], taal: str) -> str:
    """Les 38: coupletweergave — groepen gescheiden door lege regel op paginawissel (§4.8)."""
    delen = ['<div class="couplet">']
    huidige_pagina = None
    for row in rows:
        zin_id = row.get("id") or ""
        pagina = zin_id[1:].split("-")[0] if zin_id.startswith("p") else None
        if huidige_pagina is not None and pagina != huidige_pagina:
            delen.append('<div class="couplet-scheiding"></div>')
        huidige_pagina = pagina
        delen.append(f'<p class="tar">{row.get("tarifit", "")}</p>')
        delen.append(f'<p class="nl">{row.get(taal, "")}</p>')
    delen.append("</div>")
    return "\n".join(delen)


WEERGAVE_PER_SLUG = {
    "dialogen": render_zinnen_dialoog,
    "sprookje": render_zinnen_regel,
    "izran": render_zinnen_couplet,
}


def render_zinnenblok(m: Manifest, groepen: list[tuple[str, str, list[dict]]], taal: str) -> str:
    speciaal = WEERGAVE_PER_SLUG.get(m.slug)
    if speciaal:
        rijen = [r for _s, _w, rows in groepen for r in rows]
        return speciaal(rijen, taal)
    delen = ['<div class="zinnenblok">']
    for soort, waarde, rows in groepen:
        if soort == "context":
            kop = humaniseer_context(waarde)
            delen.append(f"<h3>{kop}</h3>")
        delen.append(render_zinnen_tabel(rows, taal))
    delen.append("</div>")
    return "\n".join(delen)


# ---------------------------------------------------------------------------
# §4.3 — kernwoorden
# ---------------------------------------------------------------------------

def render_kernwoord_li(r: dict, taal: str) -> str:
    return (
        f'<li><span class="tar">{r["tarifit"]}</span> · {r[taal]} · '
        f'<span class="cefr-badge">{r["cefr"]}</span> · {r["thema"]}</li>'
    )


def render_kernwoordenblok(kernwoorden: list[dict], taal: str, labels: dict) -> str:
    if not kernwoorden:
        return '<div class="kernwoorden"></div>'
    zichtbaar = kernwoorden[:KERNWOORDEN_ZICHTBAAR]
    rest = kernwoorden[KERNWOORDEN_ZICHTBAAR:]
    delen = ['<div class="kernwoorden">', f"<h3>{labels['kernwoorden_kop']}</h3>", '<ul class="kernwoorden-lijst">']
    delen.extend(render_kernwoord_li(r, taal) for r in zichtbaar)
    delen.append("</ul>")
    if rest:
        delen.append(f"<details><summary>{labels['meer_kernwoorden']} ({len(rest)})</summary>")
        delen.append('<ul class="kernwoorden-lijst">')
        delen.extend(render_kernwoord_li(r, taal) for r in rest)
        delen.append("</ul></details>")
    delen.append("</div>")
    return "\n".join(delen)


# ---------------------------------------------------------------------------
# Lesbody: placeholders + ::: verdieping ... :::
# ---------------------------------------------------------------------------

VERDIEPING_RE = re.compile(r'::: verdieping "([^"]+)"\r?\n(.*?)\r?\n:::', re.S)


def render_body(body: str, placeholders: dict[str, str]) -> str:
    def verdieping_sub(m: re.Match) -> str:
        titel, inner = m.group(1), m.group(2)
        return f'<details class="verdieping"><summary>{titel}</summary>\n\n{_alinea_html(inner, placeholders)}\n\n</details>'

    body = VERDIEPING_RE.sub(verdieping_sub, body)
    return _alinea_html(body, placeholders)


def _alinea_blokken(tekst: str, placeholder_tokens: set[str]) -> list[str]:
    """Splitst op lege regels (alinea's) én dwingt een blokgrens af rond elke regel die
    exact een placeholder-token is — nodig omdat {{zinnen}}/{{kernwoorden}}/{{oefeningen}}
    in het sjabloon zonder tussenliggende lege regel op elkaar volgen (zie plan §3)."""
    blokken: list[str] = []
    huidig: list[str] = []
    for regel in tekst.split("\n"):
        gestript = regel.strip()
        if gestript in placeholder_tokens:
            if huidig:
                blokken.append("\n".join(huidig).strip())
                huidig = []
            blokken.append(gestript)
        elif gestript == "":
            if huidig:
                blokken.append("\n".join(huidig).strip())
                huidig = []
        else:
            huidig.append(regel)
    if huidig:
        blokken.append("\n".join(huidig).strip())
    return [b for b in blokken if b]


# Inline-markdown in lesbodies (schrijffase): `x` -> Tarifit-span, **x** -> strong,
# *x* -> em. Volgorde: eerst backticks (Tarifit mag * bevatten), dan vet, dan cursief.
_INLINE_TAR_RE = re.compile(r"`([^`\n]+)`")
# De afsluitende ** mag niet zelf door een * gevolgd worden: anders knipt "**vet met *cursief***"
# op de verkeerde plek en kruisen <strong> en <em> elkaar (ongeldige HTML).
_INLINE_STRONG_RE = re.compile(r"\*\*(.+?)\*\*(?!\*)")
_INLINE_EM_RE = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")


def _inline_md(tekst: str) -> str:
    """`x` -> Tarifit-span, **x** -> strong, *x* -> em.

    De inhoud van backticks wordt eerst apart gezet en pas op het eind teruggeplaatst.
    Anders lopen de vet/cursief-regels dwars door een Tarifit-vorm heen — de brondata
    gebruikt `*` voor gereconstrueerde vormen (`(< *zriɣ-t)`) en `<` voor afleidingen,
    en die mogen niet als markdown of als HTML-tag worden gelezen (R1).
    """
    bewaard: list[str] = []

    def _park(m: re.Match) -> str:
        bewaard.append(m.group(1))
        return f"\x00{len(bewaard) - 1}\x00"

    tekst = _INLINE_TAR_RE.sub(_park, tekst)
    tekst = _INLINE_STRONG_RE.sub(r"<strong>\1</strong>", tekst)
    tekst = _INLINE_EM_RE.sub(r"<em>\1</em>", tekst)

    def _herstel(m: re.Match) -> str:
        inhoud = bewaard[int(m.group(1))]
        veilig = inhoud.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f'<span class="tar">{veilig}</span>'

    return re.sub(r"\x00(\d+)\x00", _herstel, tekst)


def _md_tabel_html(regels: list[str]) -> str:
    """Markdown-pijptabel -> HTML-tabel in een .tabelwrapper (zelfde scroll-gedrag als de
    zinnentabellen). Rij 2 (|---|...) is de scheidingsregel en wordt overgeslagen."""
    rijen = []
    for regel in regels:
        cellen = [c.strip() for c in regel.strip().strip("|").split("|")]
        rijen.append(cellen)
    if len(rijen) >= 2 and all(set(c) <= set("-: ") for c in rijen[1]):
        kop, data = rijen[0], rijen[2:]
    else:
        kop, data = None, rijen
    delen = ['<div class="tabelwrapper">', "<table>"]
    if kop:
        delen.append("<thead><tr>" + "".join(f"<th>{_inline_md(c)}</th>" for c in kop) + "</tr></thead>")
    delen.append("<tbody>")
    for rij in data:
        delen.append("<tr>" + "".join(f"<td>{_inline_md(c)}</td>" for c in rij) + "</tr>")
    delen.append("</tbody></table>")
    delen.append("</div>")
    return "\n".join(delen)


_BOX_TITEL_RE = re.compile(r"^<strong>(.+?)</strong>\s*—\s*")


def _md_blok_html(blok: str) -> str:
    """Eén markdown-blok (alinea, kop, lijst, tabel of >-box) -> HTML."""
    regels = blok.split("\n")
    if blok.startswith("### "):
        return f'<h3 class="lesson-sub">{_inline_md(blok[4:].strip())}</h3>'
    if blok.startswith("#### "):
        return f"<h4>{_inline_md(blok[5:].strip())}</h4>"
    if all(r.lstrip().startswith(">") for r in regels):
        # "> **Titel** — tekst" -> box met titel; anders een kale box.
        inhoud = _inline_md(" ".join(r.lstrip().lstrip(">").strip() for r in regels))
        m = _BOX_TITEL_RE.match(inhoud)
        if m:
            rest = inhoud[m.end():]
            return (
                f'<div class="box tip"><div class="box-title">{m.group(1)}</div>'
                f'<p style="margin: 0;">{rest}</p></div>'
            )
        return f'<div class="box tip"><p style="margin: 0;">{inhoud}</p></div>'
    if all(r.lstrip().startswith("- ") for r in regels):
        items = "".join(f"<li>{_inline_md(r.lstrip()[2:].strip())}</li>" for r in regels)
        return f"<ul>{items}</ul>"
    if all(re.match(r"^\d+\.\s", r.lstrip()) for r in regels):
        genummerd = [re.sub(r"^\d+\.\s*", "", r.lstrip()) for r in regels]
        items = "".join(f"<li>{_inline_md(r)}</li>" for r in genummerd)
        return f"<ol>{items}</ol>"
    if all(r.lstrip().startswith("|") for r in regels):
        return _md_tabel_html(regels)
    return f"<p>{_inline_md(' '.join(r.strip() for r in regels))}</p>"


def _alinea_html(tekst: str, placeholders: dict[str, str]) -> str:
    out = []
    for blok in _alinea_blokken(tekst.strip(), set(placeholders.keys())):
        if blok in placeholders:
            out.append(placeholders[blok])
        elif blok.startswith("<!--") or blok.startswith("<"):
            out.append(blok)
        else:
            out.append(_md_blok_html(blok))
    return "\n\n".join(out)


def les_body_voor_taal(m: Manifest, taal: str, labels: dict) -> str:
    """NL: altijd de eigen body. EN: bron/lessen/en/{id}.md als dat bestaat, anders de
    NL-body met een banner erboven (F7: "vertaling volgt")."""
    if taal == "nl":
        return m.body
    en_pad = LESSEN_EN_DIR / f"{m.id}.md"
    if en_pad.exists():
        return en_pad.read_text(encoding="utf-8")
    banner = labels["vertaling_banner"]
    if not banner:
        return m.body
    return f'<p class="vertaling-banner">{banner}</p>\n\n{m.body}'


# ---------------------------------------------------------------------------
# Per-les sectie
# ---------------------------------------------------------------------------

def render_les_sectie(
    m: Manifest,
    groepen: list[tuple[str, str, list[dict]]],
    kernwoorden: list[dict],
    vorige: Manifest | None,
    volgende: Manifest | None,
    verdieping_groepen: list[tuple[str, str, list[dict]]] | None,
    taal: str,
    labels: dict,
) -> str:
    badge = f' <span class="badge badge-{m.status}">{m.status}</span>' if m.status != "af" else ""
    eyebrow = f"{labels['blok']} {m.blok} · {labels['les']} {m.id} · {m.status}"
    pagina = boekpagina([r for _s, _w, rows in groepen for r in rows], prefix=labels["boek_prefix"])
    zinnen_html = render_zinnenblok(m, groepen, taal)
    if verdieping_groepen:
        verdieping_inhoud = render_zinnenblok(m, verdieping_groepen, taal)
        zinnen_html += (
            f'\n\n<details class="verdieping"><summary>{labels["verdieping"]}</summary>'
            f"\n\n{verdieping_inhoud}\n\n</details>"
        )
    placeholders = {
        "{{zinnen}}": zinnen_html,
        "{{kernwoorden}}": render_kernwoordenblok(kernwoorden, taal, labels),
        "{{oefeningen}}": f'<div class="oefeningen" data-les="les-{m.id}"></div>',
    }
    body_html = render_body(les_body_voor_taal(m, taal, labels), placeholders)

    nav_delen = ['<div class="lesson-nav">']
    if vorige:
        nav_delen.append(f'<a href="#les-{vorige.id}"><span class="label">{labels["vorige_les"]}</span><span class="title">{vorige.titel}</span></a>')
    if volgende:
        nav_delen.append(f'<a href="#les-{volgende.id}" class="next"><span class="label">{labels["volgende_les"]}</span><span class="title">{volgende.titel} →</span></a>')
    nav_delen.append("</div>")
    nav_html = "\n".join(nav_delen)

    delen = [
        '<section class="lesson">',
        f'<div class="eyebrow">{eyebrow}{badge}</div>',
        f'<h2 id="les-{m.id}">{m.titel}</h2>',
    ]
    if m.doel:
        delen.append(f'<p class="lead">{m.doel}</p>')
    if pagina:
        delen.append(f'<p class="source">{pagina}</p>')
    if m.grammatica:
        links = " · ".join(
            f'<a href="{labels["uitleg_bestand"]}#{a}">§{a[1:].replace("-", ".")}</a>'
            for a in m.grammatica
        )
        delen.append(f'<p class="source">{labels["uitleg_label"]}: {links}</p>')
    delen.append(body_html)
    delen.append(nav_html)
    delen.append("</section>")
    return "\n".join(delen)


# ---------------------------------------------------------------------------
# Sidebar + blokpagina
# ---------------------------------------------------------------------------

def render_sidebar(lessen_per_blok: dict[str, list[Manifest]], kaarten: list[Manifest], labels: dict) -> str:
    delen = [f'<div class="sidebar-title">{labels["sidebar_titel"]}</div>']
    for blok in sorted(lessen_per_blok, key=lambda b: int(b)):
        delen.append('<div class="sidebar-section">')
        delen.append(f'<div class="sidebar-section-label">{labels["blok"]} {blok}</div>')
        for m in lessen_per_blok[blok]:
            badge = f' <span class="badge badge-{m.status}">{m.status}</span>' if m.status != "af" else ""
            delen.append(f'<a href="blok-{blok}.html#les-{m.id}"><span class="num">{m.id}</span> {m.titel}{badge}</a>')
        delen.append("</div>")
    if kaarten:
        delen.append('<div class="sidebar-section">')
        delen.append(f'<div class="sidebar-section-label">{labels["kaarten"]}</div>')
        for k in kaarten:
            delen.append(f'<a href="#{k.slug}"><span class="num">📖</span> {k.titel}</a>')
        delen.append("</div>")
    delen.append('<div class="sidebar-section">')
    delen.append(f'<div class="sidebar-section-label">{labels["naslagwerk"]}</div>')
    delen.append(f'<a href="lezen.html"><span class="num">📖</span> {labels["lezen"]}</a>')
    delen.append(f'<a href="woordenlijst.html"><span class="num">📖</span> {labels["woordenlijst"]}</a>')
    delen.append("</div>")
    return "\n".join(delen)


def render_pagina(sjabloon_pad: Path, titel: str, sidebar_html: str, inhoud_html: str) -> str:
    sjabloon = sjabloon_pad.read_text(encoding="utf-8")
    return (
        sjabloon
        .replace("{{TITEL}}", titel)
        .replace("{{SIDEBAR}}", sidebar_html)
        .replace("{{INHOUD}}", inhoud_html)
    )


# ---------------------------------------------------------------------------
# §9 F8 — overzichtspagina (cutover van nl/cursus.html + en/course.html)
# ---------------------------------------------------------------------------

def render_redirect_script(blok_van: dict[str, str]) -> str:
    """Vertaalt een oude #les-NN-hash (uit een bookmark of een cross-link vanuit
    oefeningen.html/exercises.html) naar de nieuwe blok-pagina + anker. Puur client-side:
    een #hash-fragment wordt nooit naar de server verstuurd, dus vercel.json kan dit niet
    (een redirects-regel op basis van een hash bestaat niet — zie WIJZIGINGEN/commit-notitie)."""
    return (
        '<script>\n'
        "  (function () {\n"
        r"    var m = location.hash.match(/^#les-(\d{2})$/);" "\n"
        "    if (!m) return;\n"
        f"    var oudNaarNieuw = {json.dumps(OUD_NAAR_NIEUW)};\n"
        f"    var blokVan = {json.dumps(blok_van)};\n"
        "    var nieuw = oudNaarNieuw[m[1]];\n"
        "    if (!nieuw) return;\n"
        "    var blok = blokVan[nieuw];\n"
        "    if (!blok) return;\n"
        '    location.replace("blok-" + blok + ".html#les-" + nieuw);\n'
        "  })();\n"
        "</script>"
    )


def render_overzicht(
    lessen_per_blok: dict[str, list[Manifest]],
    kaarten: list[Manifest],
    context_index: dict[str, list[dict]],
    id_index: dict[str, dict],
    taal: str,
    labels: dict,
) -> str:
    totaal_lessen = sum(len(v) for v in lessen_per_blok.values())
    totaal_zinnen = 0
    for blok_lessen in lessen_per_blok.values():
        for m in blok_lessen:
            for _s, _w, rows in resolve_zinnen_grouped(m, context_index, id_index):
                totaal_zinnen += len(rows)

    delen: list[str] = [render_redirect_script({m.id: m.blok for v in lessen_per_blok.values() for m in v})]
    delen.append(f'<div class="eyebrow">{labels["sidebar_titel"]}</div>')
    delen.append(f"<h1>{labels['sidebar_titel']}</h1>")
    delen.append(
        f'<p class="lead">{totaal_lessen} lessen · {len(lessen_per_blok)} '
        f'{"blokken" if taal == "nl" else "blocks"} · {totaal_zinnen} '
        f'{"zinnen" if taal == "nl" else "sentences"}</p>'
    )
    delen.append('<div class="overzicht-voortgang" data-overzicht-voortgang></div>')

    for blok in sorted(lessen_per_blok, key=lambda b: int(b)):
        delen.append('<section class="overzicht-blok">')
        delen.append(f'<h2>{labels["blok"]} {blok}</h2>')
        delen.append('<ul class="overzicht-lessen">')
        for m in lessen_per_blok[blok]:
            badge = f' <span class="badge badge-{m.status}">{m.status}</span>' if m.status != "af" else ""
            delen.append(
                f'<li><a href="blok-{blok}.html#les-{m.id}" class="overzicht-les-link">'
                f'<span class="num">{m.id}</span> {m.titel}{badge}</a></li>'
            )
        delen.append("</ul>")
        delen.append("</section>")

    if kaarten:
        delen.append('<section class="overzicht-blok">')
        delen.append(f'<h2>{labels["kaarten"]}</h2>')
        delen.append('<ul class="overzicht-lessen">')
        for k in kaarten:
            n = sum(len(rows) for _s, _w, rows in resolve_zinnen_grouped(k, context_index, id_index))
            telling = f" ({n} {'zinnen' if taal == 'nl' else 'sentences'})" if n else ""
            delen.append(f'<li><span class="num">📖</span> {k.titel}{telling}</li>')
        delen.append("</ul>")
        delen.append("</section>")

    delen.append('<section class="overzicht-blok">')
    delen.append(f'<h2>{labels["naslagwerk"]}</h2>')
    delen.append('<ul class="overzicht-lessen">')
    delen.append(f'<li><a href="lezen.html"><span class="num">📖</span> {labels["lezen"]}</a></li>')
    delen.append(f'<li><a href="woordenlijst.html"><span class="num">📖</span> {labels["woordenlijst"]}</a></li>')
    delen.append("</ul>")
    delen.append("</section>")

    return "\n".join(delen)


# ---------------------------------------------------------------------------
# HTML-geldigheid: geen onafgesloten tags
# ---------------------------------------------------------------------------

class _TagBalansChecker(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stack: list[str] = []
        self.fouten: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag not in VOID_ELEMENTS:
            self.stack.append(tag)

    def handle_startendtag(self, tag: str, attrs) -> None:
        pass

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID_ELEMENTS:
            return
        if tag not in self.stack:
            self.fouten.append(f"</{tag}> zonder openende tag")
            return
        while self.stack and self.stack[-1] != tag:
            self.fouten.append(f"onafgesloten tag: <{self.stack.pop()}>")
        if self.stack:
            self.stack.pop()


def controleer_html(label: str, html_tekst: str) -> None:
    checker = _TagBalansChecker()
    checker.feed(html_tekst)
    checker.close()
    for restant in reversed(checker.stack):
        checker.fouten.append(f"onafgesloten tag: <{restant}>")
    if checker.fouten:
        sys.exit(f"FOUT [{label}]: HTML niet geldig — " + "; ".join(checker.fouten))


# ---------------------------------------------------------------------------
# Eén taal renderen (stap 4 + 5)
# ---------------------------------------------------------------------------

def bouw_taal(
    taal: str,
    lessen_per_blok: dict[str, list[Manifest]],
    kaarten: list[Manifest],
    context_index: dict[str, list[dict]],
    id_index: dict[str, dict],
    lemma_index: dict[str, dict],
    geclaimde_ids: set[str],
) -> None:
    labels = LABELS[taal]
    sjabloon_pad = SJABLONEN_DIR / f"pagina-{taal}.html"
    if not sjabloon_pad.exists():
        sys.exit(f"FOUT: sjabloon {sjabloon_pad} ontbreekt")
    taal_dir = REPO_ROOT / labels["dir"]
    taal_dir.mkdir(parents=True, exist_ok=True)

    sidebar_html = render_sidebar(lessen_per_blok, kaarten, labels)

    for blok, blok_lessen in sorted(lessen_per_blok.items(), key=lambda kv: int(kv[0])):
        secties = []
        for i, m in enumerate(blok_lessen):
            groepen = resolve_zinnen_grouped(m, context_index, id_index)
            resolved = [r for _s, _w, rows in groepen for r in rows]
            kernwoorden = kernwoorden_auto(resolved, lemma_index)
            vorige = blok_lessen[i - 1] if i > 0 else None
            volgende = blok_lessen[i + 1] if i + 1 < len(blok_lessen) else None
            verdieping_groepen = None
            if m.raw.get("verdieping_zinnen"):
                verdieping_groepen = resolve_zinnen_grouped(m, context_index, id_index, zinnen_veld="verdieping_zinnen")
            secties.append(render_les_sectie(m, groepen, kernwoorden, vorige, volgende, verdieping_groepen, taal, labels))
        inhoud_html = "\n\n<!-- ============================================ -->\n\n".join(secties)
        titel = labels["titel_blok"].format(blok=blok)
        pagina_html = render_pagina(sjabloon_pad, titel, sidebar_html, inhoud_html)
        controleer_html(f"{labels['dir']}/blok-{blok}.html", pagina_html)
        doel = taal_dir / f"blok-{blok}.html"
        doel.write_text(pagina_html, encoding="utf-8")
        print(f"geschreven: {doel.relative_to(REPO_ROOT)} ({len(blok_lessen)} les(sen))")

    # Stap 5 — lezen.html: restregel, alle "text"-zinnen die geen les/kaart claimt.
    tekst_rows = [r for r in context_index.get("text", []) if r.get("id") not in geclaimde_ids]
    lezen_delen = ['<div class="leesboek">']
    huidige_pagina = None
    for row in tekst_rows:
        pagina_n = row["id"][1:].split("-")[0] if row.get("id", "").startswith("p") else None
        if pagina_n != huidige_pagina:
            if huidige_pagina is not None:
                lezen_delen.append("</div>")
            lezen_delen.append(f'<div class="leesboek-pagina" data-pagina="{pagina_n}">')
            huidige_pagina = pagina_n
        lezen_delen.append(f'<p class="tar">{row.get("tarifit", "")}</p>')
        lezen_delen.append(f'<p class="nl">{row.get(taal, "")}</p>')
    if huidige_pagina is not None:
        lezen_delen.append("</div>")
    lezen_delen.append("</div>")
    lezen_html = render_pagina(sjabloon_pad, labels["titel_lezen"], sidebar_html, "\n".join(lezen_delen))
    controleer_html(f"{labels['dir']}/lezen.html", lezen_html)
    (taal_dir / "lezen.html").write_text(lezen_html, encoding="utf-8")
    print(f"geschreven: {labels['dir']}/lezen.html ({len(tekst_rows)} zin(nen))")

    # §9 F8 — cutover: nl/cursus.html + en/course.html worden het gegenereerde overzicht.
    overzicht_inhoud = render_overzicht(lessen_per_blok, kaarten, context_index, id_index, taal, labels)
    overzicht_html = render_pagina(sjabloon_pad, labels["sidebar_titel"], sidebar_html, overzicht_inhoud)
    overzicht_pad = taal_dir / labels["overzicht_bestand"]
    controleer_html(f"{labels['dir']}/{labels['overzicht_bestand']}", overzicht_html)
    overzicht_pad.write_text(overzicht_html, encoding="utf-8")
    print(f"geschreven: {overzicht_pad.relative_to(REPO_ROOT)} (overzicht)")


# ---------------------------------------------------------------------------
# Hoofdprogramma
# ---------------------------------------------------------------------------

def main() -> int:
    lessen = load_lessen(LESSEN_DIR) if LESSEN_DIR.exists() else []
    kaarten = load_kaarten(KAARTEN_DIR)
    context_index, id_index = laad_zinnen()
    laad_morfemen()  # ingelezen conform §6 stap 1; gebruikt vanaf fase F5
    woordenlijst_rows = laad_woordenlijst()
    lemma_index = woordenlijst_lemma_index(woordenlijst_rows)

    lessen_per_blok: dict[str, list[Manifest]] = {}
    for m in lessen:
        if m.type == "kaart":
            continue
        lessen_per_blok.setdefault(str(m.blok), []).append(m)
    for blok_lessen in lessen_per_blok.values():
        blok_lessen.sort(key=lambda m: m.id)

    # Claims verzamelen (gebruikt door stap 5, 6 en het bouwrapport; taalonafhankelijk):
    # per zin-id de claimende lesnummers (§4.5: kolom les = laagste claimende lesnummer)
    # en, als geen enkele les claimt maar wel een kaart, de kaartslug.
    les_claims: dict[str, set[str]] = {}
    kaart_claims: dict[str, set[str]] = {}
    for m in lessen:
        velden = ["zinnen"] + (["verdieping_zinnen"] if m.raw.get("verdieping_zinnen") else [])
        for veld in velden:
            for _s, _w, rows in resolve_zinnen_grouped(m, context_index, id_index, zinnen_veld=veld):
                for r in rows:
                    if r.get("id"):
                        les_claims.setdefault(r["id"], set()).add(m.id)
    for m in kaarten:
        for _s, _w, rows in resolve_zinnen_grouped(m, context_index, id_index):
            for r in rows:
                if r.get("id"):
                    kaart_claims.setdefault(r["id"], set()).add(m.slug)

    geclaimde_ids: set[str] = set(les_claims) | set(kaart_claims)

    # Stap 4+5, per taal.
    for taal in ("nl", "en"):
        bouw_taal(taal, lessen_per_blok, kaarten, context_index, id_index, lemma_index, geclaimde_ids)

    # Stap 6 — zinnen.csv terugschrijven: alléén de kolom 'les' wijzigt (§4.5).
    with ZINNEN_CSV.open(encoding="utf-8-sig", newline="") as f:
        alle_rijen = list(csv.reader(f))
    header, csv_rijen = alle_rijen[0], alle_rijen[1:]
    les_kolom = header.index("les")
    tags_kolom = header.index("tags")
    for rij in csv_rijen:
        tags = parse_tags(rij[tags_kolom])
        zin_id = tags.get("id")
        context = tags.get("context")
        if zin_id in les_claims:
            rij[les_kolom] = min(les_claims[zin_id])
        elif zin_id in kaart_claims:
            rij[les_kolom] = min(kaart_claims[zin_id])
        elif context == "text":
            rij[les_kolom] = "leesboek"
        else:
            rij[les_kolom] = "buiten-cursus"
    with ZINNEN_CSV.open("w", encoding="utf-8", newline="") as f:
        schrijver = csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator="\r\n")
        schrijver.writerow(header)
        schrijver.writerows(csv_rijen)
    print(f"geschreven: {ZINNEN_CSV.relative_to(REPO_ROOT)} (kolom 'les' bijgewerkt)")

    # Stap 7 — bouwrapport.
    print()
    print("bouwrapport:")
    for m in sorted(lessen, key=lambda m: m.id):
        groepen = resolve_zinnen_grouped(m, context_index, id_index)
        resolved = [r for _s, _w, rows in groepen for r in rows]
        kernwoorden = kernwoorden_auto(resolved, lemma_index)
        extra = ""
        if m.raw.get("verdieping_zinnen"):
            vg = resolve_zinnen_grouped(m, context_index, id_index, zinnen_veld="verdieping_zinnen")
            extra = f" (+{sum(len(rows) for _s, _w, rows in vg)} verdieping)"
        en_status = "vertaald" if (LESSEN_EN_DIR / f"{m.id}.md").exists() else "vertaling volgt"
        print(f"  les {m.id} ({m.slug}): {len(resolved)} zin(nen){extra}, {len(kernwoorden)} kernwoord(en), status {m.status}, EN: {en_status}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
