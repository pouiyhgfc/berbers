"""
Past spellingcorrecties toe op woordenlijst.csv, uitleg.html en cursus.html.

Drie categorieën correcties:
  1. ǧ → ž   (CSV gebruikte ž als hoofdvorm; 2 woorden hadden nog ǧ)
  2. ɣar → ɣaa  (preposition 'naar/bij')
  3. j → y of ž  (Berbers j is y, Arabisch j is ž — per woord)

Voor de HTML-bestanden: vervangingen alleen binnen .tar (Tarifit-tekst), 
niet in lopende NL-tekst, om "ja" / "jij" etc. niet te raken.
"""

import csv
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
CSV_PATH = os.path.join(ROOT, 'assets', 'woordenlijst', 'woordenlijst.csv')
UITLEG_PATH = os.path.join(ROOT, 'uitleg.html')
CURSUS_PATH = os.path.join(ROOT, 'cursus.html')

# ----------------------------------------------------------------------
# Mapping van oud → nieuw (alle bekende correcties)
# ----------------------------------------------------------------------

REPLACEMENTS = {
    # ǧ → ž (2 in CSV)
    'aǧun': 'ažun',
    'feǧeq': 'fežeq',

    # ɣar → ɣaa (woordgrens — andere woorden met 'ɣar' in midden blijven)
    'ɣar': 'ɣaa',

    # Berbers j → y (semi-klinker)
    'Ajidar': 'Ayidar',
    'sennej': 'senney',
    'řeynuj': 'řeynuy',
    'mjaa': 'myaa',
    'ajemmad-in': 'ayemmad-in',
    'iggʷej': 'iggʷey',
    'jjawen': 'yyawen',

    # Arabisch j → ž (zh-klank)
    'ṯajarṛarṯ': 'ṯažarṛarṯ',
    'ṯaqmijaṯ': 'ṯaqmižaṯ',
    'musejjala': 'musežžala',
    'ṯṯajriba': 'ṯṯažriba',
    'lgaṛaj': 'lgaṛaž',
    'joɛ': 'žoɛ',
    'ṯallajṯ': 'ṯallažṯ',
    'ljarima': 'lžarima',
    'ayenja': 'ayenža',
    'pijama': 'pižama',
    'ḍṛuj': 'ḍṛuž',
    'jar': 'žar',
    'ljamiɛa': 'lžamiɛa',
    'ṯḥajiṯ': 'ṯḥažiṯ',
    'jjib': 'žžib',
    'řejbub': 'řežbub',
    'sewjeḏ': 'sewžeḏ',
    'ssewjeḏ': 'ssewžeḏ',
    'qežjḏeḥ': 'qežyḏeḥ',  # typo: y, niet j
}

# Sorteer langste-eerst zodat 'ssewjeḏ' eerder matcht dan 'sewjeḏ'
SORTED_KEYS = sorted(REPLACEMENTS.keys(), key=len, reverse=True)

# yaa-preposition (incl. afgeleide vormen met clitic-suffixen) → ɣaa
# Belangrijk: zorg dat 'yaaḏen' (tarwe), 'yiyyaa' (veld), 'yemyaa' (groot)
# en andere woorden waarvan 'yaa' deel uitmaakt NIET worden geraakt.
# Volgorde van suffixen: langste eerst (greedy alternation in Python re)
YAA_PREP = re.compile(
    r'(?<![A-Za-zḏḍḥṯṭṣẓřṛḇḵǧžɛɣḷŘƐƔƷʷ\u0331\-])'
    r'yaa(senṯ|kenṯ|sen|ney|wem|s|k|m)?'
    r'(?=[\s<.,;:!?\)"\']|$)'
)


def replace_in_text(text):
    """Past alle mappings toe op een stuk tekst, met woordgrens-bewaking."""
    changes = []

    TARIFIT_LETTER = r"[A-Za-zḏḍḥṯṭṣẓřṛḇḵǧžɛɣḷŘƐƔƷʷ\u0331\-]"

    for old in SORTED_KEYS:
        new = REPLACEMENTS[old]
        pattern = re.compile(
            r'(?<!' + TARIFIT_LETTER + r')'
            + re.escape(old)
            + r'(?!' + TARIFIT_LETTER + r')'
        )
        new_text, n = pattern.subn(new, text)
        if n:
            changes.append((old, new, n))
            text = new_text

    # yaa-preposition → ɣaa (na alle andere vervangingen, om interferentie
    # te vermijden)
    yaa_count = [0]

    def yaa_repl(m):
        yaa_count[0] += 1
        suffix = m.group(1) or ''
        return 'ɣaa' + suffix

    new_text = YAA_PREP.sub(yaa_repl, text)
    if yaa_count[0]:
        changes.append(('yaa(prep)', 'ɣaa(prep)', yaa_count[0]))
        text = new_text

    return text, changes


# ----------------------------------------------------------------------
# 1. CSV — beide kolommen (Tarifit + NL-uitleg kan ook tarifit-tokens bevatten)
# ----------------------------------------------------------------------

print('=== woordenlijst.csv ===')
with open(CSV_PATH, 'r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    rows = list(reader)

total_changes = 0
for i, row in enumerate(rows):
    new_row = []
    for j, cell in enumerate(row):
        new_cell, changes = replace_in_text(cell)
        if changes:
            for old, new, n in changes:
                print(f'  rij {i+1} kol {j+1}: {old!r} → {new!r} ×{n}')
                total_changes += n
        new_row.append(new_cell)
    rows[i] = new_row

with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerows(rows)
print(f'CSV: {total_changes} wijzigingen toegepast.\n')


# ----------------------------------------------------------------------
# 2. HTML — alleen binnen .tar-spans/em's, niet in lopende NL-tekst
# ----------------------------------------------------------------------

def replace_in_html_tar_only(html):
    """
    Zoek <span class="tar">...</span>, <em class="tar">...</em>, en doe daar
    de vervangingen. Voor de inhoud van een sectie waar de hele paragraaf
    Tarifit is (ze gebruiken soms `<span class="tar">…</span>` over een
    hele zin), volstaat dit.
    """
    pattern = re.compile(
        r'(<(?:span|em)[^>]*class="[^"]*\btar\b[^"]*"[^>]*>)([^<]*)(</(?:span|em)>)',
        flags=re.IGNORECASE,
    )

    summary = []

    def repl(m):
        opening, inner, closing = m.group(1), m.group(2), m.group(3)
        new_inner, changes = replace_in_text(inner)
        for old, new, n in changes:
            summary.append((old, new, n))
        return opening + new_inner + closing

    new_html = pattern.sub(repl, html)
    return new_html, summary


for label, path in [('uitleg.html', UITLEG_PATH), ('cursus.html', CURSUS_PATH)]:
    print(f'=== {label} ===')
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    new_html, summary = replace_in_html_tar_only(html)
    # Aggregate per (old, new) tuple
    agg = {}
    for old, new, n in summary:
        agg[(old, new)] = agg.get((old, new), 0) + n
    for (old, new), n in sorted(agg.items()):
        print(f'  {old!r} → {new!r} ×{n}')
    if new_html != html:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f'{label}: {sum(agg.values())} wijzigingen geschreven.\n')
    else:
        print(f'{label}: geen wijzigingen.\n')


print('Klaar.')
