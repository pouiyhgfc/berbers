#!/usr/bin/env python3
"""
check_dekking.py — dekkingsrapport voor de cursus (plan/BOUWPLAN-CURSUS-UITVOERING.md §7).

Rapport naar stdout + _project/dekking.md:
  * tabel per les (zinnen/kernwoorden/oefeningen/status/gedeeld-met)
  * tabel per contextstring (geclaimd door)
  * lijst buiten-cursus
  * lijst gedeelde claims
  * dunne/concept-lessen

Puur rapportage, geen validator: schrijft niets terug en faalt niet hard (dat is
check_bronnen.py). Verwacht dat bouw_cursus.py al gedraaid heeft (leest de bijgewerkte
'les'-kolom van assets/zinnen/zinnen.csv).
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _bron_data import (  # noqa: E402
    ZINNEN_CSV,
    kernwoorden_auto,
    laad_woordenlijst,
    laad_zinnen,
    resolve_zinnen_grouped,
    woordenlijst_lemma_index,
)
from _manifest import Manifest, load_kaarten, load_lessen  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
LESSEN_DIR = REPO_ROOT / "bron" / "lessen"
KAARTEN_DIR = REPO_ROOT / "bron" / "kaarten"
OEFENINGEN_JSON = REPO_ROOT / "assets" / "oefeningen" / "exercises-nl.json"
UITVOER_MD = REPO_ROOT / "_project" / "dekking.md"


def oefeningen_aantal(les_id: str) -> int:
    if not OEFENINGEN_JSON.exists():
        return 0
    data = json.loads(OEFENINGEN_JSON.read_text(encoding="utf-8"))
    return len(data.get(f"les-{les_id}", []))


def main() -> int:
    lessen = load_lessen(LESSEN_DIR) if LESSEN_DIR.exists() else []
    kaarten = load_kaarten(KAARTEN_DIR)
    context_index, id_index = laad_zinnen()
    woordenlijst_rows = laad_woordenlijst()
    lemma_index = woordenlijst_lemma_index(woordenlijst_rows)

    # Per les: geclaimde contexts + resolved rows.
    les_contexts: dict[str, set[str]] = {}
    les_resolved: dict[str, list[dict]] = {}
    for m in lessen:
        groepen = resolve_zinnen_grouped(m, context_index, id_index)
        les_contexts[m.id] = {w for s, w, _r in groepen if s == "context"}
        les_resolved[m.id] = [r for _s, _w, rows in groepen for r in rows]

    # Gedeelde claims: context -> lessen die 'm claimen (>1 = gedeeld).
    context_naar_lessen: dict[str, list[str]] = {}
    for les_id, contexts in les_contexts.items():
        for c in contexts:
            context_naar_lessen.setdefault(c, []).append(les_id)
    for v in context_naar_lessen.values():
        v.sort()
    gedeelde_claims = {c: v for c, v in context_naar_lessen.items() if len(v) > 1}

    def gedeeld_met(les_id: str) -> list[str]:
        anderen = set()
        for c in les_contexts.get(les_id, ()):
            anderen |= {x for x in context_naar_lessen.get(c, []) if x != les_id}
        return sorted(anderen)

    # zinnen.csv: les-kolom lezen voor buiten-cursus/leesboek-telling.
    with ZINNEN_CSV.open(encoding="utf-8-sig", newline="") as f:
        alle_rijen = list(csv.DictReader(f))
    buiten_cursus = [r for r in alle_rijen if r["les"] == "buiten-cursus"]
    leesboek = [r for r in alle_rijen if r["les"] == "leesboek"]

    regels: list[str] = []
    regels.append("# Dekkingsrapport — cursus\n")

    regels.append("## Per les\n")
    regels.append("| les | slug | zinnen | kernwoorden | oefeningen | status | gedeeld met |")
    regels.append("|---|---|---|---|---|---|---|")
    for m in sorted(lessen, key=lambda m: m.id):
        n_zin = len(les_resolved[m.id])
        n_kern = len(kernwoorden_auto(les_resolved[m.id], lemma_index))
        n_oef = oefeningen_aantal(m.id)
        gd = ", ".join(gedeeld_met(m.id)) or "—"
        regels.append(f"| {m.id} | {m.slug} | {n_zin} | {n_kern} | {n_oef} | {m.status} | {gd} |")
    regels.append("")

    regels.append("## Per contextstring\n")
    regels.append("| contextstring | geclaimd door |")
    regels.append("|---|---|")
    for c in sorted(context_naar_lessen):
        regels.append(f"| {c} | {', '.join(context_naar_lessen[c])} |")
    regels.append("")

    regels.append("## Gedeelde claims\n")
    if gedeelde_claims:
        for c, ls in sorted(gedeelde_claims.items()):
            regels.append(f"- `{c}` — lessen {', '.join(ls)}")
    else:
        regels.append("(geen)")
    regels.append("")

    regels.append("## Dunne / concept-lessen\n")
    bijzonder = [m for m in lessen if m.status in {"dun", "concept"}]
    if bijzonder:
        for m in sorted(bijzonder, key=lambda m: m.id):
            regels.append(f"- les {m.id} ({m.slug}): status {m.status}")
    else:
        regels.append("(geen)")
    regels.append("")

    regels.append(f"## Buiten-cursus ({len(buiten_cursus)} zin(nen))\n")
    regels.append("Zinnen die geen enkele les of kaart claimt en geen `context:text` hebben.")
    regels.append("")

    regels.append(f"## Leesboek ({len(leesboek)} zin(nen))\n")
    regels.append("`context:text`-zinnen buiten het les-37-paginabereik (restregel, → nl/lezen.html).")
    regels.append("")

    tekst = "\n".join(regels) + "\n"
    UITVOER_MD.parent.mkdir(parents=True, exist_ok=True)
    UITVOER_MD.write_text(tekst, encoding="utf-8")
    print(tekst)
    print(f"geschreven: {UITVOER_MD.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
