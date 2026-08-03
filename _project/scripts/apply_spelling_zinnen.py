"""
Toepasser (stap S.3): past goedgekeurde spellingvervangingen uit
`_project/rapporten/spelling-kandidaten.csv` toe op de `tarifit`-kolom van
`assets/zinnen/zinnen.csv` — en NERGENS anders.

Gebruikt uitsluitend rijen met `status=ja`. Vervangt hele tokens (op woordgrenzen, inclusief
clitic-koppeltekens als grens — dezelfde tokenisatie-opvatting als check_spelling_zinnen.py),
nooit een deel van een langer woord.

Standaard: DRY-RUN. Toont per vervanging tot 3 voor/na-voorbeelden uit de zinnen die echt
wijzigen. Schrijft pas naar zinnen.csv met de vlag --apply.

Na --apply verifieert het script zelf:
  - alle kolommen behalve `tarifit` zijn byte-identiek aan voor de vervanging;
  - het aantal gewijzigde rijen wordt gemeld;
  - elke toegepaste vervanging komt uit een status=ja-rij (per constructie: de mapping wordt
    uitsluitend uit die rijen gebouwd).

Draaien:
    python _project/scripts/apply_spelling_zinnen.py            # dry-run
    python _project/scripts/apply_spelling_zinnen.py --apply    # schrijft zinnen.csv
"""

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ZINNEN_CSV = ROOT / "assets/zinnen/zinnen.csv"
KANDIDATEN_CSV = ROOT / "_project/rapporten/spelling-kandidaten.csv"
KOLOMMEN = ["tarifit", "nl", "en", "gloss", "hoofdstuk", "les", "bron", "tags"]
MAX_VOORBEELDEN = 3


def load_mapping() -> dict[str, str]:
    if not KANDIDATEN_CSV.exists():
        sys.exit(f"FOUT: {KANDIDATEN_CSV.relative_to(ROOT)} ontbreekt — draai eerst check_spelling_zinnen.py.")
    mapping: dict[str, str] = {}
    with open(KANDIDATEN_CSV, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if (row.get("status") or "").strip().lower() != "ja":
                continue
            token = (row.get("token") or "").strip()
            voorstel = (row.get("voorstel") or "").strip()
            if not token or not voorstel:
                continue
            if token in mapping and mapping[token] != voorstel:
                sys.exit(
                    f"FOUT: token {token!r} heeft tegenstrijdige status=ja-voorstellen "
                    f"({mapping[token]!r} vs {voorstel!r}) — repareer het rapport."
                )
            mapping[token] = voorstel
    if not mapping:
        sys.exit("FOUT: geen enkele rij met status=ja gevonden — niets om toe te passen.")
    return mapping


def build_pattern(mapping: dict[str, str]) -> re.Pattern:
    # Langste tokens eerst zodat een kortere niet per ongeluk een langere overlapt.
    tokens_sorted = sorted(mapping, key=len, reverse=True)
    alternation = "|".join(re.escape(t) for t in tokens_sorted)
    return re.compile(r"(?<!\w)(" + alternation + r")(?!\w)")


def replace_tarifit(tarifit: str, mapping: dict[str, str], pattern: re.Pattern) -> str:
    return pattern.sub(lambda m: mapping[m.group(0)], tarifit)


def main() -> None:
    apply = "--apply" in sys.argv
    mapping = load_mapping()
    pattern = build_pattern(mapping)

    with open(ZINNEN_CSV, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    voorbeelden: dict[str, list[tuple[str, str, str]]] = {}  # token -> [(id, voor, na), ...]
    n_gewijzigde_rijen = 0
    changed_rows: list[tuple[int, str, str]] = []  # (row_index, before, after)

    for i, row in enumerate(rows):
        before = row["tarifit"]
        after = replace_tarifit(before, mapping, pattern)
        if after == before:
            continue
        n_gewijzigde_rijen += 1
        changed_rows.append((i, before, after))
        zid = ""
        m = re.search(r"id:([^;]+)", row.get("tags") or "")
        if m:
            zid = m.group(1).strip()
        for tok in mapping:
            if re.search(r"(?<!\w)" + re.escape(tok) + r"(?!\w)", before):
                lst = voorbeelden.setdefault(tok, [])
                if len(lst) < MAX_VOORBEELDEN:
                    lst.append((zid, before, after))

    print(f"Mapping geladen: {len(mapping)} goedgekeurde token->voorstel vervangingen.")
    print(f"Zinnen die wijzigen: {n_gewijzigde_rijen} van {len(rows)}.")
    print()
    shown = 0
    for tok, voorstel in sorted(mapping.items()):
        examples = voorbeelden.get(tok)
        if not examples:
            continue
        shown += 1
        print(f"  {tok!r} -> {voorstel!r}:")
        for zid, before, after in examples:
            print(f"    [{zid}] {before!r} -> {after!r}")
    print(f"\n({shown} van {len(mapping)} vervangingen kwamen daadwerkelijk voor in zinnen.csv)")

    if not apply:
        print("\nDRY-RUN — er is niets geschreven. Draai met --apply om te schrijven.")
        return

    new_rows = list(rows)
    for i, _before, after in changed_rows:
        new_rows[i] = dict(new_rows[i])
        new_rows[i]["tarifit"] = after

    # Harde garantie: alle kolommen behalve tarifit blijven byte-identiek.
    for old, new in zip(rows, new_rows):
        for col in KOLOMMEN:
            if col == "tarifit":
                continue
            if (old.get(col) or "") != (new.get(col) or ""):
                sys.exit(f"FOUT: kolom {col!r} veranderde onverwacht — apply afgebroken, niets geschreven.")

    with open(ZINNEN_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(new_rows)

    print(f"\nToegepast: {n_gewijzigde_rijen} rijen bijgewerkt in {ZINNEN_CSV.relative_to(ROOT)}.")
    print("Draai nu: python _project/scripts/gen_zinnen_md.py && python _project/scripts/gen_index_md.py")


if __name__ == "__main__":
    main()
