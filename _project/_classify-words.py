"""
Voegt drie kolommen toe aan woordenlijst.csv:
  - niveau     : CEFR-niveau A1..C2 (heuristisch bepaald)
  - woordsoort : grammaticale categorie (znw_m_ev, ww, vnw, vz, ...)
  - anki_tag   : hierarchische Anki-tags

Werkwijze
---------
NIVEAU
  1. Eerste les in cursus.html waar het woord verschijnt → A1..C2 mapping op
     basis van les-nummer (zie LES_TO_NIVEAU).
  2. Indien niet in cursus: frequentie in _boek-tekst.txt → B2..C2 mapping.
  3. Vaste basis-lijst (BASIS_A1) overschrijft als A1 (handmatige seed).

WOORDSOORT
  1. Vaste lijsten voor closed-class woorden (vnw, vz, voegw, telw, vraagw,
     ontk, aanw_vnw).
  2. Prefix-heuristiek voor zelfstandig naamwoord: ṯa-/ṯi-/a-/i-.
  3. Restcategorie = ww (werkwoord).

ANKI-TAG
  Ruimte-gescheiden hiërarchische tags, te plakken in Anki:
    tarifit::cefr::A1 tarifit::woordsoort::znw_m_ev

Veilig om meerdere keren te draaien — bestaande extra kolommen worden
overschreven. Gebruikt utf-8 en standaard csv-quoting.
"""

import csv
import os
import re
import unicodedata
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
CSV_PATH = os.path.join(ROOT, 'assets', 'woordenlijst', 'woordenlijst.csv')
CURSUS_PATH = os.path.join(ROOT, 'cursus.html')
BOOK_PATH = os.path.join(SCRIPT_DIR, '_boek-tekst.txt')
OVERRIDE_PATH = os.path.join(SCRIPT_DIR, '_classify-overrides.csv')


# ----------------------------------------------------------------------
# CEFR mapping per cursus-les
# ----------------------------------------------------------------------

LES_TO_NIVEAU = {}
for les in range(1, 4):    LES_TO_NIVEAU[les] = 'A1'   # les 1-3
for les in range(4, 8):    LES_TO_NIVEAU[les] = 'A2'   # les 4-7
for les in range(8, 13):   LES_TO_NIVEAU[les] = 'B1'   # les 8-12
for les in range(13, 21):  LES_TO_NIVEAU[les] = 'B2'   # les 13-20
for les in range(21, 29):  LES_TO_NIVEAU[les] = 'C1'   # les 21-28
for les in range(29, 37):  LES_TO_NIVEAU[les] = 'C2'   # les 29-36


# ----------------------------------------------------------------------
# Closed-class lijsten
# ----------------------------------------------------------------------

PERSOONLIJK_VNW = {
    'nec', 'cek', 'cem', 'netta', 'nettaṯ', 'neccin',
    'kenniw', 'kennint', 'niṯni', 'niṯenti',
}

BEZIT_VNW = {
    # bezittelijk suffix-loos
    'inu', 'nnec', 'nnem', 'nnes', 'nney', 'nwem', 'nkent',
    'nsen', 'nsent',
}

VRAAGWOORD = {
    'mani', 'melmi', 'mecḥař', 'manwen', 'menyu', 'mayemmi',
    'mix', 'ma', 'ce', 'mayaa', 'umi', 'min', 'manis', 'mami',
    'manaya', 'manwa', 'manten', 'mayemma',
}

VOORZETSEL = {
    'i', 'di', 'ḏi', 'x', 'n', 'ḏay', 'ɣaa', 'ḵ', 'ar', 'ɣef',
    'fawḏ', 'deg', 'gar', 'zeg', 'ɣir', 'qbeř',
}

ONTKENNING = {
    'waa', 'war', 'ca', 'bu', 'řa', 'ula', 'maca',
}

VOEGWOORD = {
    'arami', 'axmi', 'mara', 'ɣir', 'mli', 'awarni', 'ammu',
    'mecḥař', 'ammi', 'mliḥ', 'ḏ',
}

AANW_VNW = {
    'a', 'in', 'enni', 'ennaṯ', 'an', 'on', 'un',
    'ina', 'inu', 'aya', 'ayenni',
}

TELWOORD = {
    'ijj', 'ṯin', 'sin', 'ṯřaṯa', 'ṛeḇɛa', 'xemsa', 'sebɛa',
    'ṯmenya', 'ṯesɛa', 'ɛecra', 'řatnac', 'ttnayen', 'ṯřata',
    'ṛebɛa', 'xemsa', 'setta', 'sebɛa', 'ṯmanya', 'ṯesɛuḏ',
}


# Handgemaakte A1-basis (~150 essentie-woorden — overschrijft cursus-les
# mapping als woord daar niet in zit, maar wel hier)
BASIS_A1 = {
    # Familie
    'yemma', 'baba', 'uma', 'weltma', 'mmi', 'iţţma', 'jeddi',
    'jedda', 'lwalidin', 'aɛzizen', 'imeddukař',
    # Persoonlijke vnw
    'nec', 'cek', 'cem', 'netta', 'nettaṯ', 'neccin', 'kenniw',
    'kennint', 'niṯni', 'niṯenti',
    # Getallen 1-10
    'ijj', 'ṯin', 'sin', 'ṯřaṯa', 'ṛeḇɛa', 'xemsa', 'setta',
    'sebɛa', 'ṯmenya', 'ṯesɛa', 'ɛecra',
    # Begroetingen / basis
    'azuř', 'řemřic', 'aha', 'wah', 'lla', 'lliḥ',
    # Basis ww
    'eǧa', 'raḥ', 'usi-d', 'ssneɣ', 'ḵḵa', 'ywa',
    # Eten / drinken
    'aɣrum', 'atay', 'aman', 'aksum',
    # Tijd
    'ass', 'ssbeḥ', 'lɛecya', 'iḍ', 'řweqṯ',
    # Lichaamsdelen
    'afus', 'ḍar', 'aqemmum', 'ařəm', 'aqaṛṛuḏ', 'aɛeḏḏis',
}

BASIS_A2 = {
    # Kleuren
    'azegga', 'abercan', 'awessar', 'aẓuwwaɣ', 'azizaw',
    # Dagen
    'řḥed', 'sebṯ', 'řaaṯnayen', 'řaaṯlaṯa', 'řaaṛḇaɛ',
    # Maanden / seizoenen
    'reḇiɛ', 'ṣṣif', 'lxḏif', 'ssḇa',
    # Beroepen
    'amḏan', 'amɛeřřim',
}


# ----------------------------------------------------------------------
# Hulpfuncties
# ----------------------------------------------------------------------

def normalize(s):
    """NFC-normalize (combineer combining-diacritics naar precomposed waar
    mogelijk)."""
    return unicodedata.normalize('NFC', s)


def split_variants(berber):
    """Splitst 'a / b / c' op slashes, returnt lijst genormaliseerde
    varianten."""
    parts = re.split(r'\s*/\s*', berber)
    return [normalize(p.strip()) for p in parts if p.strip()]


def first_lesson_for(words, lessons):
    """Returnt het eerste lesnummer waarin een van de varianten voorkomt
    als zelfstandig token. Returnt None als geen match.

    `lessons` is een dict {nummer: tekst} waarin tekst is alleen tar-content
    van die les."""
    for les_num in sorted(lessons.keys()):
        text = lessons[les_num]
        for w in words:
            # word-boundary (geen Tarifit-letter eromheen)
            pat = re.compile(
                r'(?<![A-Za-zḏḍḥṯṭṣẓřṛḇḵǧžɛɣḷŘƐƔƷʷ\u0331\-])'
                + re.escape(w)
                + r'(?![A-Za-zḏḍḥṯṭṣẓřṛḇḵǧžɛɣḷŘƐƔƷʷ\u0331\-])'
            )
            if pat.search(text):
                return les_num
    return None


def freq_in_book(words, book_text):
    """Returnt het maximum aantal voorkomens onder de varianten."""
    max_count = 0
    for w in words:
        pat = re.compile(
            r'(?<![A-Za-zḏḍḥṯṭṣẓřṛḇḵǧžɛɣḷŘƐƔƷʷ\u0331\-])'
            + re.escape(w)
            + r'(?![A-Za-zḏḍḥṯṭṣẓřṛḇḵǧžɛɣḷŘƐƔƷʷ\u0331\-])'
        )
        n = len(pat.findall(book_text))
        if n > max_count:
            max_count = n
    return max_count


def determine_woordsoort(words, meaning):
    """Heuristische bepaling. Eerste matchende variant telt.

    Volgorde:
      1. Closed-class match  (vnw, vz, etc)
      2. NL-vertaling sterke hint (begin met "de/het/een" of een
         werkwoordsindicator) wint VOOR de Tarifit-prefix-heuristiek,
         omdat veel werkwoorden met `a-`/`i-` beginnen wat ten onrechte
         "znw_m_ev" zou geven.
      3. Tarifit-prefix-heuristiek (alleen bij twijfel)
      4. Default werkwoord
    """
    meaning_lc = meaning.lower().strip()
    words_lc = [w.lower() for w in words]

    for w in words_lc:
        if w in PERSOONLIJK_VNW: return 'vnw_pers'
        if w in BEZIT_VNW: return 'vnw_bez'
        if w in VRAAGWOORD: return 'vraagw'
        if w in VOORZETSEL: return 'vz'
        if w in ONTKENNING: return 'ontk'
        if w in VOEGWOORD: return 'voegw'
        if w in AANW_VNW: return 'vnw_aanw'
        if w in TELWOORD: return 'telw'

    # NL-hints
    is_nl_noun = bool(re.match(r'^(de|het|een)\s+\w', meaning_lc))
    # NL ww-infinitief: enkel woord eindigend op -en (niet -er, want "aannemer"
    # is znw); dekt "aanbranden", "aankomen", etc.
    is_nl_verb_infinitive = bool(
        re.match(r'^[a-zàâéèëïô]+en\s*$', meaning_lc)
        or re.match(r'^[a-zàâéèëïô]+en\s*[/(].*$', meaning_lc)
    )
    # Tweede znw-hint: bevat ergens "(de|het) X"
    has_nl_article = bool(
        re.search(r'\b(de|het|een)\s+[a-zàâéèëïô]+', meaning_lc)
    )
    nominal_hint = is_nl_noun or has_nl_article

    # NL-werkwoord wint van Tarifitse a-/i- prefix
    if is_nl_verb_infinitive and not is_nl_noun:
        return 'ww'

    # Tarifitse prefix-heuristiek
    for w in words_lc:
        if w.startswith('ṯi') and (w.endswith('in') or w.endswith('iwin')):
            return 'znw_v_mv'
        if w.startswith('ṯa'):
            return 'znw_v_ev'
        if w.startswith('ṯi'):
            return 'znw_v_mv'
        if w.startswith('a') and len(w) >= 3:
            return 'znw_m_ev'
        if w.startswith('i') and len(w) >= 3:
            return 'znw_m_mv'
        if (w.startswith('ll') or w.startswith('l')) and nominal_hint:
            return 'znw_m_ev'

    if nominal_hint:
        return 'znw'

    return 'ww'


def determine_niveau(les_num, freq, words, meaning):
    """Bepalt CEFR-niveau via cursus + handlijsten + woord-eenvoud."""
    words_lc = [w.lower() for w in words]

    # 1. Handgemaakte basis-A1 overschrijft alles
    if any(w in BASIS_A1 for w in words_lc):
        return 'A1'

    # 2. Cursus-les bepaalt
    if les_num is not None and les_num in LES_TO_NIVEAU:
        return LES_TO_NIVEAU[les_num]

    # 3. Handgemaakte basis-A2
    if any(w in BASIS_A2 for w in words_lc):
        return 'A2'

    # 4. Heel hoge boekfrequentie hint dat woord centraal is
    if freq >= 50:
        return 'B1'

    # 5. Woord-eenvoud heuristiek: kortere = eenvoudiger
    # Pak de kortste variant (vaak de hoofd-vorm)
    shortest = min(len(w) for w in words)
    if shortest <= 4:
        return 'B1'
    if shortest <= 7:
        return 'B2'
    if shortest <= 10:
        return 'C1'
    return 'C2'


def make_anki_tag(niveau, woordsoort):
    return f'tarifit::cefr::{niveau} tarifit::woordsoort::{woordsoort}'


def load_classify_overrides(path):
    """Optioneel CSV: Berbers,niveau,woordsoort — kolommen leeg = niet overschrijven."""
    out = {}
    if not os.path.isfile(path):
        return out
    with open(path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw = (row.get('Berbers') or row.get('berbers') or '').strip()
            if not raw:
                continue
            key = normalize(raw)
            rec = {}
            nv = (row.get('niveau') or '').strip()
            ws = (row.get('woordsoort') or '').strip()
            if nv:
                rec['niveau'] = nv
            if ws:
                rec['woordsoort'] = ws
            if rec:
                out[key] = rec
    return out


def apply_classify_overrides(variants, niveau, woordsoort, overrides):
    for v in variants:
        ovr = overrides.get(v)
        if not ovr:
            continue
        if ovr.get('niveau'):
            niveau = ovr['niveau']
        if ovr.get('woordsoort'):
            woordsoort = ovr['woordsoort']
        break
    return niveau, woordsoort


# ----------------------------------------------------------------------
# Cursus-tekst per les inlezen
# ----------------------------------------------------------------------

with open(CURSUS_PATH, 'r', encoding='utf-8') as f:
    cursus_html = f.read()

# Splits op <section id="les-NN">
les_pattern = re.compile(
    r'<section\s+id="les-(\d+)"[^>]*>(.*?)(?=<section\s+id="les-\d+"|</main)',
    re.DOTALL,
)
LESSONS = {}
for m in les_pattern.finditer(cursus_html):
    num = int(m.group(1))
    body = m.group(2)
    # Pak alle tar-content uit deze les
    tar_pat = re.compile(
        r'<(?:span|em)[^>]*class="[^"]*\btar\b[^"]*"[^>]*>([^<]*)</(?:span|em)>',
        re.IGNORECASE,
    )
    tar_chunks = tar_pat.findall(body)
    LESSONS[num] = ' '.join(tar_chunks)

print(f'Cursus geladen: {len(LESSONS)} lessen, '
      f'{sum(len(t) for t in LESSONS.values())} tekens tar-content.')

OVERRIDES = load_classify_overrides(OVERRIDE_PATH)
if OVERRIDES:
    print(f'Classify-overrides: {len(OVERRIDES)} regels uit {OVERRIDE_PATH}')
else:
    print(f'Geen overrides ({OVERRIDE_PATH} ontbreekt of leeg).')


# ----------------------------------------------------------------------
# Boek-tekst inlezen
# ----------------------------------------------------------------------

if os.path.exists(BOOK_PATH):
    with open(BOOK_PATH, 'r', encoding='utf-8') as f:
        BOOK_TEXT = normalize(f.read())
    print(f'Boek geladen: {len(BOOK_TEXT)} tekens.')
else:
    BOOK_TEXT = ''
    print(f'Geen boek gevonden op {BOOK_PATH} — frequentie wordt 0.')


# ----------------------------------------------------------------------
# CSV verwerken
# ----------------------------------------------------------------------

with open(CSV_PATH, 'r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]
print(f'CSV header was: {header}')

# Schrijf nieuwe header
new_header = ['Berbers', 'Nederlands', 'niveau', 'woordsoort', 'anki_tag']
new_rows = [new_header]

stats_niveau = Counter()
stats_woordsoort = Counter()

for row in rows[1:]:
    if len(row) < 2:
        continue
    berber = normalize(row[0])
    meaning = row[1]
    if not berber.strip() or not meaning.strip():
        continue

    variants = split_variants(berber)

    les_num = first_lesson_for(variants, LESSONS)
    freq = freq_in_book(variants, BOOK_TEXT)
    woordsoort = determine_woordsoort(variants, meaning)
    niveau = determine_niveau(les_num, freq, variants, meaning)
    niveau, woordsoort = apply_classify_overrides(variants, niveau, woordsoort, OVERRIDES)
    anki = make_anki_tag(niveau, woordsoort)

    stats_niveau[niveau] += 1
    stats_woordsoort[woordsoort] += 1

    new_rows.append([berber, meaning, niveau, woordsoort, anki])


with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerows(new_rows)


print('\n=== Niveau-verdeling ===')
for niv in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']:
    print(f'  {niv}: {stats_niveau[niv]}')

print('\n=== Woordsoort-verdeling ===')
for ws, n in stats_woordsoort.most_common():
    print(f'  {ws}: {n}')

print(f'\nTotaal: {len(new_rows) - 1} woorden naar CSV geschreven.')
