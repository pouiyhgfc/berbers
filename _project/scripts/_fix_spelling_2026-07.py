"""
Spellingcorrecties (2026-07), opgegeven door de gebruiker:

  1. woordenlijst.csv: yyawen -> jjawen (specifieke woordcorrectie)
  2. assets/zinnen/zinnen_en.md: binnen het "tarifit"-veld van elke regel:
       gh -> ɣ
       dj -> ǧ
       7  -> ḥ
     (oude ASCII-transliteratie uit de brontekst, niet toegepast op
     "vertaling"/"context"/andere velden om Engelse woorden als "night",
     "eighty", "ghost" niet te raken.)

Niet met de hand herdraaien zonder de tellingen te controleren; dit is een
eenmalig correctiescript, geen onderdeel van `make build`.
"""

import csv
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
CSV_PATH = os.path.join(ROOT, 'assets', 'woordenlijst', 'woordenlijst.csv')
ZINNEN_PATH = os.path.join(ROOT, 'assets', 'zinnen', 'zinnen_en.md')


# ----------------------------------------------------------------------
# 1. woordenlijst.csv: yyawen -> jjawen
# ----------------------------------------------------------------------

print('=== woordenlijst.csv ===')
with open(CSV_PATH, 'r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    rows = list(reader)

count = 0
for row in rows:
    for j, cell in enumerate(row):
        if re.search(r'(?<![A-Za-zḏḍḥṯṭṣẓřṛḇḵǧžɛɣḷ])yyawen(?![A-Za-zḏḍḥṯṭṣẓřṛḇḵǧžɛɣḷ])', cell):
            new_cell = re.sub(r'(?<![A-Za-zḏḍḥṯṭṣẓřṛḇḵǧžɛɣḷ])yyawen(?![A-Za-zḏḍḥṯṭṣẓřṛḇḵǧžɛɣḷ])', 'jjawen', cell)
            print(f'  kol {j+1}: {cell!r} -> {new_cell!r}')
            row[j] = new_cell
            count += 1

with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerows(rows)
print(f'CSV: {count} wijziging(en) toegepast.\n')


# ----------------------------------------------------------------------
# 2. zinnen_en.md: gh -> ɣ, dj -> ǧ, 7 -> ḥ, alleen in het "tarifit"-veld
# ----------------------------------------------------------------------

TARIFIT_FIELD = re.compile(r'"tarifit":"((?:[^"\\]|\\.)*)"')

REPLACEMENTS = [
    ('gh', 'ɣ'),
    ('dj', 'ǧ'),
    ('7', 'ḥ'),
]


def fix_tarifit_value(value):
    changes = []
    for old, new in REPLACEMENTS:
        n = value.count(old)
        if n:
            value = value.replace(old, new)
            changes.append((old, new, n))
    return value, changes


print('=== zinnen_en.md ===')
with open(ZINNEN_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

total_changes = {}
out_lines = []
for i, line in enumerate(lines):
    m = TARIFIT_FIELD.search(line)
    if not m:
        out_lines.append(line)
        continue

    old_value = m.group(1)
    new_value, changes = fix_tarifit_value(old_value)
    if changes:
        for old, new, n in changes:
            total_changes[(old, new)] = total_changes.get((old, new), 0) + n
        line = line[:m.start(1)] + new_value + line[m.end(1):]
    out_lines.append(line)

with open(ZINNEN_PATH, 'w', encoding='utf-8') as f:
    f.writelines(out_lines)

for (old, new), n in sorted(total_changes.items()):
    print(f'  {old!r} -> {new!r}: {n}x')
print(f'zinnen_en.md: {sum(total_changes.values())} vervanging(en) toegepast.\n')

print('Klaar.')
