"""
Gedeelde laad-functies voor de cursusgenerator (bouw_cursus.py). Leest zinnen.csv en
woordenlijst.csv en levert kleine, herbruikbare opzoekstructuren. Bewust los van
check_bronnen.py (dat blijft ongewijzigd — een werkende validator wordt niet aangeraakt
voor een refactor die niets aan gedrag toevoegt).
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ZINNEN_CSV = REPO_ROOT / "assets" / "zinnen" / "zinnen.csv"
WOORDENLIJST_CSV = REPO_ROOT / "assets" / "woordenlijst" / "woordenlijst.csv"
MORFEMEN_CSV = REPO_ROOT / "bron" / "morfemen.csv"

CEFR_RANG = {"A1": 0, "A2": 1, "B1": 2, "B2": 3}


def parse_tags(tags: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in tags.split(";"):
        part = part.strip()
        if not part or ":" not in part:
            continue
        k, _, v = part.partition(":")
        out[k.strip()] = v.strip()
    return out


def zin_sorteersleutel(row: dict) -> tuple[int, int]:
    zin_id = row.get("id") or ""
    m = zin_id[1:].split("-") if zin_id.startswith("p") else None
    if not m or len(m) != 2:
        return (0, 0)
    try:
        return (int(m[0]), int(m[1]))
    except ValueError:
        return (0, 0)


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
    for rows in context_index.values():
        rows.sort(key=zin_sorteersleutel)
    return context_index, id_index


def laad_woordenlijst() -> list[dict]:
    if not WOORDENLIJST_CSV.exists():
        sys.exit(f"FOUT: {WOORDENLIJST_CSV} ontbreekt")
    with WOORDENLIJST_CSV.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def woordenlijst_lemma_index(rows: list[dict]) -> dict[str, dict]:
    """lemma (lowercase variant) -> woordenlijst-rij. Bij meerdere rijen met dezelfde
    variant wint de eerste (rijvolgorde van het bestand)."""
    index: dict[str, dict] = {}
    for r in rows:
        for variant in r["tarifit"].split(" / "):
            key = variant.strip().lower()
            index.setdefault(key, r)
    return index


def laad_morfemen() -> list[dict]:
    if not MORFEMEN_CSV.exists():
        return []
    with MORFEMEN_CSV.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def resolve_zinnen_grouped(
    m, context_index: dict[str, list[dict]], id_index: dict[str, dict], zinnen_veld: str = "zinnen"
) -> list[tuple[str, str, list[dict]]]:
    """Simpele, harde-fout-variant van claim-resolutie (geen suggesties — dat is het
    werk van check_bronnen.py, dat vóór de build hoort te draaien). Geeft per
    zinnen-item (in manifest-volgorde) (soort, waarde, gesorteerde rijen)."""
    groepen: list[tuple[str, str, list[dict]]] = []
    for item in m.raw.get(zinnen_veld, []) or []:
        if not isinstance(item, dict) or len(item) != 1:
            sys.exit(f"FOUT: {m.path.name}: ongeldig {zinnen_veld}-item {item!r}")
        (soort, waarde), = item.items()
        if soort == "context":
            rows = context_index.get(waarde)
            if rows is None:
                sys.exit(f"FOUT: {m.path.name}: contextstring '{waarde}' niet gevonden (draai eerst check_bronnen.py)")
            rows = list(rows)
            if zinnen_veld == "zinnen":
                rows = pas_les36_uitsluiting_toe(m, soort, waarde, rows)
            groepen.append((soort, waarde, rows))
        elif soort == "selectie":
            sel_path = REPO_ROOT / waarde
            if not sel_path.exists():
                sys.exit(f"FOUT: {m.path.name}: selectiebestand '{waarde}' ontbreekt")
            rows = []
            for zin_id in selectie_ids(sel_path, context_index):
                row = id_index.get(zin_id)
                if row is None:
                    sys.exit(f"FOUT: {m.path.name}: onbekend zin-id '{zin_id}' in selectie '{waarde}'")
                rows.append(row)
            rows.sort(key=zin_sorteersleutel)
            groepen.append((soort, waarde, rows))
        elif soort == "ids":
            rows = []
            for zin_id in waarde:
                row = id_index.get(zin_id)
                if row is None:
                    sys.exit(f"FOUT: {m.path.name}: onbekend zin-id '{zin_id}'")
                rows.append(row)
            rows.sort(key=zin_sorteersleutel)
            groepen.append((soort, waarde, rows))
        else:
            sys.exit(f"FOUT: {m.path.name}: onbekend zinnen-itemtype '{soort}'")
    return groepen


def resolve_zinnen(m, context_index: dict[str, list[dict]], id_index: dict[str, dict]) -> list[dict]:
    resolved: list[dict] = []
    for _soort, _waarde, rows in resolve_zinnen_grouped(m, context_index, id_index):
        resolved.extend(rows)
    resolved.sort(key=zin_sorteersleutel)
    return resolved


LES36_UITSLUITING = REPO_ROOT / "bron" / "selecties" / "les-01-begroetingen.txt"


def pas_les36_uitsluiting_toe(m, soort: str, waarde: str, rows: list[dict]) -> list[dict]:
    """§4.7: les 36 (dialogen) claimt 'dialogues' minus de ids uit de les-01-selectie."""
    if m.slug != "dialogen" or soort != "context" or waarde != "dialogues":
        return rows
    if not LES36_UITSLUITING.exists():
        return rows
    uitgesloten = {r.strip() for r in LES36_UITSLUITING.read_text(encoding="utf-8").splitlines() if r.strip()}
    return [r for r in rows if r.get("id") not in uitgesloten]


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


def boekpagina(resolved: list[dict], prefix: str = "boek p.") -> str:
    paginas = set()
    for row in resolved:
        zin_id = row.get("id") or ""
        if zin_id.startswith("p"):
            num = zin_id[1:].split("-")[0]
            if num.isdigit():
                paginas.add(int(num))
    if not paginas:
        return ""
    if len(paginas) == 1:
        return f"{prefix}{next(iter(paginas))}"
    return f"{prefix}{min(paginas)}–{max(paginas)}"


# '[' en ']' zijn redactionele groeperingshaken om frasen heen (zinnen.csv markeert er
# bijzinnen mee) — geen onderdeel van de Tarifit-vorm, dus splitsen. Zelfde keuze als in
# _gen_common.py, dat ze al van de tokenrand stript.
_TAR_SPLIT_CHARS = ' \t\n.,;:!?()«»„“”[]'


def tarifit_tokens(tekst: str) -> list[str]:
    tokens: list[str] = []
    huidig = []
    for ch in tekst:
        if ch in _TAR_SPLIT_CHARS:
            if huidig:
                tokens.append("".join(huidig))
                huidig = []
        else:
            huidig.append(ch)
    if huidig:
        tokens.append("".join(huidig))
    return [t.strip("-") for t in tokens if t.strip("-")]


def kernwoorden_auto(resolved: list[dict], lemma_index: dict[str, dict]) -> list[dict]:
    gevonden: dict[int, dict] = {}
    for row in resolved:
        for token in tarifit_tokens(row.get("tarifit", "")):
            lemma_row = lemma_index.get(token.lower())
            if lemma_row is not None:
                gevonden[id(lemma_row)] = lemma_row
    return sorted(
        gevonden.values(),
        key=lambda r: (CEFR_RANG.get(r["cefr"], 99), r["tarifit"].lower()),
    )
