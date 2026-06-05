"""
Fase 1, Stap 1.2 — Oefeningen: assets/cursus/ ↔ assets/oefeningen/
De engine laadt assets/oefeningen/ (actief). assets/cursus/ is de ongebruikte kopie.
Rapporteert per taal/les welke items alleen in de ongebruikte cursus-kopie staan.
Wijzigt GEEN bronbestanden.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CURSUS_DIR = ROOT / "assets/cursus"
OEFENINGEN_DIR = ROOT / "assets/oefeningen"
OUT_PATH = ROOT / "_project/generated/recon-oefeningen.md"

TALEN = ["nl", "en"]


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def item_key(item: dict) -> str:
    """Maak een vergelijkbare sleutel voor een oefening-item via type + vraag."""
    vraag = item.get("q", item.get("question", item.get("vraag", ""))).strip()
    itype = item.get("type", "").strip()
    return f"{itype}||{vraag}"


def compare_taal(taal: str) -> dict:
    """
    Vergelijkt exercises-{taal}.json uit cursus vs oefeningen.
    Structuur: dict van les-sleutel → lijst van items.
    Retourneert dict met statistieken en unieke items per les.
    """
    cursus_path = CURSUS_DIR / f"exercises-{taal}.json"
    oefeningen_path = OEFENINGEN_DIR / f"exercises-{taal}.json"

    if not cursus_path.exists():
        return {"fout": f"{cursus_path} niet gevonden"}
    if not oefeningen_path.exists():
        return {"fout": f"{oefeningen_path} niet gevonden"}

    cursus_data = load_json(cursus_path)
    oefeningen_data = load_json(oefeningen_path)

    # Zorg dat we dicts van les → [items] hebben
    def to_les_dict(data) -> dict[str, list]:
        if isinstance(data, dict):
            return data
        return {}

    cursus_lessen = to_les_dict(cursus_data)
    oefeningen_lessen = to_les_dict(oefeningen_data)

    # Bouw index: les_key → set van item_keys
    def index_lessen(lessen: dict) -> dict[str, set[str]]:
        return {lk: {item_key(item) for item in items} for lk, items in lessen.items()}

    cursus_idx = index_lessen(cursus_lessen)
    oefeningen_idx = index_lessen(oefeningen_lessen)

    cursus_total = sum(len(v) for v in cursus_idx.values())
    oefeningen_total = sum(len(v) for v in oefeningen_idx.values())

    # Per les: items alleen in cursus (ongebruikt)
    alleen_in_cursus: dict[str, list] = {}
    for lk in sorted(set(cursus_idx) | set(oefeningen_idx)):
        cursus_items = cursus_idx.get(lk, set())
        oefen_items = oefeningen_idx.get(lk, set())
        uniek = cursus_items - oefen_items
        if uniek:
            alleen_in_cursus[lk] = sorted(uniek)

    return {
        "cursus_lessen": len(cursus_idx),
        "oefeningen_lessen": len(oefeningen_idx),
        "cursus_items": cursus_total,
        "oefeningen_items": oefeningen_total,
        "alleen_in_cursus": alleen_in_cursus,
    }


def main():
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("# Recon-rapport: oefeningen `assets/cursus/` ↔ `assets/oefeningen/`\n\n")
        f.write(
            "> **Actieve engine laadt `assets/oefeningen/`.** De `assets/cursus/`-kopie is ongebruikt.\n"
            "> Hieronder staat per taal/les wat úniek is in de ongebruikte cursus-kopie.\n"
            "> **Jij beslist:** niets unieks → fase 2 naar archief; wel iets unieks → eerst toevoegen aan oefeningen.\n\n"
        )

        for taal in TALEN:
            f.write(f"## Taal: {taal.upper()}\n\n")
            result = compare_taal(taal)

            if "fout" in result:
                f.write(f"_Fout: {result['fout']}_\n\n")
                continue

            f.write(f"| | cursus/ | oefeningen/ |\n")
            f.write(f"|---|---|---|\n")
            f.write(f"| Lessen | {result['cursus_lessen']} | {result['oefeningen_lessen']} |\n")
            f.write(f"| Items totaal | {result['cursus_items']} | {result['oefeningen_items']} |\n\n")

            alleen = result["alleen_in_cursus"]
            if not alleen:
                f.write(
                    "_Geen unieke items in de cursus-kopie — alle cursus-items zitten ook in oefeningen._\n"
                    "_Aanbeveling: cursus-kopie kan veilig naar archief._\n\n"
                )
            else:
                totaal_uniek = sum(len(v) for v in alleen.values())
                f.write(
                    f"**{totaal_uniek} unieke items** in de cursus-kopie (niet in oefeningen), "
                    f"verspreid over {len(alleen)} les(sen):\n\n"
                )
                for lk, items in sorted(alleen.items(), key=lambda x: x[0].zfill(4)):
                    f.write(f"### Les {lk} ({len(items)} uniek)\n\n")
                    for item in items:
                        # Toon type en eerste deel van vraag leesbaar
                        parts = item.split("||", 1)
                        itype = parts[0] if parts else "?"
                        vraag = parts[1][:120] if len(parts) > 1 else ""
                        f.write(f"- `[{itype}]` {vraag}\n")
                    f.write("\n")

    print(f"Rapport geschreven: {OUT_PATH}")
    for taal in TALEN:
        r = compare_taal(taal)
        if "fout" not in r:
            print(
                f"  {taal.upper()}: cursus={r['cursus_items']} items, "
                f"oefeningen={r['oefeningen_items']} items, "
                f"uniek-in-cursus={sum(len(v) for v in r['alleen_in_cursus'].values())}"
            )


if __name__ == "__main__":
    main()
