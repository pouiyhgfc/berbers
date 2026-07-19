"""
Fase 1, Stap 1.1 — Woorden: CSV leidend (advisory)
Vergelijkt _ai/woordenlijst.md met assets/woordenlijst/woordenlijst.csv.
Rapporteert woorden die wél in de MD staan maar NIET in de CSV (kijklijst).
Wijzigt GEEN bronbestanden.
"""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "assets/woordenlijst/woordenlijst.csv"
MD_PATH = ROOT / "_ai/woordenlijst.md"
OUT_PATH = ROOT / "_project/generated/recon-woorden.md"


def normalize(s: str) -> str:
    """Trim whitespace, lowercase — vergelijk op Tarifit-vorm zonder spelling te wijzigen."""
    return s.strip().lower()


def load_csv_tarifit() -> set[str]:
    keys = set()
    with open(CSV_PATH, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                keys.add(normalize(row[0]))
    return keys


def load_md_entries() -> list[dict]:
    """
    Leest tabel-rijen uit woordenlijst.md.
    Retourneert lijst van {tarifit, nl, en, soort, niveau}.
    """
    entries = []
    current_niveau = ""
    niveau_re = re.compile(r"^##\s+Niveau\s+(\S+)", re.IGNORECASE)
    row_re = re.compile(r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|")

    with open(MD_PATH, encoding="utf-8") as f:
        for line in f:
            m = niveau_re.match(line)
            if m:
                current_niveau = m.group(1)
                continue
            # skip header / separator
            if re.match(r"^\|[-| ]+\|", line):
                continue
            m = row_re.match(line)
            if m:
                tarifit, nl, en, soort = (g.strip() for g in m.groups())
                if tarifit.lower() in ("tarifit", ""):
                    continue
                entries.append(
                    {
                        "tarifit": tarifit,
                        "nl": nl,
                        "en": en,
                        "soort": soort,
                        "niveau": current_niveau,
                    }
                )
    return entries


def main():
    csv_keys = load_csv_tarifit()
    md_entries = load_md_entries()

    only_in_md = [e for e in md_entries if normalize(e["tarifit"]) not in csv_keys]

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("# Recon-rapport: woorden alleen in `_ai/woordenlijst.md` (niet in CSV)\n\n")
        f.write(
            "> **Kijklijst, geen gate.** Dit zijn woorden die in de MD staan maar ontbreken in de canonieke CSV.\n"
            "> Wil je een woord bewaren, voeg het dan zélf aan de CSV toe (jij levert de Tarifit-vorm).\n"
            "> Fase 3 regenereert uit de CSV.\n\n"
        )
        f.write(f"CSV-bestand : `{CSV_PATH.relative_to(ROOT)}`\n")
        f.write(f"MD-bestand  : `{MD_PATH.relative_to(ROOT)}`\n\n")
        f.write(f"**CSV-woorden:** {len(csv_keys)}  \n")
        f.write(f"**MD-woorden:** {len(md_entries)}  \n")
        f.write(f"**Alleen in MD (niet in CSV):** {len(only_in_md)}\n\n")

        if not only_in_md:
            f.write("_Geen verschillen gevonden — MD en CSV zijn gesynchroniseerd._\n")
        else:
            # Groepeer per niveau
            by_niveau: dict[str, list] = {}
            for e in only_in_md:
                by_niveau.setdefault(e["niveau"], []).append(e)

            for niveau, entries in sorted(by_niveau.items()):
                f.write(f"## Niveau {niveau} ({len(entries)} woorden)\n\n")
                f.write("| Tarifit | Nederlands | Engels | Soort |\n")
                f.write("|---------|------------|--------|-------|\n")
                for e in entries:
                    f.write(f"| {e['tarifit']} | {e['nl']} | {e['en']} | {e['soort']} |\n")
                f.write("\n")

    print(f"Rapport geschreven: {OUT_PATH}")
    print(f"  CSV-woorden : {len(csv_keys)}")
    print(f"  MD-woorden  : {len(md_entries)}")
    print(f"  Alleen in MD: {len(only_in_md)}")


if __name__ == "__main__":
    main()
