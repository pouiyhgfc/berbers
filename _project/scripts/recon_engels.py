"""
Fase 1, Stap 1.3 — Engelse import-CSV sanity-check
Vergelijkt woordenlijst-engels-import.csv met de canonieke woordenlijst.csv.
Rapporteert Tarifit-sleutels die alleen in de import-CSV staan (niet in de canonieke CSV).
Na deze check mag de import-CSV naar archief.
Wijzigt GEEN bronbestanden.
"""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANON_CSV = ROOT / "assets/woordenlijst/woordenlijst.csv"
IMPORT_CSV = ROOT / "assets/woordenlijst/woordenlijst-engels-import.csv"
OUT_PATH = ROOT / "_project/generated/recon-engels.md"


def normalize(s: str) -> str:
    return s.strip().lower()


def load_csv(path: Path, tarifit_col: int = 0) -> dict[str, dict]:
    """Laad CSV; retourneert dict van normalized-tarifit → rij-dict."""
    rows = {}
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            key = normalize(row[tarifit_col])
            if key:
                rows[key] = row
    return rows


def main():
    canon = load_csv(CANON_CSV, tarifit_col=0)
    import_csv = load_csv(IMPORT_CSV, tarifit_col=0)

    alleen_in_import = {k: v for k, v in import_csv.items() if k not in canon}
    alleen_in_canon = {k: v for k, v in canon.items() if k not in import_csv}

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("# Recon-rapport: `woordenlijst-engels-import.csv` ↔ canonieke CSV\n\n")
        f.write(
            "> **Sanity-check.** De canonieke `woordenlijst.csv` is de bron van waarheid.\n"
            "> Na deze check mag `woordenlijst-engels-import.csv` naar archief (fase 2).\n\n"
        )
        f.write(f"Canonieke CSV  : `{CANON_CSV.relative_to(ROOT)}`  ({len(canon)} sleutels)\n")
        f.write(f"Import CSV     : `{IMPORT_CSV.relative_to(ROOT)}`  ({len(import_csv)} sleutels)\n\n")

        f.write(f"| Categorie | Aantal |\n")
        f.write(f"|-----------|--------|\n")
        f.write(f"| Alleen in import-CSV (niet in canoniek) | {len(alleen_in_import)} |\n")
        f.write(f"| Alleen in canonieke CSV (niet in import) | {len(alleen_in_canon)} |\n")
        f.write(f"| In beide aanwezig | {len(canon) & len(import_csv)} |\n\n")

        # Correcte overlap-telling
        overlap = len(set(canon) & set(import_csv))
        f.write(f"_Correcte overlap: {overlap} sleutels in beide bestanden._\n\n")

        if alleen_in_import:
            f.write(f"## Sleutels alleen in import-CSV ({len(alleen_in_import)})\n\n")
            f.write(
                "> Dit zijn Tarifit-vormen die in de import-CSV staan maar ontbreken in de canonieke CSV.\n"
                "> Controleer of ze bewaard moeten worden vóór archivering van de import-CSV.\n\n"
            )
            f.write("| Tarifit (import) | Engels | Niveau | Soort |\n")
            f.write("|------------------|--------|--------|-------|\n")
            for key, row in sorted(alleen_in_import.items()):
                tarifit = row[0] if len(row) > 0 else ""
                engels = row[1] if len(row) > 1 else ""
                niveau = row[2] if len(row) > 2 else ""
                soort = row[3] if len(row) > 3 else ""
                f.write(f"| {tarifit} | {engels} | {niveau} | {soort} |\n")
            f.write("\n")
        else:
            f.write("## Sleutels alleen in import-CSV\n\n")
            f.write("_Geen — alle import-CSV-sleutels zijn ook aanwezig in de canonieke CSV._\n\n")

        if alleen_in_canon:
            f.write(f"## Sleutels alleen in canonieke CSV ({len(alleen_in_canon)}) — ter info\n\n")
            f.write(
                "> Dit zijn Tarifit-vormen die wél in de canonieke CSV zitten maar niet in de import-CSV.\n"
                "> Dit is informatief; de canonieke CSV is compleet en de bron van waarheid.\n\n"
            )
            f.write("| Tarifit | Nederlands | Engels | Niveau | Soort |\n")
            f.write("|---------|------------|--------|--------|-------|\n")
            for key, row in sorted(alleen_in_canon.items()):
                tarifit = row[0] if len(row) > 0 else ""
                nl = row[1] if len(row) > 1 else ""
                en = row[2] if len(row) > 2 else ""
                niveau = row[3] if len(row) > 3 else ""
                soort = row[4] if len(row) > 4 else ""
                f.write(f"| {tarifit} | {nl} | {en} | {niveau} | {soort} |\n")
            f.write("\n")

    print(f"Rapport geschreven: {OUT_PATH}")
    print(f"  Canoniek      : {len(canon)} sleutels")
    print(f"  Import        : {len(import_csv)} sleutels")
    print(f"  Overlap       : {overlap}")
    print(f"  Alleen import : {len(alleen_in_import)}")
    print(f"  Alleen canon  : {len(alleen_in_canon)}")


if __name__ == "__main__":
    main()
