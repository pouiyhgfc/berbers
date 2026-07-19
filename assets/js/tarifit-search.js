// ==============================================================
// tarifit-search.js — gedeelde CSV-parser + zoeknormalisatie
//
// Gelicht uit nl/woordenlijst.html (PLAN-ZINNEN-WEBSITE.md, stap 1.1). Gedeeld door de
// woordenlijst- en zinnen-pagina's (NL+EN), zodat "7ar"/"ghar"/"taddart"-achtige
// internet-spelling overal hetzelfde geattesteerde woord/zin vindt. Geen modules — gewone
// globals, zoals de rest van de site.
// ==============================================================

// --------------------------------------------------------------
// CSV-parser — handelt quoted velden en escaped quotes correct af
// --------------------------------------------------------------
function parseCSV(text) {
  const rows = [];
  let field = '';
  let row = [];
  let inQuotes = false;
  let i = 0;
  while (i < text.length) {
    const c = text[i];
    if (inQuotes) {
      if (c === '"' && text[i + 1] === '"') { field += '"'; i += 2; continue; }
      if (c === '"') { inQuotes = false; i++; continue; }
      field += c; i++; continue;
    }
    if (c === '"') { inQuotes = true; i++; continue; }
    if (c === ',') { row.push(field); field = ''; i++; continue; }
    if (c === '\r') { i++; continue; }
    if (c === '\n') {
      row.push(field); field = '';
      if (row.some(v => v.trim() !== '')) rows.push(row);
      row = []; i++; continue;
    }
    field += c; i++;
  }
  if (field !== '' || row.length > 0) {
    row.push(field);
    if (row.some(v => v.trim() !== '')) rows.push(row);
  }
  return rows;
}

// --------------------------------------------------------------
// Letter-mapping: van eerste karakter naar groep-letter (woordenlijst)
// --------------------------------------------------------------
const LETTER_MAP = {
  'a': 'A', 'b': 'B', 'ḇ': 'B',
  'c': 'C',
  'd': 'D', 'ḍ': 'D', 'ḏ': 'D',
  'e': 'E',
  'f': 'F',
  'g': 'G',
  'h': 'H', 'ḥ': 'Ḥ',
  'i': 'I',
  'k': 'K', 'ḵ': 'K',
  'l': 'L', 'ḷ': 'L',
  'm': 'M',
  'n': 'N',
  'o': 'O',
  'p': 'P',
  'q': 'Q',
  'r': 'R', 'ř': 'Ř', 'ṛ': 'R',
  's': 'S', 'ṣ': 'S',
  't': 'T', 'ṭ': 'T', 'ṯ': 'T',
  'u': 'U',
  'v': 'V',
  'w': 'W',
  'x': 'X',
  'y': 'Y',
  'z': 'Z', 'ẓ': 'Z', 'ǧ': 'Ǧ',
  'ɛ': 'Ɛ',
  'ɣ': 'Ɣ'
};

const LETTERS_ORDER = [
  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'Ḥ',
  'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'Ř',
  'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Ǧ', 'Ɛ', 'Ɣ'
];

function getLetter(word) {
  // Pak het deel vóór de eerste '/' (varianten zoals "ssiɣ / ccel")
  const main = word.split('/')[0].trim().toLowerCase();
  if (!main) return '?';
  // Eerst: probeer het originele karakter — zo behouden ḥ, ǧ, ɛ, ř etc. hun eigen rubriek
  const orig = main[0];
  if (LETTER_MAP[orig]) return LETTER_MAP[orig];
  // Fallback: voor decomposed vormen (t + combining U+0331) eerst combining marks strippen
  const stripped = main.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  const c = stripped[0] || orig;
  return LETTER_MAP[c] || c.toUpperCase();
}

// --------------------------------------------------------------
// Normaliseren voor zoeken — alle diakrieten en internet-spellingsvarianten
// worden teruggebracht naar basisletters
// --------------------------------------------------------------
function normalize(s) {
  // Internet-spelling (zelfde tabel als _ai/index.md §13): cijfer/digraaf -> Tarifit-letter,
  // vóór de diakriet-afplatting hieronder, zodat "ia3jeb" en "iaɛjeb" hetzelfde platslaan.
  s = s.toLowerCase().replace(/gh/g, 'ɣ').replace(/3/g, 'ɛ').replace(/7/g, 'ḥ').replace(/9/g, 'q');
  return s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/ḏ/g, 'd').replace(/ḍ/g, 'd').replace(/ṯ/g, 't').replace(/ṭ/g, 't').replace(/ḥ/g, 'h').replace(/ɣ/g, 'g').replace(/ɛ/g, 'a').replace(/ř/g, 'r').replace(/ṛ/g, 'r').replace(/ẓ/g, 'z').replace(/ǧ/g, 'j').replace(/ṣ/g, 's').replace(/ǧ/g, 'g').replace(/ḇ/g, 'b').replace(/ḵ/g, 'k').replace(/ḷ/g, 'l');
}

function escapeHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// --------------------------------------------------------------
// Fetch-met-nette-foutmelding — dezelfde file://-detectie en boodschap-opzet als
// woordenlijst.html had, herbruikbaar voor elke CSV-gedreven pagina. `opts.onFileProtocol`
// en `opts.onOtherError` leveren de taal-specifieke HTML voor de twee foutgevallen.
// --------------------------------------------------------------
function fetchTarifitCSV(path, opts) {
  fetch(path, { cache: 'no-cache' }).then(resp => {
    if (!resp.ok) throw new Error('HTTP ' + resp.status);
    return resp.text();
  }).then(text => {
    opts.onSuccess(parseCSV(text));
  }).catch(err => {
    const onFile = location.protocol === 'file:';
    if (onFile) {
      opts.onFileProtocol();
    } else {
      opts.onOtherError(err);
    }
  });
}
