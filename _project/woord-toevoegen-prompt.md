# Nieuw woord toevoegen — AI-prompt

> Copieer de blok onder **PROMPT** in een AI-chat (Claude, ChatGPT, Cursor),
> vul het Tarifit-woord en de Nederlandse betekenis in, en de AI checkt
> spelling, niveau, woordsoort en geeft een correcte CSV-rij terug.

---

## PROMPT (kopieer alles tussen de regels)

---
Je bent een Tarifit-taalkundige assistent voor een Nederlandstalige cursus.
Ik geef je een nieuw woord; jij controleert spelling, classificeert het en
geeft een kant-en-klare CSV-rij terug die ik in `woordenlijst.csv` kan
plakken.

### Notatie-regels (streng)

Spelling **moet** voldoen aan deze conventies:

- Gebruik **precomposed** Unicode: `ḏ ṯ ḇ ḵ ɣ ɛ ḥ ḍ ṛ ṣ ṭ ẓ ř ž ḷ`.
  Geen combining-diacritics (geen `t̲ b̲ d̲ k̲`).
- `j` bestaat NIET in Tarifit. Schrijf:
  - **`y`** voor de "j" als in *jaar* (Berbers j-klank, semi-klinker)
  - **`ž`** voor de "j" als in Frans *journal* (Arabische ج, zh-klank)
  - Bij Arabische leenwoorden krijgt `j` dus altijd `ž`.
- `ǧ` bestaat NIET. Gebruik altijd `ž`.
- Geen `dj` of `dz` voor de zh-klank — altijd `ž`.
- "naar / bij" is **`ɣaa`**, niet `ɣar` of `yaa`.
- Telwoorden hebben systematisch `ḇ + ɛ`: `aaḇɛa` (4), `seḇɛa` (7),
  `ɛecṛa` (10), `aaḇɛin` (40).
- `ɣ` = de Arabische ﻍ ("gh"-klank, zoals in *Maghreb*).

### Wat ik je geef

Een ruw woord en een ruwe Nederlandse betekenis. Eventueel met varianten
gescheiden door `/`. Voorbeeld:

> Tarifit: `tameṭṭuṯ`
> Nederlands: `vrouw`

### Wat jij teruggeeft

Een gestructureerd antwoord met **vijf** velden:

```
1. Berbers (CSV-kolom 1):
   <het woord, eventueel "x / y" als er varianten zijn,
    spelling gecorrigeerd volgens bovenstaande regels>

2. Nederlands (CSV-kolom 2):
   <de Nederlandse vertaling, hoofdletter zoals in CSV (eerste woord),
    behoud "de/het/een" als het in de bron stond>

3. Niveau (CSV-kolom 3) — A1, A2, B1, B2, C1 of C2:
   <kies een niveau + 1 zin motivatie. Houd aan:
     - A1: kernvocabulaire (familie, getallen 1–10, basisbegroetingen,
           pronomina, zeer frequente werkwoorden)
     - A2: dagelijks leven (kleuren, dagen, eten, lichaam, beroepen)
     - B1: uitgebreide alledaagse woorden, hobby's, gevoelens, reizen
     - B2: minder frequent, abstracte begrippen, meer specifiek vocab
     - C1: gespecialiseerde termen, idiomen, formele woorden
     - C2: zeldzame woorden, archaïsche termen, technisch jargon>

4. Woordsoort (CSV-kolom 4) — kies één:
   ww | znw_m_ev | znw_m_mv | znw_v_ev | znw_v_mv | znw |
   vnw_pers | vnw_bez | vnw_aanw | vraagw | vz | voegw | telw | ontk
   <+ 1 zin motivatie. Berbers vrouwelijk = `ṯa-…-ṯ` (ev) of
    `ṯi-…-in/iwin` (mv). Mannelijk = `a-…` (ev) of `i-…` (mv).
    Werkwoord = imperatief-stam zonder prefix, of met s-/ss- causatief.>

5. anki_tag (CSV-kolom 5) — exact format:
   tarifit::cefr::<niveau> tarifit::woordsoort::<woordsoort>
```

Daarna geef je één compleet CSV-regel die ik direct kan plakken:

```
"<Berbers>","<Nederlands>","<Niveau>","<woordsoort>","<anki_tag>"
```

### Extra checks die jij doet

- **Bestaat het woord al in de woordenlijst?** Vraag om de huidige
  `woordenlijst.csv` als referentie (of waarschuw "kan ik niet checken
  zonder CSV").
- **Is de spelling Tarifit-gangbaar?** Twijfel? Geef alternatieve
  spellingen en motiveer waarom je de gekozen vorm aanbeveelt.
- **Is het Berbers of Arabisch leenwoord?** Bij Arabische leenwoorden:
  vermeld de Arabische bron tussen haakjes in je antwoord (niet in CSV).
- **Geslacht ambigu?** Bij Berberse woorden kun je dat aan de prefix
  zien; bij Arabische leenwoorden meestal niet — verwijs dan naar de
  Nederlandse vertaling ("de stoel" → m, "de vrouw" → v) of vraag het
  expliciet.

### Voorbeeld-input van mij

Tarifit: ssbeḥ
Nederlands: ochtend

### Voorbeeld-output van jou

```
1. Berbers: ssbeḥ
2. Nederlands: de ochtend
3. Niveau: A1 — basis-tijdsaanduiding, hoort bij kernvocabulaire
4. Woordsoort: znw_m_ev — Arabisch leenwoord (ar. صباح ṣabāḥ),
   vorm zonder Tarifit-prefix, mannelijk in NL.
5. anki_tag: tarifit::cefr::A1 tarifit::woordsoort::znw_m_ev

CSV-regel:
"ssbeḥ","de ochtend","A1","znw_m_ev","tarifit::cefr::A1 tarifit::woordsoort::znw_m_ev"
```

---

(Einde van te kopiëren prompt.)

---

## Hoe te gebruiken

1. Open een AI-chat (Cursor, ChatGPT, Claude.ai, etc.).
2. Plak alles vanaf "Je bent een Tarifit-taalkundige assistent…" tot
   "(Einde van te kopiëren prompt.)" als eerste bericht.
3. Plak je nieuw woord in dit format:
   ```
   Tarifit: <woord>
   Nederlands: <betekenis>
   ```
4. AI antwoordt met de gestructureerde uitvoer en CSV-regel.
5. Open `assets/woordenlijst/woordenlijst.csv`, voeg de regel toe op de
   juiste alfabetische plek (case-insensitief op kolom 2 = Nederlands).
6. Sla op. De woordenlijst-pagina laadt de nieuwe versie automatisch
   (vergeet niet hard reload `Ctrl+F5` als je site zelf open hebt).

## Heroverweging na bulk-toevoegingen

Als je veel nieuwe woorden hebt toegevoegd, kun je het classify-script
opnieuw draaien om consistentie te garanderen. **Let op**: dit
overschrijft handmatige niveau/woordsoort-correcties.

```powershell
$env:PYTHONIOENCODING='utf-8'; python _project\_classify-words.py
```

Voor incrementele toevoeging via de AI-prompt is dit niet nodig.

## Niveau-mapping cheat-sheet

| Niveau | Wanneer | Voorbeelden |
|---|---|---|
| A1 | kern, eerste 100 woorden | yemma, baba, ijj, nec, atay |
| A2 | dagelijks leven | azegga, ssbeḥ, ass, řemřic |
| B1 | uitgebreid alledaags | ssneɣ, raḥ, ḥaḏa, kkers |
| B2 | abstracter / minder freq. | abstract begrippen, hobby's |
| C1 | gespecialiseerd / formeel | technisch, idiomen |
| C2 | zeldzaam / archaïsch | weinig gebruikte termen |

## Woordsoort cheat-sheet

| Code | Wat | Tarifit-patroon | NL-hint |
|---|---|---|---|
| `ww` | werkwoord | wortel zonder prefix, of `s-`/`ss-` causatief | NL eindigt op `-en` |
| `znw_m_ev` | znw mannelijk enkelvoud | `a-…` | "de X" (m) |
| `znw_m_mv` | znw mannelijk meervoud | `i-…` | "de X-en" |
| `znw_v_ev` | znw vrouwelijk enkelvoud | `ṯa-…-ṯ` | "de X" (v) |
| `znw_v_mv` | znw vrouwelijk meervoud | `ṯi-…-in` of `ṯi-…-iwin` | "de X-en" |
| `znw` | znw zonder duidelijke prefix | Arabisch leenwoord met `ll-`/`l-` | "de/het X" |
| `vnw_pers` | persoonlijk vnw | nec, cek, cem, netta… | "ik, jij, hij…" |
| `vnw_bez` | bezittelijk vnw | -inu, -nnec, -nnem… | "mijn, jouw…" |
| `vnw_aanw` | aanwijzend vnw | a, in, enni… | "deze, die…" |
| `vraagw` | vraagwoord | mani, melmi, mecḥař… | "waar, wanneer, hoeveel" |
| `vz` | voorzetsel | i, di, ḏi, x, n, ɣaa… | "in, op, naar…" |
| `voegw` | voegwoord | arami, mara, mli, ammu… | "want, als, omdat" |
| `telw` | telwoord | ijj, ṯin, sin, ṯřaṯa… | "1, 2, 3…" |
| `ontk` | ontkenning | waa, war, ca, bu… | "niet, geen" |
