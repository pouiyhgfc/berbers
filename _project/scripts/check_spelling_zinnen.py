"""
Detector (leest alleen, schrijft nooit naar zinnen.csv): vindt vermoedelijke spellingafwijkingen
tussen `assets/zinnen/zinnen.csv` (OCR uit het boek) en `assets/woordenlijst/woordenlijst.csv`
(learntarifit-schrijfwijze).

Kernprincipe (plan §Fase S): detecteren is machinaal, beslissen is menselijk, toepassen is
mechanisch. Dit script classificeert elk Tarifit-token uit de zinnen als OK / KANDIDAAT / ONBEKEND
en schrijft rapporten. Het wijzigt nooit de brondata — beslissen gebeurt door Idries (stap S.2) in
`_project/rapporten/spelling-kandidaten.csv`, toepassen door `apply_spelling_zinnen.py` (stap S.3).

De platslag-functie normalize_tarifit() is een LETTERLIJKE, één-op-één Python-port van de
`normalize()`-functie in `nl/woordenlijst.html` (rond regel 403), zodat dezelfde twee spellingen
altijd naar dezelfde vorm platslaan als in de zoekfunctie op de site zelf:

    function normalize(s) {
      return s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '')
        .replace(/ḏ/g, 'd').replace(/ḍ/g, 'd').replace(/ṯ/g, 't').replace(/ṭ/g, 't')
        .replace(/ḥ/g, 'h').replace(/ɣ/g, 'g').replace(/ɛ/g, 'a').replace(/ř/g, 'r')
        .replace(/ṛ/g, 'r').replace(/ẓ/g, 'z').replace(/ǧ/g, 'j').replace(/ṣ/g, 's')
        .replace(/ǧ/g, 'g').replace(/ḇ/g, 'b').replace(/ḵ/g, 'k').replace(/ḷ/g, 'l');
    }

(Verificatie: op één na alle letters in deze lijst — ḏ ḍ ṯ ṭ ḥ ř ṛ ẓ ǧ ṣ ḇ ḵ ḷ — decomponeren
onder NFD al naar hun grondletter + een combining mark in U+0300–U+036F, en zijn dus al weg
vóórdat de expliciete `.replace()`-regels ze zouden kunnen raken; die regels zijn effectief dode
code/dubbele beveiliging. Alleen `ɛ`→`a` en `ɣ`→`g` doen echt werk: die twee letters hebben geen
NFD-decompositie. Dit is bevestigd gedrag van het origineel (JS normaliseert ook eerst NFD), dus
de Python-port reproduceert het letterlijk — geen fix, alleen overgenomen.)

Classificatie per token:
  - OK        — exacte match met een vorm (of `/`-variant) in woordenlijst.csv.
  - KANDIDAAT — geen exacte match, maar de platgeslagen vorm matcht precies ÉÉN
                woordenlijstwoord met een andere spelling.
  - AMBIGU    — de platgeslagen vorm matcht MEERDERE woordenlijstwoorden — nooit een
                enkelvoudig voorstel, apart gerapporteerd.
  - ONBEKEND  — geen match, ook niet platgeslagen. Geen fout: meestal een vervoegde/verbogen
                vorm of een woord dat nog niet in de lijst staat (oogst voor S.4).
Tokens korter dan 3 tekens worden nooit als KANDIDAAT/AMBIGU voorgesteld (te veel
toevalstreffers) en landen in een aparte, informatieve lijst.

Output:
  _project/rapporten/spelling-kandidaten.csv   (S.1/S.2 — Idries vult kolom `status`)
  _project/rapporten/spelling-ambigu.csv       (informatief, geen voorstel-kolom)
  _project/rapporten/onbekende-tokens.csv      (S.4 — werklijst voor woordenlijst-uitbreiding)
  _project/rapporten/spelling-korte-tokens.csv (informatief, < 3 tekens)

Draaien:  python _project/scripts/check_spelling_zinnen.py
"""

import csv
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WOORDENLIJST_CSV = ROOT / "assets/woordenlijst/woordenlijst.csv"
ZINNEN_CSV = ROOT / "assets/zinnen/zinnen.csv"
RAPPORTEN = ROOT / "_project/rapporten"

MIN_KANDIDAAT_LEN = 3
_ID_TAG_RE = re.compile(r"id:([^;]+)")
_COMBINING_RE = re.compile("[\\u0300-\\u036f]")
_EDGE_PUNCT = '"“”„‘’,.;:?!…·→>*()[]{}«»—–- '


def normalize_tarifit(s: str) -> str:
    """Eén-op-één port van normalize() in nl/woordenlijst.html — zie moduledocstring."""
    s = s.lower()
    s = unicodedata.normalize("NFD", s)
    s = _COMBINING_RE.sub("", s)
    for a, b in (
        ("ḏ", "d"), ("ḍ", "d"), ("ṯ", "t"), ("ṭ", "t"),
        ("ḥ", "h"), ("ɣ", "g"), ("ɛ", "a"), ("ř", "r"),
        ("ṛ", "r"), ("ẓ", "z"), ("ǧ", "j"), ("ṣ", "s"),
        ("ǧ", "g"), ("ḇ", "b"), ("ḵ", "k"), ("ḷ", "l"),
    ):
        s = s.replace(a, b)
    return s


def load_woordenlijst() -> tuple[set[str], dict[str, list[dict]]]:
    """(exacte spellingen, platgeslagen vorm -> lijst van {spelling, nl, en})."""
    if not WOORDENLIJST_CSV.exists():
        sys.exit(f"FOUT: {WOORDENLIJST_CSV.relative_to(ROOT)} ontbreekt.")
    exact: set[str] = set()
    flat_map: dict[str, list[dict]] = {}
    seen_per_flat: dict[str, set[str]] = {}
    with open(WOORDENLIJST_CSV, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw = (row.get("tarifit") or "").strip()
            if not raw:
                continue
            for variant in raw.split("/"):
                variant = variant.strip()
                if not variant:
                    continue
                exact.add(variant)
                flat = normalize_tarifit(variant)
                if not flat:
                    continue
                seen = seen_per_flat.setdefault(flat, set())
                if variant in seen:
                    continue
                seen.add(variant)
                flat_map.setdefault(flat, []).append(
                    {"spelling": variant, "nl": (row.get("nl") or "").strip(),
                     "en": (row.get("en") or "").strip()}
                )
    return exact, flat_map


def tokenize(tarifit: str) -> list[str]:
    """Splits op witruimte én op clitic-koppeltekens, strip randleestekens."""
    tokens: list[str] = []
    for piece in tarifit.split():
        for sub in piece.split("-"):
            tok = sub.strip(_EDGE_PUNCT)
            if tok and any(ch.isalpha() for ch in tok):
                tokens.append(tok)
    return tokens


def load_zinnen() -> list[dict]:
    if not ZINNEN_CSV.exists():
        sys.exit(f"FOUT: {ZINNEN_CSV.relative_to(ROOT)} ontbreekt.")
    rows = []
    with open(ZINNEN_CSV, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tarifit = (row.get("tarifit") or "").strip()
            if not tarifit or tarifit == "tarifit":
                continue
            m = _ID_TAG_RE.search(row.get("tags") or "")
            row["_id"] = m.group(1).strip() if m else "?"
            rows.append(row)
    return rows


def betekenis(entry: dict) -> str:
    parts = [p for p in (entry["nl"], entry["en"]) if p]
    return " / ".join(parts)


def write_csv(path: Path, header: list[str], rows: list[list]) -> None:
    RAPPORTEN.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def main() -> None:
    exact, flat_map = load_woordenlijst()
    zinnen = load_zinnen()

    n_ok = 0
    kandidaten: dict[tuple[str, str], dict] = {}
    ambigu: dict[str, dict] = {}
    onbekend: Counter = Counter()
    onbekend_ids: dict[str, list[str]] = {}
    korte: Counter = Counter()

    for row in zinnen:
        tarifit, en, zid = row["tarifit"], (row.get("en") or "").strip(), row["_id"]
        for tok in tokenize(tarifit):
            if tok in exact:
                n_ok += 1
                continue
            if len(tok) < MIN_KANDIDAAT_LEN:
                korte[tok] += 1
                continue
            flat = normalize_tarifit(tok)
            matches = flat_map.get(flat)
            if not matches:
                onbekend[tok] += 1
                ids = onbekend_ids.setdefault(tok, [])
                if len(ids) < 3:
                    ids.append(zid)
                continue
            if len(matches) == 1:
                voorstel = matches[0]
                key = (tok, voorstel["spelling"])
                slot = kandidaten.setdefault(key, {
                    "betekenis": betekenis(voorstel), "aantal": 0, "ids": [], "en": en,
                })
                slot["aantal"] += 1
                if len(slot["ids"]) < 3:
                    slot["ids"].append(zid)
            else:
                slot = ambigu.setdefault(tok, {"matches": matches, "aantal": 0, "ids": [], "en": en})
                slot["aantal"] += 1
                if len(slot["ids"]) < 3:
                    slot["ids"].append(zid)

    kand_rows = sorted(
        (
            [tok, voorstel, v["betekenis"], v["aantal"], "; ".join(v["ids"]), v["en"], ""]
            for (tok, voorstel), v in kandidaten.items()
        ),
        key=lambda r: -r[3],
    )
    write_csv(
        RAPPORTEN / "spelling-kandidaten.csv",
        ["token", "voorstel", "betekenis_woordenlijst", "aantal", "voorbeeld_ids", "voorbeeld_en", "status"],
        kand_rows,
    )

    ambigu_rows = sorted(
        (
            [tok, "; ".join(f"{m['spelling']} ({betekenis(m)})" for m in v["matches"]),
             v["aantal"], "; ".join(v["ids"]), v["en"]]
            for tok, v in ambigu.items()
        ),
        key=lambda r: -r[2],
    )
    write_csv(
        RAPPORTEN / "spelling-ambigu.csv",
        ["token", "kandidaten", "aantal", "voorbeeld_ids", "voorbeeld_en"],
        ambigu_rows,
    )

    onbekend_rows = sorted(
        ([tok, n, "; ".join(onbekend_ids[tok])] for tok, n in onbekend.items()),
        key=lambda r: -r[1],
    )
    write_csv(RAPPORTEN / "onbekende-tokens.csv", ["token", "aantal", "voorbeeld_ids"], onbekend_rows)

    korte_rows = sorted(([tok, n] for tok, n in korte.items()), key=lambda r: -r[1])
    write_csv(RAPPORTEN / "spelling-korte-tokens.csv", ["token", "aantal"], korte_rows)

    print(f"Zinnen verwerkt: {len(zinnen)}")
    print(f"Tokens OK (exacte match): {n_ok}")
    print(f"Kandidaten (uniek token->voorstel paar): {len(kand_rows)}  "
          f"(totaal {sum(r[3] for r in kand_rows)} tokenvoorkomens)")
    print(f"Ambigu (uniek token): {len(ambigu_rows)}  "
          f"(totaal {sum(r[2] for r in ambigu_rows)} tokenvoorkomens)")
    print(f"Onbekend (uniek token): {len(onbekend_rows)}  "
          f"(totaal {sum(r[1] for r in onbekend_rows)} tokenvoorkomens)")
    print(f"Korte tokens (<{MIN_KANDIDAAT_LEN} tekens, uniek): {len(korte_rows)}  "
          f"(totaal {sum(r[1] for r in korte_rows)} tokenvoorkomens)")
    print(f"Geschreven: {RAPPORTEN.relative_to(ROOT)}/spelling-kandidaten.csv, "
          f"spelling-ambigu.csv, onbekende-tokens.csv, spelling-korte-tokens.csv")


if __name__ == "__main__":
    main()
