"""
Audit-script: vergelijkt alle Tarifit-tokens in uitleg.html met de CSV.

Output: woord-audit.md met:
  - Sectie 1: Tokens die afwijken van CSV qua spelling (mismatched notatie)
  - Sectie 2: Tokens die niet in CSV staan (mogelijk typo of niet opgenomen)
  - Sectie 3: Statistieken
"""

import csv
import os
import re
import unicodedata
from collections import defaultdict
from html.parser import HTMLParser

# Paden zijn relatief aan dit script, zodat het werkt ongeacht waar je het draait.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
CSV_PATH = os.path.join(ROOT, 'assets', 'woordenlijst', 'woordenlijst.csv')
UITLEG_PATH = os.path.join(ROOT, 'uitleg.html')
OUTPUT_PATH = os.path.join(SCRIPT_DIR, 'woord-audit.md')

# ---- 1. Lees CSV ----
csv_words = {}  # normalized -> list of (original_form, meaning)
csv_originals = set()  # voor exacte match-check

def normalize(s):
    """Normaliseer voor fuzzy matching: lowercase, strip diakrieten, map speciale tekens."""
    s = s.lower()
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = (s
        .replace('ḏ', 'd').replace('ḍ', 'd')
        .replace('ṯ', 't').replace('ṭ', 't')
        .replace('ḥ', 'h')
        .replace('ɣ', 'g').replace('ɛ', 'a')
        .replace('ř', 'r').replace('ṛ', 'r')
        .replace('ẓ', 'z').replace('ž', 'j')
        .replace('ṣ', 's')
        .replace('ǧ', 'g').replace('ḇ', 'b').replace('ḵ', 'k').replace('ḷ', 'l')
    )
    return s

with open(CSV_PATH, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) < 2: continue
        word = row[0].strip()
        meaning = row[1].strip()
        if not word: continue
        for variant in [v.strip() for v in word.split('/')]:
            if not variant: continue
            csv_originals.add(variant)
            n = normalize(variant)
            csv_words.setdefault(n, []).append((variant, meaning))

# ---- 2. Parse uitleg.html — verzamel <em> tokens met sectie-context ----

class TokenCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tokens = []  # list of (token, current_section)
        self.in_em = False
        self.current_section = "(geen)"
        self.section_stack = []
        self.text_buffer = ""
        self.in_h1 = False
        self.in_h2 = False
        self.in_h3 = False
        self.heading_buffer = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'em':
            self.in_em = True
            self.text_buffer = ""
        elif tag == 'h1':
            self.in_h1 = True
            self.heading_buffer = ""
        elif tag == 'h2':
            self.in_h2 = True
            self.heading_buffer = ""

    def handle_endtag(self, tag):
        if tag == 'em' and self.in_em:
            self.in_em = False
            t = self.text_buffer.strip()
            if t:
                self.tokens.append((t, self.current_section))
            self.text_buffer = ""
        elif tag == 'h1' and self.in_h1:
            self.in_h1 = False
            self.current_section = self.heading_buffer.strip()
            self.heading_buffer = ""
        elif tag == 'h2' and self.in_h2:
            self.in_h2 = False
            sub = self.heading_buffer.strip()
            if sub:
                # Behoud hoofdstuk + voeg sub toe
                base = self.current_section.split(' › ')[0] if ' › ' in self.current_section else self.current_section
                self.current_section = f"{base} › {sub}"
            self.heading_buffer = ""

    def handle_data(self, data):
        if self.in_em:
            self.text_buffer += data
        if self.in_h1 or self.in_h2:
            self.heading_buffer += data

with open(UITLEG_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

parser = TokenCollector()
parser.feed(html)

# ---- 3. Filter: alleen Tarifit-achtige tokens ----
# Een token is "Tarifit" als:
#  - bevat ten minste één Tarifit-specifieke letter (ḏ ḥ ɛ ɣ ř ṛ ṣ ṭ ẓ ǧ ḇ ḵ ž ṯ ḍ ḷ + combining marks)
#  - OF matcht (na normalisatie) iets in de CSV

TARIFIT_CHARS = set('ḏḥɛɣřṛṣṭẓǧḇḵžṯḍḷĦḤŘƐƔ')

def has_tarifit_chars(token):
    if any(c in TARIFIT_CHARS for c in token):
        return True
    # Check ook combining marks (t̲, b̲)
    nfd = unicodedata.normalize('NFD', token)
    if any(unicodedata.category(c) == 'Mn' for c in nfd):
        return True
    return False

# Bekende niet-Tarifit-woorden die in <em> kunnen staan (Engels/Nederlands voorbeelden)
# We filteren ze er uit zodat ze niet als 'niet-in-CSV' worden gemarkeerd
NON_TARIFIT_HINTS = {
    'this', 'think', 'thin', 'show', 'china', 'joke', 'but', 'the', 'duh',
    'déjà-vu', 'déjà', 'kat', 'bad', 'bier', 'boek', 'lachen', 'dat', 'die',
    'show', 'sh', 'tch', 'ggw', 'kkw',  # IPA-achtige / fonetische
    'pero', 'perro', 'queso', 'banco', 'gato',  # Spaans
    'tch', 'sh', 'ng',  # fonetische
    'a', 'i', 'u', 'e',  # losse klinker-letters
    'b', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'w', 'x', 'y', 'z',  # losse medeklinker-letters
    'tmazight', 'Tarifit', 'tarifit', 'Tarifiyt', 'Mourigh', 'Kossmann',  # eigennamen
    'Groningen', 'displays', 'bad',  # Nederlands voorbeelden
    'ad', 'qa', 'tuya',  # partikels - die staan wel in CSV
    'show', 'bin', 'duh', 'I work', 'I am working',  # Engelse voorbeeldzinnen
}

# Categorieen
exact_match = []          # token komt exact voor in CSV
diacritic_mismatch = []   # token komt voor na normalisatie maar niet exact (notatie-issue)
not_in_csv = []           # token niet in CSV in welke vorm dan ook

token_count = defaultdict(int)
token_locations = defaultdict(list)
for t, sec in parser.tokens:
    token_count[t] += 1
    if sec not in token_locations[t]:
        token_locations[t].append(sec)

unique_tokens = list(token_count.keys())

for t in unique_tokens:
    # Skip lege tokens of zinnen (met spatie)
    if ' ' in t or len(t) < 2:
        continue
    # Niet checken als duidelijk niet-Tarifit
    if t in NON_TARIFIT_HINTS:
        continue
    # Skip puur numerieke of cijfers
    if re.match(r'^[\d.,]+$', t):
        continue
    # Filter: alleen Tarifit-achtige
    if not has_tarifit_chars(t):
        # Geen diakrieten — kan nog steeds Tarifit zijn (bv. afunas)
        # Check fuzzy in CSV; alleen meedoen als matcht
        n = normalize(t)
        if n not in csv_words:
            continue  # Skippen — vermoedelijk niet-Tarifit (Engels/NL)
    
    # Check matches
    if t in csv_originals:
        exact_match.append(t)
    else:
        n = normalize(t)
        if n in csv_words:
            diacritic_mismatch.append((t, csv_words[n]))
        else:
            not_in_csv.append(t)

# Sort
exact_match.sort()
diacritic_mismatch.sort(key=lambda x: x[0])
not_in_csv.sort()

# ---- 4. Schrijf woord-audit.md ----
out = []
out.append('# Woord-audit van uitleg.html tegen woordenlijst.csv\n')
out.append('Automatisch gegenereerd. Vergelijkt elk Tarifit-token in `uitleg.html` (alle `<em>...</em>` tags) met de CSV.\n')
out.append('## Samenvatting\n')
out.append(f'- **Unieke Tarifit-tokens in uitleg.html**: {len(exact_match) + len(diacritic_mismatch) + len(not_in_csv)}')
out.append(f'- **Exacte match met CSV**: {len(exact_match)}')
out.append(f'- **Match na diakrieten-normalisatie (notatie-mismatch)**: {len(diacritic_mismatch)}')
out.append(f'- **Niet in CSV (in welke vorm dan ook)**: {len(not_in_csv)}\n')

out.append('---\n')
out.append('## Sectie 1 — Notatie-mismatches\n')
out.append('Tokens in uitleg die schrijfwijzelijk afwijken van de CSV. CSV is leidend.\n')
out.append('| Token in uitleg | CSV-vorm(en) | Aantal x | Voorkomt in |')
out.append('|---|---|---|---|')
for token, csv_matches in diacritic_mismatch:
    csv_forms = ' / '.join(set(f'`{m[0]}`' for m in csv_matches))
    locations = '; '.join(token_locations[token][:2])  # eerste 2 locaties
    if len(token_locations[token]) > 2:
        locations += f' (+{len(token_locations[token])-2} meer)'
    out.append(f'| `{token}` | {csv_forms} | {token_count[token]}× | {locations} |')

out.append('\n---\n')
out.append('## Sectie 2 — Niet in CSV\n')
out.append('Tokens die mogelijk Tarifit zijn maar in geen enkele vorm in de CSV staan. Kunnen typo\'s zijn, OCR-fouten in de uitleg, of geldige woorden die niet in deze CSV-versie zijn opgenomen.\n')
out.append('| Token | Aantal x | Voorkomt in |')
out.append('|---|---|---|')
for token in not_in_csv:
    locations = '; '.join(token_locations[token][:2])
    if len(token_locations[token]) > 2:
        locations += f' (+{len(token_locations[token])-2} meer)'
    out.append(f'| `{token}` | {token_count[token]}× | {locations} |')

out.append('\n---\n')
out.append('## Sectie 3 — Exacte matches\n')
out.append(f'{len(exact_match)} tokens kloppen exact met CSV. (Niet uitgeschreven om het document leesbaar te houden.)\n')

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print(f'woord-audit.md geschreven.')
print(f'Stats: {len(exact_match)} exact, {len(diacritic_mismatch)} mismatch, {len(not_in_csv)} niet-in-CSV')
