"""
Fase 3, Stap 3.5 — NL/EN-pariteitscheck.

De Tarifit-tekst in de NL- en EN-bronpagina's hoort identiek te zijn; alleen de uitleg-taal
verschilt. Deze check vergelijkt de Tarifit-tokenverzamelingen:
    nl/cursus.html  ↔  en/course.html
    nl/uitleg.html  ↔  en/grammar.html
en meldt per paar de verschillen.

Kalibratie (plan): draai deze check één keer op de huidige bestanden. Zijn er nu al bewuste
verschillen, zet de check dan eerst op *waarschuwen*; maak hem hard zodra NL/EN gelijk zijn.
De modus wordt vastgelegd in PARITY_MODE hieronder, zodat `make parity` zich consistent gedraagt.

Gebruik:
    python _project/scripts/check_parity.py            # gebruikt PARITY_MODE
    python _project/scripts/check_parity.py --strict    # forceer hard falen
    python _project/scripts/check_parity.py --warn       # forceer alleen waarschuwen
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _gen_common import load_main, tar_tokens_from_html  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]

# "warn"  = verschillen melden maar exit 0 (gekalibreerd: NL/EN lopen nu nog uiteen).
# "strict" = falen (exit 1) bij elk verschil. Zet op "strict" zodra de paren gelijk zijn.
PARITY_MODE = "warn"

PAIRS = [
    ("cursus ↔ course", ROOT / "nl/cursus.html", ROOT / "en/course.html"),
    ("uitleg ↔ grammar", ROOT / "nl/uitleg.html", ROOT / "en/grammar.html"),
]

# Hoeveel afwijkende tokens we maximaal tonen per richting (de rest wordt samengevat).
SHOW = 25


def compare(nl_path: Path, en_path: Path) -> tuple[set[str], set[str]]:
    _, nl_main = load_main(nl_path)
    _, en_main = load_main(en_path)
    nl = tar_tokens_from_html(nl_main)
    en = tar_tokens_from_html(en_main)
    return nl - en, en - nl  # (alleen NL, alleen EN)


def _sample(tokens: set[str]) -> str:
    items = sorted(tokens)
    if len(items) <= SHOW:
        return ", ".join(items)
    return ", ".join(items[:SHOW]) + f", … (+{len(items) - SHOW} meer)"


def main() -> None:
    mode = PARITY_MODE
    if "--strict" in sys.argv:
        mode = "strict"
    elif "--warn" in sys.argv:
        mode = "warn"

    any_diff = False
    print(f"NL/EN-pariteitscheck (modus: {mode})")
    for label, nl_path, en_path in PAIRS:
        only_nl, only_en = compare(nl_path, en_path)
        n = len(only_nl) + len(only_en)
        if n == 0:
            print(f"  ✓ {label}: identieke Tarifit-tokenverzameling")
            continue
        any_diff = True
        print(f"  ✗ {label}: {len(only_nl)} alleen-NL, {len(only_en)} alleen-EN")
        if only_nl:
            print(f"      alleen in {nl_path.name}: {_sample(only_nl)}")
        if only_en:
            print(f"      alleen in {en_path.name}: {_sample(only_en)}")

    if not any_diff:
        print("Pariteit OK — alle paren gelijk.")
        return

    if mode == "strict":
        sys.exit("FOUT: NL/EN-Tarifit-pariteit niet gehaald (zie verschillen hierboven).")
    print(
        "\nWAARSCHUWING: NL/EN lopen uiteen (gekalibreerde 'warn'-modus). "
        "Zet PARITY_MODE op 'strict' zodra de paren gelijk zijn."
    )


if __name__ == "__main__":
    main()
