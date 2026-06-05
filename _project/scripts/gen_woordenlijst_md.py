"""
Fase 3, Stap 3.1 — Generator: _ai/woordenlijst.md  <-  assets/woordenlijst/woordenlijst.csv

Verliesloze herformatteerder: leest de canonieke CSV naam-gebaseerd, groepeert op CEFR-niveau
en emit per niveau een tabel | Tarifit | Nederlands | Engels | Soort | met een *berekend* totaal.
Elke Tarifit-vorm komt LETTERLIJK uit kolom `tarifit`. De generator synthetiseert nooit Tarifit.

Banner bovenaan (stap 3.4). Draaien:  python _project/scripts/gen_woordenlijst_md.py
"""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "assets/woordenlijst/woordenlijst.csv"
OUT_PATH = ROOT / "_ai/woordenlijst.md"

# Geldige CEFR-niveaus, in weergavevolgorde. Rijen met een ander niveau (bv. de stray
# header-rij `niveau` die uit een oude import in de CSV is blijven hangen) worden overgeslagen.
NIVEAU_ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"]

BANNER = (
    "<!-- AUTO-GEGENEREERD uit assets/woordenlijst/woordenlijst.csv "
    "door _project/scripts/gen_woordenlijst_md.py\n"
    "     NIET met de hand bewerken. Bewerk de bron en draai `make build`. "
    "Zie WIJZIGINGEN.md. -->"
)

LEGEND = (
    "**Afkortingen woordsoort:** ww = werkwoord · znw = zelfstandig naamwoord · "
    "vnw = voornaamwoord · voegw = voegwoord · bvnw = bijvoeglijk naamwoord · byw = bijwoord"
)


def load_rows() -> list[dict]:
    """Lees de CSV naam-gebaseerd (koprij verplicht). Sla rijen zonder geldig CEFR-niveau over."""
    rows: list[dict] = []
    skipped: list[dict] = []
    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required = {"tarifit", "nl", "en", "cefr", "woordsoort"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            sys.exit(f"FOUT: CSV mist verplichte kolom(men): {sorted(missing)}")
        for row in reader:
            niveau = (row.get("cefr") or "").strip()
            if niveau in NIVEAU_ORDER:
                rows.append(row)
            else:
                skipped.append(row)
    if skipped:
        # Geen Tarifit verloren — dit zijn rijen die geen geldig niveau dragen (bv. een
        # achtergebleven header-rij). We melden ze zodat ze zichtbaar blijven.
        print(f"  Overgeslagen rijen zonder geldig CEFR-niveau: {len(skipped)}")
        for r in skipped:
            print(f"    - tarifit={r.get('tarifit')!r} cefr={r.get('cefr')!r}")
    return rows


def cell(value: str) -> str:
    """Maak een waarde veilig voor een markdown-tabelcel (escape pipe, normaliseer whitespace)."""
    return " ".join((value or "").split()).replace("|", "\\|")


def build_markdown(rows: list[dict]) -> str:
    out: list[str] = [BANNER, ""]
    out.append("# Tarifit Woordenlijst")
    out.append("> **REGEL:** Gebruik ALLEEN woorden die letterlijk in deze lijst staan.")
    out.append(f"> Totaal: {len(rows)} woorden.")
    out.append("")
    out.append(LEGEND)
    out.append("")

    by_niveau: dict[str, list[dict]] = {n: [] for n in NIVEAU_ORDER}
    for row in rows:
        by_niveau[row["cefr"].strip()].append(row)

    for niveau in NIVEAU_ORDER:
        entries = by_niveau[niveau]
        if not entries:
            continue
        out.append(f"## Niveau {niveau}")
        out.append("")
        out.append("| Tarifit | Nederlands | Engels | Soort |")
        out.append("|---------|------------|--------|-------|")
        for e in entries:
            # Kolom 0 (tarifit) wordt LETTERLIJK overgenomen — alleen tabel-escaping.
            out.append(
                f"| {cell(e['tarifit'])} | {cell(e['nl'])} | "
                f"{cell(e['en'])} | {cell(e['woordsoort'])} |"
            )
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def main() -> None:
    rows = load_rows()
    md = build_markdown(rows)
    OUT_PATH.write_text(md, encoding="utf-8")
    print(f"Geschreven: {OUT_PATH.relative_to(ROOT)}  ({len(rows)} woorden)")


if __name__ == "__main__":
    main()
