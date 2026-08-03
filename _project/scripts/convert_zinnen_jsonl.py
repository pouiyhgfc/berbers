"""
Eenmalige migratie: gecureerde OCR-zinnen (JSONL-regels in een .md)  ->  assets/zinnen/zinnen.csv

Invoerformaat (één JSON-object per regel; andere regels zoals ```-fences worden overgeslagen):
    {"id":"p205-03","tarifit":"iaɛjeb-ayi rḥar","vertaling":"I am pleased (...)","pagina":205,"context":"Word list"}

Mapping naar het CSV-schema:
    tarifit   <- tarifit     (LETTERLIJK — geen normalisatie, geen strip behalve randwitruimte)
    nl        <- leeg        (wordt later in batch gevuld uit `en`, zie plan stap 1.8)
    en        <- vertaling   (de inhoud is Engels, ondanks de Nederlandse sleutelnaam)
    gloss     <- leeg
    hoofdstuk <- leeg        (later verrijken)
    les       <- leeg
    bron      <- "boek p. {pagina}"
    tags      <- "id:{id};context:{context-in-kleine-letters-met-koppeltekens}"

Veiligheid:
- Weigert te draaien als zinnen.csv al datarijen bevat, tenzij --force (dan volledig herschreven).
- Dubbel `id` -> harde fout met beide regelnummers.
- Regel met ontbrekend `tarifit` -> harde fout (een sleutelfout in de JSON kan geen Tarifit
  verzinnen, dus dit moet in de bron gefixt worden).
- Regel met ontbrekend/`null` `vertaling` -> WORDT OVERGESLAGEN (niet hard gefaald): een vertaling
  verzinnen mag niet, en één ontbrekende glos mag de migratie van de overige ~1200 zinnen niet
  blokkeren. Overgeslagen regels worden aan het eind gemeld met regelnummer + id, zodat niets
  stilzwijgend verdwijnt — vul de vertaling later aan uit het boek en voeg de zin met de hand toe
  aan zinnen.csv.

Draaien:  python _project/scripts/convert_zinnen_jsonl.py <pad-naar-md> [--force]
"""

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/zinnen/zinnen.csv"
KOLOMMEN = ["tarifit", "nl", "en", "gloss", "hoofdstuk", "les", "bron", "tags"]


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--force"]
    force = "--force" in sys.argv
    if len(args) != 1:
        sys.exit("Gebruik: convert_zinnen_jsonl.py <pad-naar-md> [--force]")
    src = Path(args[0])
    if not src.exists():
        sys.exit(f"FOUT: {src} bestaat niet.")

    if OUT.exists() and not force:
        with open(OUT, encoding="utf-8-sig", newline="") as f:
            if sum(1 for _ in csv.DictReader(f)) > 0:
                sys.exit(f"FOUT: {OUT.relative_to(ROOT)} bevat al datarijen. Gebruik --force om te herschrijven.")

    rows, seen_ids, skipped, zonder_vertaling = [], {}, 0, []
    for lineno, line in enumerate(src.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line.startswith("{"):
            if line:
                skipped += 1
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            sys.exit(f"FOUT: regel {lineno} is geen geldige JSON: {e}")

        tarifit = (obj.get("tarifit") or "").strip()
        vertaling = (obj.get("vertaling") or "").strip()
        zid = (obj.get("id") or "").strip()
        if not tarifit:
            sys.exit(f"FOUT: regel {lineno} mist tarifit — repareer de bron, ik vul niets aan.")
        if not vertaling:
            zonder_vertaling.append((lineno, zid or "?", tarifit))
            continue  # geen vertaling om over te nemen — verzin er geen, sla de rij over
        if zid:
            if zid in seen_ids:
                sys.exit(f"FOUT: id '{zid}' staat dubbel (regel {seen_ids[zid]} en {lineno}).")
            seen_ids[zid] = lineno

        pagina = obj.get("pagina")
        context = (obj.get("context") or "").strip().lower().replace(" ", "-")
        tags = ";".join(x for x in (f"id:{zid}" if zid else "", f"context:{context}" if context else "") if x)
        rows.append({
            "tarifit": tarifit,
            "nl": "",
            "en": vertaling,
            "gloss": "",
            "hoofdstuk": "",
            "les": "",
            "bron": f"boek p. {pagina}" if pagina is not None else "",
            "tags": tags,
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=KOLOMMEN)
        w.writeheader()
        w.writerows(rows)
    print(f"Geschreven: {OUT.relative_to(ROOT)}  ({len(rows)} zinnen, {skipped} niet-JSON-regels overgeslagen)")
    if zonder_vertaling:
        print(f"  Overgeslagen zonder vertaling ({len(zonder_vertaling)}) — later met de hand aanvullen:")
        for lineno, zid, tarifit in zonder_vertaling:
            print(f"    - regel {lineno} (id={zid}): tarifit={tarifit!r}")
    print("Volgende stappen: make build && make check · daarna NL-batch (plan stap 1.8).")


if __name__ == "__main__":
    main()
