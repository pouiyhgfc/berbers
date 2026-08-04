#!/usr/bin/env python3
"""
check_bronnen.py — validator voor bron/lessen, bron/kaarten en bron/selecties tegen
assets/zinnen/zinnen.csv en assets/woordenlijst/woordenlijst.csv.

Implementeert alle punten 1-8 uit plan/BOUWPLAN-CURSUS-UITVOERING.md §7:
  1. elk manifest parsebaar; id uniek en gelijk aan bestandsnaam; blok in 1-8
  2. elke contextstring bestaat exact in zinnen.csv (anders: fout + 3 suggesties)
  3. elke selectie-id bestaat; selectiebestanden bestaan
  4. elke les >=3 zinnen tenzij status: dun; type: kaart vrijgesteld
  5. elk grammatica:-anker bestaat na gen_ankers.py in nl/uitleg.html
  6. Tarifit-in-proza-regel (§4.4)
  7. kernwoorden-expliciete lemma's bestaan in woordenlijst
  8. woordenlijst-header exact + cefr/thema-domeinen

Faalt hard (exit 1) met een lijst van concrete vindplaatsen; nooit stil doorbouwen (R3).
"""
from __future__ import annotations

import csv
import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _bron_data import laad_morfemen, tarifit_tokens  # noqa: E402
from _manifest import Manifest, ManifestError, load_manifest  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
LESSEN_DIR = REPO_ROOT / "bron" / "lessen"
KAARTEN_DIR = REPO_ROOT / "bron" / "kaarten"
SELECTIES_DIR = REPO_ROOT / "bron" / "selecties"
ZINNEN_CSV = REPO_ROOT / "assets" / "zinnen" / "zinnen.csv"
WOORDENLIJST_CSV = REPO_ROOT / "assets" / "woordenlijst" / "woordenlijst.csv"
UITLEG_HTML = REPO_ROOT / "nl" / "uitleg.html"

ANKER_ID_RE = re.compile(r'<h[23]\s+id="(s\d+(?:-\d+)*)"')

# §4.4 — detectieset voor "vrij Tarifit in proza".
TAR_CHARS = "ḏṯřǧčɛɣƔḥṛṣṭẓḍạẹịụʷ"
PLACEHOLDER_TOKENS = {"{{zinnen}}", "{{kernwoorden}}", "{{oefeningen}}"}
VERDIEPING_KOP_RE = re.compile(r'^::: verdieping ".*"$')
BACKTICK_RE = re.compile(r"`([^`]+)`")
_TOKEN_RANDTEKENS = '.,;:!?()«»„“”"\'-…'

WOORDENLIJST_HEADER = ["tarifit", "nl", "en", "cefr", "woordsoort", "thema", "tags"]
CEFR_DOMEIN = {"A1", "A2", "B1", "B2"}
THEMA_DOMEIN = {
    "dieren", "eigenschappen & kleuren", "eten & drinken", "familie & mensen",
    "functiewoorden", "gereedschap & materiaal", "getallen & hoeveelheid",
    "gevoel & denken", "gezondheid", "handel & geld", "handelingen",
    "huis & huishouden", "kleding & sieraad", "landbouw & veeteelt & visserij",
    "lichaam", "muziek & kunst", "natuur & weer", "overig",
    "plaats & richting & geografie", "religie & leven-dood", "samenleving & volken",
    "taal & school & communicatie", "tijd", "vervoer & reizen",
    "werk & beroep & ambacht",
}


class Fouten:
    def __init__(self) -> None:
        self.items: list[str] = []

    def add(self, msg: str) -> None:
        self.items.append(msg)

    def __bool__(self) -> bool:
        return bool(self.items)

    def __len__(self) -> int:
        return len(self.items)


def parse_tags(tags: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in tags.split(";"):
        part = part.strip()
        if not part or ":" not in part:
            continue
        k, _, v = part.partition(":")
        out[k.strip()] = v.strip()
    return out


def laad_zinnen() -> tuple[dict[str, list[dict]], dict[str, dict]]:
    """Geeft (context_index, id_index) van assets/zinnen/zinnen.csv."""
    if not ZINNEN_CSV.exists():
        sys.exit(f"FOUT: {ZINNEN_CSV} ontbreekt")
    context_index: dict[str, list[dict]] = {}
    id_index: dict[str, dict] = {}
    with ZINNEN_CSV.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            tags = parse_tags(row.get("tags", ""))
            zin_id = tags.get("id")
            context = tags.get("context")
            entry = {**row, "id": zin_id, "context": context}
            if zin_id:
                id_index[zin_id] = entry
            if context:
                context_index.setdefault(context, []).append(entry)
    return context_index, id_index


def laad_woordenlijst() -> tuple[list[dict], Fouten]:
    fouten = Fouten()
    if not WOORDENLIJST_CSV.exists():
        sys.exit(f"FOUT: {WOORDENLIJST_CSV} ontbreekt")
    with WOORDENLIJST_CSV.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != WOORDENLIJST_HEADER:
            fouten.add(
                f"woordenlijst.csv: header is {reader.fieldnames}, verwacht {WOORDENLIJST_HEADER}"
            )
        rows = []
        for i, r in enumerate(reader, start=2):
            rows.append(r)
            if r["cefr"] not in CEFR_DOMEIN:
                fouten.add(f"woordenlijst.csv regel {i}: cefr '{r['cefr']}' niet in {sorted(CEFR_DOMEIN)}")
            if r["thema"] not in THEMA_DOMEIN:
                fouten.add(f"woordenlijst.csv regel {i}: thema '{r['thema']}' niet in de 25 toegestane thema's")
    return rows, fouten


def laad_ankers() -> set[str]:
    """Alle s{n1}-{n2}(-{n3}) §-ankers die gen_ankers.py in nl/uitleg.html heeft gezet."""
    if not UITLEG_HTML.exists():
        sys.exit(f"FOUT: {UITLEG_HTML} ontbreekt (draai eerst gen_ankers.py)")
    html = UITLEG_HTML.read_text(encoding="utf-8")
    return set(ANKER_ID_RE.findall(html))


def check_grammatica(m: Manifest, ankers: set[str], fouten: Fouten) -> None:
    for anker in m.grammatica:
        if anker in ankers:
            continue
        hoofdstuk = anker.split("-")[0]
        beschikbaar = sorted(a for a in ankers if a.split("-")[0] == hoofdstuk)
        fouten.add(
            f"{m.path.name}: grammatica-anker '{anker}' bestaat niet in nl/uitleg.html "
            f"— beschikbaar in hoofdstuk {hoofdstuk}: {beschikbaar}"
        )


def woordenlijst_lemma_set(rows: list[dict]) -> set[str]:
    lemmas: set[str] = set()
    for r in rows:
        for variant in r["tarifit"].split(" / "):
            lemmas.add(variant.strip().lower())
    return lemmas


def check_manifest_basis(m: Manifest, fouten: Fouten, gezien_ids: dict[str, Path]) -> None:
    if m.type == "kaart":
        # Kaartbestanden hebben geen numerieke id-prefix: bron/kaarten/<slug>.md.
        if m.path.name != f"{m.slug}.md":
            fouten.add(f"{m.path.name}: slug '{m.slug}' komt niet overeen met bestandsnaam")
    else:
        verwacht_prefix = f"{m.path.name[:2]}-"
        if not m.path.name.startswith(f"{m.id}-"):
            fouten.add(f"{m.path.name}: id '{m.id}' komt niet overeen met bestandsnaam (verwacht prefix '{verwacht_prefix}')")
    if m.id in gezien_ids and gezien_ids[m.id] != m.path:
        fouten.add(f"{m.path.name}: id '{m.id}' is niet uniek (ook in {gezien_ids[m.id].name})")
    else:
        gezien_ids[m.id] = m.path
    if m.status not in {"af", "concept", "dun"}:
        fouten.add(f"{m.path.name}: status '{m.status}' niet in {{af, concept, dun}}")
    if m.type != "kaart":
        if m.blok is None:
            fouten.add(f"{m.path.name}: veld 'blok' ontbreekt")
        else:
            try:
                blok_n = int(m.blok)
            except ValueError:
                blok_n = None
            if blok_n is None or not (1 <= blok_n <= 8):
                fouten.add(f"{m.path.name}: blok '{m.blok}' niet in 1..8")


def dichtstbijzijnde(context: str, alle_contexts: list[str], n: int = 3) -> list[str]:
    return difflib.get_close_matches(context, alle_contexts, n=n, cutoff=0.0)


def selectie_ids(sel_path: Path, context_index: dict[str, list[dict]]) -> list[str]:
    """Regels van een selectiebestand. Speciaal geval (§4.7): een bron/besluiten/-bestand
    met als eerste regel 'paginabereik START END' claimt alle context:text-zinnen in dat
    paginabereik in plaats van losse zin-ids."""
    regels = sel_path.read_text(encoding="utf-8").splitlines()
    if regels and regels[0].strip().startswith("paginabereik"):
        delen = regels[0].split()
        start, eind = int(delen[1]), int(delen[2])
        ids = []
        for row in context_index.get("text", []):
            zin_id = row.get("id") or ""
            if zin_id.startswith("p"):
                num = zin_id[1:].split("-")[0]
                if num.isdigit() and start <= int(num) <= eind:
                    ids.append(zin_id)
        return ids
    return [r.strip() for r in regels if r.strip()]


LES36_UITSLUITING = REPO_ROOT / "bron" / "selecties" / "les-01-begroetingen.txt"


def resolve_zinnen(
    m: Manifest,
    context_index: dict[str, list[dict]],
    id_index: dict[str, dict],
    alle_contexts: list[str],
    fouten: Fouten,
    zinnen_veld: str = "zinnen",
) -> list[dict]:
    resolved: list[dict] = []
    for item in m.raw.get(zinnen_veld, []) or []:
        if not isinstance(item, dict) or len(item) != 1:
            fouten.add(f"{m.path.name}: ongeldig {zinnen_veld}-item {item!r} (verwacht context/selectie/ids)")
            continue
        (soort, waarde), = item.items()
        if soort == "context":
            rows = context_index.get(waarde)
            if rows is None:
                sugg = dichtstbijzijnde(waarde, alle_contexts)
                fouten.add(
                    f"{m.path.name}: contextstring '{waarde}' niet gevonden in zinnen.csv "
                    f"— suggesties: {sugg}"
                )
                continue
            resolved.extend(rows)
        elif soort == "selectie":
            sel_path = REPO_ROOT / waarde
            if not sel_path.exists():
                fouten.add(f"{m.path.name}: selectiebestand '{waarde}' bestaat niet")
                continue
            for zin_id in selectie_ids(sel_path, context_index):
                row = id_index.get(zin_id)
                if row is None:
                    fouten.add(f"{m.path.name}: selectie '{waarde}': onbekend zin-id '{zin_id}'")
                    continue
                resolved.append(row)
        elif soort == "ids":
            for zin_id in waarde:
                row = id_index.get(zin_id)
                if row is None:
                    fouten.add(f"{m.path.name}: onbekend zin-id '{zin_id}' in ids-lijst")
                    continue
                resolved.append(row)
        else:
            fouten.add(f"{m.path.name}: onbekend zinnen-itemtype '{soort}'")
    return resolved


def pas_les36_uitsluiting_toe(m: Manifest, resolved: list[dict], context_index: dict[str, list[dict]]) -> list[dict]:
    """§4.7: les 36 (dialogen) claimt 'dialogues' minus de ids uit de les-01-selectie."""
    if m.slug != "dialogen":
        return resolved
    if not LES36_UITSLUITING.exists():
        return resolved
    uitgesloten = {r.strip() for r in LES36_UITSLUITING.read_text(encoding="utf-8").splitlines() if r.strip()}
    return [r for r in resolved if r.get("id") not in uitgesloten]


def check_tarifit_in_proza(m: Manifest, toegestane_tokens: set[str], fouten: Fouten) -> None:
    """§4.4: elke regel van de lesbody die buiten {{...}}-placeholders, buiten
    ::: verdieping-koppen en buiten `backticks` een TAR_CHARS-teken bevat, faalt. In
    backticks is Tarifit alleen toegestaan als het token in toegestane_tokens zit
    (woordenlijst-varianten ∪ tokens van geclaimde zinnen ∪ morfemen.csv)."""
    for regelnr, regel in enumerate(m.body.split("\n"), start=m.body_start_line):
        gestript = regel.strip()
        if gestript in PLACEHOLDER_TOKENS or VERDIEPING_KOP_RE.match(gestript) or gestript == ":::":
            continue
        for bt in BACKTICK_RE.finditer(regel):
            for token in bt.group(1).split():
                token_schoon = token.strip(_TOKEN_RANDTEKENS)
                # Ook het ongestripte token proberen: prefixen als `ss-` staan mét
                # koppelteken in morfemen.csv en mogen niet kapotgestript worden.
                if (
                    token_schoon
                    and token_schoon.lower() not in toegestane_tokens
                    and token.lower() not in toegestane_tokens
                ):
                    fouten.add(
                        f"{m.path.name} regel {regelnr}: vrij Tarifit in proza "
                        f"(backtick-token '{token_schoon}' niet in woordenlijst/zinnen/morfemen)"
                    )
        buiten_backticks = BACKTICK_RE.sub("", regel)
        if any(ch in TAR_CHARS for ch in buiten_backticks):
            fouten.add(f"{m.path.name} regel {regelnr}: vrij Tarifit in proza")


def check_kernwoorden(m: Manifest, lemma_set: set[str], fouten: Fouten) -> None:
    if m.kernwoorden == "auto":
        return
    if not isinstance(m.kernwoorden, list):
        fouten.add(f"{m.path.name}: kernwoorden moet 'auto' of een lijst zijn, kreeg {m.kernwoorden!r}")
        return
    for lemma in m.kernwoorden:
        if lemma.strip().lower() not in lemma_set:
            fouten.add(f"{m.path.name}: kernwoord '{lemma}' niet gevonden in woordenlijst")


def main() -> int:
    fouten = Fouten()

    manifests: list[Manifest] = []
    for pad in sorted(LESSEN_DIR.glob("*.md")) if LESSEN_DIR.exists() else []:
        try:
            manifests.append(load_manifest(pad))
        except ManifestError as e:
            fouten.add(str(e))
    kaarten: list[Manifest] = []
    for pad in sorted(KAARTEN_DIR.glob("*.md")) if KAARTEN_DIR.exists() else []:
        try:
            kaarten.append(load_manifest(pad))
        except ManifestError as e:
            fouten.add(str(e))

    context_index, id_index = laad_zinnen()
    alle_contexts = sorted(context_index.keys())
    ankers = laad_ankers()
    woordenlijst_rows, wl_fouten = laad_woordenlijst()
    fouten.items.extend(wl_fouten.items)
    lemma_set = woordenlijst_lemma_set(woordenlijst_rows)
    morfemen_vormen = {r["vorm"].strip().lower() for r in laad_morfemen()}

    gezien_ids: dict[str, Path] = {}
    totaal_zinnen = 0
    for m in manifests + kaarten:
        check_manifest_basis(m, fouten, gezien_ids)
        check_grammatica(m, ankers, fouten)
        resolved = resolve_zinnen(m, context_index, id_index, alle_contexts, fouten)
        resolved = pas_les36_uitsluiting_toe(m, resolved, context_index)
        verdieping_resolved: list[dict] = []
        if m.raw.get("verdieping_zinnen"):
            verdieping_resolved = resolve_zinnen(
                m, context_index, id_index, alle_contexts, fouten, zinnen_veld="verdieping_zinnen"
            )
        if m.type != "kaart" and m.status != "dun" and len(resolved) < 3:
            fouten.add(f"{m.path.name}: slechts {len(resolved)} zin(nen), minimaal 3 vereist (tenzij status: dun)")
        check_kernwoorden(m, lemma_set, fouten)

        geclaimde_tokens = set()
        for row in resolved + verdieping_resolved:
            geclaimde_tokens |= {t.lower() for t in tarifit_tokens(row.get("tarifit", ""))}
        toegestane_tokens = lemma_set | morfemen_vormen | geclaimde_tokens
        check_tarifit_in_proza(m, toegestane_tokens, fouten)

        totaal_zinnen += len(resolved)

    if fouten:
        print(f"FOUT — {len(fouten)} fout(en):", file=sys.stderr)
        for msg in fouten.items:
            print(f"  - {msg}", file=sys.stderr)
        return 1

    n_les = len(manifests)
    les_woord = "les" if n_les == 1 else "lessen"
    print(f"OK — {n_les} {les_woord}, {totaal_zinnen} zinnen, 0 fouten")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
