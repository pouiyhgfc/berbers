# Handoff — Tarifit-cursus website

> Voor de volgende agent. Lees dit eerst, dan [`review-uitleg.md`](review-uitleg.md) en [`woord-audit.md`](woord-audit.md), en dan kun je doorgaan vanaf Fase 5b (les 6–36 oefeningen).

## 1. Wat het project is

Een Nederlandse cursus-website voor het leren van Tarifit (Riffijns-Berber, Nador-dialect), gebaseerd op het academische boek **Mourigh & Kossmann (2019), *An Introduction to Tarifiyt Berber (Nador, Morocco)***. De gebruiker is een Nederlandstalige met familie-achtergrond uit het Rifgebied, geen taalkundige.

Project-pad: `c:\Users\Idrie\Downloads\tarifit-website_1`

### Bestanden

De projectstructuur is geordend per HTML-pagina:

```
/
  index.html
  boek.html
  cursus.html
  uitleg.html
  woordenlijst.html
  styles.css                # gedeeld door alle pagina's
  serve.ps1                 # lokale dev-server (moet aan de root)

  /assets/
    /boek/                  # gebruikt door boek.html
      tarifit-boek.pdf            (5 MB, zoekbaar)
      tarifit-boek-hires.pdf      (287 MB, hi-res scan)
      README.txt
    /cursus/                # gebruikt door cursus.html
      cursus.js                   (oefening-engine)
    /woordenlijst/          # gebruikt door woordenlijst.html
      woordenlijst.csv            (LEIDEND voor spelling, 1835 woorden)

  /_project/                # interne docs en tools — niet voor de site zelf
    _handoff.md             (dit bestand)
    _audit-script.py        (genereert woord-audit.md)
    _boek-tekst.txt         (OCR van het boek, 391 K chars)
    review-uitleg.md        (kritische review per hoofdstuk)
    woord-audit.md          (auto-gegenereerd uit script)
```

| Bestand / map | Wat het is | Status |
|---|---|---|
| `index.html` | Homepage | klaar |
| `boek.html` | PDF-viewer met 2 tabs (zoekbaar 5 MB / hi-res 287 MB) | Fase 1 klaar |
| `woordenlijst.html` | Woordenlijst die CSV dynamisch laadt | Fase 2 klaar |
| `uitleg.html` | Lange grammaticale uitleg, 20 secties | Fase 4 klaar |
| `cursus.html` | 36-lessen cursus met cross-links naar uitleg + link naar oefeningen per les | Fase 5a + 5b: oefeningen op `oefeningen.html` |
| `oefeningen.html` | Interactieve oefeningen les 01–36 (JSON + cursus.js) | Fase 5b klaar |
| `woord-inzenden.html` | Publiek formulier woordsuggesties (Supabase) | vereist `assets/js/supabase-config.js` |
| `woord-inzenden-admin.html` | Admin-overzicht (login + RLS) | zie `_project/supabase-setup.md` |
| `assets/cursus/cursus.js` | Vanilla-JS oefening-engine (mc / fill / translate / match) | Fase 5a klaar |
| `styles.css` | Stylesheet met `.box`, `.tar`, `.source`, `.exercise*` etc. | gedeeld |
| `assets/woordenlijst/woordenlijst.csv` | **Leidend voor spelling.** Format `Berbers,Nederlands` | bron |
| `assets/boek/tarifit-boek.pdf` | OCR-versie 5 MB | bron |
| `assets/boek/tarifit-boek-hires.pdf` | Hi-res scan 287 MB | bron |
| `_project/review-uitleg.md` | Volledige kritische review per hoofdstuk | naslag |
| `_project/woord-audit.md` | Auto-gegenereerde audit van uitleg.html tegen CSV | naslag |
| `_project/_boek-tekst.txt` | OCR-tekst van het boek, voor verificatie | naslag |
| `_project/_audit-script.py` | Genereert `woord-audit.md`. Werkt vanuit elke cwd. | tool |
| `_project/_apply-spelling-fixes.py` | Past `ǧ→ž`, `j→y/ž` (smart split) en `ɣar→ɣaa` toe op CSV + HTML's. | tool |
| `_project/supabase-setup.md` | SQL + RLS voor `word_submissions` | setup |
| `_project/_classify-overrides.csv` | Optionele handmatige CEFR/woordsoort per woord voor `_classify-words.py` | tool |

## 2. Belangrijke beslissingen van de gebruiker

Vastgelegd in eerdere conversatie, **moeten gerespecteerd worden**:

1. **CSV is leidend voor spelling**, niet het boek. Boek-OCR heeft fouten (vooral met `ɛ`, `ɣ`, `ḏ`, `ṯ`, `ḇ` die als `e`, `g`, `d`, `t`, `b` overkomen).
2. **Kwaliteit van de lesstof gaat boven AI-detector-tricks** — focus op correctheid en duidelijkheid van uitleg, niet op het verbergen dat het door AI is geschreven.
3. **Stijl-keuze** voor herschreven uitleg: `📖` blijft (voor pagina-referenties), alle andere emoji's eruit (`💡 ⚠️ ✅ 🚨 🅰️ 🅱️ 🅲️ 🇳🇱 🟢 ⭐ 🎯 🛑 🎓 📌 📚`).
4. **Diepte van review**: zelfde grondigheid voor alle hoofdstukken, geen oppervlakkige doorloop.
5. **Werkwijze**: stapsgewijs, één ding tegelijk, niet hallucineren of uitvinden. Bij twijfel checken in CSV of boek-tekst.

## 3. Wat er klaar is (Fase 1, 2, 3, 4, en 5a)

### Fase 1 — `boek.html` — klaar

Twee tabs:
- **Standaard (zoekbaar) — 5 MB**: laadt direct, gecomprimeerde OCR-versie
- **Hoge resolutie — 287 MB**: lazy-loaded via "Laad hoge-resolutie versie"-knop

### Fase 2 — `woordenlijst.html` — klaar (uitgebreid in Fase 6)

CSV wordt via `fetch('assets/woordenlijst/woordenlijst.csv')` geladen. Letter-rubrieken: A, B, C, D, E, F, G, H, Ḥ, I, K, L, M, N, O, P, Q, R, Ř, S, T, U, V, W, X, Y, Z, Ž, Ɛ, Ɣ. Diakrieten worden in zoek genegeerd. `/`-varianten worden beide doorzoekbaar. **Geen J of Ǧ-rubriek meer** sinds Fase 6: alle voormalige `j`-woorden zijn smart-gesplitst naar `y` (Berbers) of `ž` (Arabisch), en alle `ǧ` zijn `ž` geworden.

### Fase 3 — Volledige review in `review-uitleg.md`

Per hoofdstuk genummerde issues in vier categorieën: **[FOUT]**, **[ONDUIDELIJK]**, **[ONTBREEKT]**, **[SPELLING]**, **[STIJL]**. Aan het einde van het document staat een algemene observatie-sectie en de batch-aanpak voor Fase 4.

### Audit in `woord-audit.md`

Auto-gegenereerd Python-script dat alle Tarifit-tokens (`<em>...</em>`-tags) in `uitleg.html` cross-checkte met de CSV. Drie secties:
- **Sectie 1**: 64 notatie-mismatches met CSV-vorm ernaast
- **Sectie 2**: 161 tokens niet in CSV (mogelijk typo of dialectwoord)
- **Sectie 3**: 111 exacte matches

### Fase 4 — Volledige `uitleg.html` herschreven — klaar

Alle 20 secties (h1 t/m h20) zijn in de nieuwe stijl geschreven. Geverifieerd met audit-script:

- Geen verboden emoji's (alleen `📖` in `.source`-blokken).
- Geen "gecontroleerd"-claims.
- Geen decomposed Unicode (`t̲ b̲ d̲ k̲` met combining U+0331); overal precomposed (`ṯ ḇ ḏ ḵ`).
- Geen `dj`/`dz` waar `ǧ`/`ǧǧ` hoort (in `<span class="tar">`).
- Bekende spelfouten uit `review-uitleg.md` allemaal hersteld (incl. `seḇɛin` op regel 2010, `mařa`, `qama`, `tbedd`, `jjḏiḏ`, `ɛecṛa`, `aaḇɛa`, `aaḇɛin`, etc.).
- HTML-balans (open/close) voor `section`, `div`, `table`, `tbody`, `thead`, `p`, `ul`, `ol` allemaal in evenwicht.

### Fase 5a — Oefeningen voor les 1–5 — klaar

Vanilla-JS oefening-engine in `cursus.js` met vier vraagtypes:

| Type | Hoe het werkt |
|---|---|
| `mc` (multiple choice) | Klik één optie. Goede groen, foute rood, andere geneutraliseerd. |
| `fill` (invul) | Tekst-input + 'Controleer' + 'Toon antwoord'. Accepteert lijst alternatieven via `accept`. |
| `translate` (vertaling) | Idem `fill`, semantisch onderscheid voor toekomstige uitbreidingen. |
| `match` (paren koppelen) | Twee kolommen, klik links + klik rechts. Goede paren blijven groen, foute flitsen rood. Rechter-kolom shuffled. |

**Vraagdata** stond oorspronkelijk in `cursus.html`; deze staat nu op **`oefeningen.html`**: per les een `<div class="exercises" data-lesson="les-NN">` met JSON. Lessen 01–05: `_project/_oefeningen-blocks.txt`; lessen 06–36: `assets/cursus/exercises-les-06-36.json` (gegenereerd met `_project/_gen_exercises_06_36.py`, ingelezen door `_project/_build-oefeningen-html.py`).

**Antwoord-normalisatie** (`normalizeAnswer`) doet NFC + lowercase + trim + collapse whitespace + strip eind-leesteken, zodat `"Necc d Mimun."` matcht met `"necc d mimun"`.

**Geleverd** voor les 1–36 (mix mc / fill / translate / match); voortgang blijft in `localStorage` onder `tarifit-cursus-progress-v1`.

CSS-conventies: alle exercise-styling in `styles.css` onder de header `Exercises (oefeningen)`. Belangrijke specificity-fix: `.content .exercise-options` (twee classes) overschrijft `.content ul` voor list-style en padding. De CSS-link in `cursus.html` heeft cache-bust `?v=2`.

### Fase 6 — Spelling-uniformatie + woordenlijst-uitbreiding — klaar

Twee samenhangende verbeteringen op verzoek van de gebruiker.

**Deel 1 — Spellingcorrecties (orthografie)**

De gebruiker wenste consistente notatie:
- `ǧ` → `ž` overal (de zh-klank wordt voortaan eenduidig met `ž` geschreven)
- `j` → smart split: Arabische leenwoorden naar `ž`, Berberse woorden naar `y` (semi-klinker)
- `ɣar` → `ɣaa` (de preposition "naar / bij" eindigt op een lange klinker, niet op `r`)
- `ɣ`-beschrijving: niet langer "Franse r" maar **Arabische ﻍ ("gh"-klank)**, zoals in *Maghreb*

Uitvoering via `_project/_apply-spelling-fixes.py`:
- 30 woorden in CSV (incl. 2 `ǧ→ž`, 25 `j→y/ž`, 2 `ɣar→ɣaa`, plus de variant `jjib→žžib`)
- 35 vervangingen in `uitleg.html` (alleen binnen `<span class="tar">/<em class="tar">`-blokken)
- 27 vervangingen in `cursus.html` (idem)
- Bewust níet aangepast: `yaaḏen` (tarwe), `yiyyaa` (veld), `yemyaa` (groot), `mayaa` (waarom) — `yaa` is daar deel van het woord, niet de preposition
- `ɣ`-beschrijving op vier plekken bijgewerkt: `cursus.html` (les 01 tabel + JSON-vraag + explain), `uitleg.html` (h3 Klanken), `index.html`

`woordenlijst.html` letter-mapping aangepast: `J` en `Ǧ` zijn weg, `Ž` is nu een eigen rubriek na `Z`. Letter-click navigatie was nooit echt kapot maar werd verfijnd: `scroll-margin-top: 220px` en een **active-state** indicator (rode highlight) op de huidige letter via `IntersectionObserver`.

**Deel 2 — CEFR-niveau, woordsoort, Anki-export**

Drie nieuwe kolommen toegevoegd aan `woordenlijst.csv`:
- `niveau` — A1, A2, B1, B2, C1, C2 (CEFR-schaal)
- `woordsoort` — `ww`, `znw_m_ev`, `znw_m_mv`, `znw_v_ev`, `znw_v_mv`, `znw`, `vnw_pers`, `vnw_bez`, `vnw_aanw`, `vraagw`, `vz`, `voegw`, `telw`, `ontk`
- `anki_tag` — hierarchische Anki-tags: `tarifit::cefr::A1 tarifit::woordsoort::znw_m_ev`

Auto-classificatie via `_project/_classify-words.py`. Heuristieken (overschrijfbaar door handmatige edits in CSV):
- **Niveau**: handmatige A1-basislijst (~30 woorden) overschrijft alles → cursus.html-les bepaalt (les 1–3 = A1, les 4–7 = A2, les 8–12 = B1, les 13–20 = B2, les 21–28 = C1, les 29–36 = C2) → handmatige A2-basislijst → woord-eenvoud (≤4 letters = B1, 5–7 = B2, 8–10 = C1, ≥11 = C2). Boek-frequentie is niet bruikbaar omdat `_boek-tekst.txt` Engelstalige glossen heeft, geen pure Tarifit.
- **Woordsoort**: closed-class lijsten (vnw, vz, voegw, telw, vraagw, ontk, aanw_vnw) → NL-werkwoord-infinitief (`-en`) wint van Tarifitse `a-/i-` prefix → Tarifitse prefix-heuristiek (`ṯa-` v ev, `ṯi-` v mv, `a-` m ev, `i-` m mv, Arabisch `l-`/`ll-` met NL-artikel = m ev) → `znw` als NL-vertaling artikel heeft → default `ww`.
- Verdeling na uitvoering: A1 29, A2 16, B1 428, B2 1044, C1 242, C2 76. Werkwoorden 1052, znw (alle subtypes) 750, rest 33.

**UI-uitbreidingen in `woordenlijst.html`**:
- Filterknoppen `Niveau:` (Alle, A1–C2) — multi-select via combobox voor `Woordsoort:`
- Tags (klein, gekleurd per niveau) zichtbaar bij elke entry: groen voor A, oker voor B, roodbruin voor C
- "Exporteer voor Anki" knop genereert tab-gescheiden tekstbestand (`tarifit-anki-{filter}-{datum}.txt`) met Anki 2.1.55+ headers (`#separator:tab`, `#html:false`, `#tags column:3`); honoreert actieve filters
- Letter-nav wordt opnieuw opgebouwd na elk filterresultaat (alleen letters met matches blijven zichtbaar)

## 4. Stijl-template voor herschrijven

Belangrijk om consistent te houden over alle batches:

### Sectie-structuur per hoofdstuk

```html
<section id="hN">
<h1>Hoofdstuk X — Titel zonder emoji</h1>
<p class="source">📖 Boek p. X–Y</p>
<p class="lead">Eén of twee zinnen die zeggen wat de leerling hier leert.</p>

<h2>X.1 Subkop</h2>
<p class="source">📖 Boek p. X</p>
<p>Lopende uitleg in helder Nederlands...</p>

<!-- Tarifit-woord inline -->
<span class="tar">tmazixt</span>

<!-- Codes / partikels -->
<code>P</code>, <code>I</code>, <code>NP</code>

<!-- Tips -->
<div class="box tip">
  <div class="box-title">Truc om te onthouden</div>
  <p style="margin: 0;">...</p>
</div>

<!-- Waarschuwingen / dialect-issues -->
<div class="box warn">
  <div class="box-title">Belangrijk verschil met Nederlands</div>
  <p style="margin: 0;">...</p>
</div>

<hr />
</section>
```

### Schrijftoon

- Korte zinnen, één idee per alinea.
- Géén "Het is belangrijk om te beseffen dat...", "Kortom...", "In essentie...".
- Géén emoji's behalve `📖` aan het begin van een `<p class="source">`.
- Géén "✅ gecontroleerd" of "🎯 Wat leer je hier" — nooit.
- Tarifit-woorden in `<span class="tar">...</span>` met **CSV-conforme spelling**.
- Engelse termen mogen blijven (Aorist, Perfectief, Imperfectief, Free State, Annexed State) maar bij eerste gebruik kort uitgelegd in NL.
- Boek-pagina's expliciet vermelden — `📖 Boek p. X–Y` aan begin van hoofdstuk en bij belangrijke subhoofdstukken.

### Spelling-conventies (CSV-leidend)

| Goed | Fout (oude uitleg) | Reden |
|---|---|---|
| `ḏ ṯ ḇ ḵ` (precomposed) | `d̲ t̲ b̲ k̲` (combining) | CSV gebruikt precomposed; copy-paste matchen werkt anders niet |
| `ž` | `ǧ`, `dj`, `dz` | **Fase 6**: gebruiker prefereert `ž` voor zh-klank (Arabische ج) |
| `y` (Berbers) of `ž` (Arabisch leenwoord) | `j` (overal) | **Fase 6**: smart split — Berber `y` voor j-klank, `ž` voor zh-klank |
| `ɣaa` "naar / bij" | `ɣar`, `yaa` | **Fase 6**: gebruiker noteert lange a in plaats van r-klank |
| `ɛ ɣ ḥ ḍ ṛ ṣ ṭ ẓ ř ḷ` | varianten zonder diakriet | CSV-conventie |
| `aaḇɛa` (4) | `aabɛa` | systematisch ḇ + ɛ in telwoorden |
| `seḇɛa` (7) | `sebɛa` | idem |
| `ɛecṛa` (10) | `ɛecra` | mist ṛ |
| `aaḇɛin` (40) | `aabein` | mist ḇ + ɛ |
| `ɣ` = Arabische ﻍ ("gh") | "Franse r" | **Fase 6**: gebruiker noemt nadrukkelijk de Arabische gh-klank als referentie |
| `qama` (bed) | `gama` | echte fout — `q` ≠ `g` |
| `mařa` | `mara` | mist ř |
| `meɛlik` | `meelik` | mist ɛ |
| `jmeɛ` (verzamelen) | `cmeɛ` | typo: c ↔ j |
| `tbedd` (opstaan) | `t̲ḥedd` | typo: ḥ ↔ b |
| `iaḏen` | `iaden` | mist ḏ |
| `cuaḏu` | `suadu` | OCR-fout |
| `řbanku` | `rbanku` | mist ř |
| `ssaḇun` | `ssabun` | mist ḇ |

Bij twijfel: gebruik [`woord-audit.md`](woord-audit.md) als referentie.

## 5. Wat er nog moet gebeuren — uitvoeren in deze volgorde

### Fase 5c — Volledige `cursus.html` herschrijven (les 06–36)

**Doel:** Elke les heeft **dezelfde inhoudelijke dekking** als het bijbehorende
deel van `uitleg.html` (zie de bestaande `crosslinks` per les — die zijn de
ankerpunten), maar in de **zelfde eenvoudige schrijfstijl** als les 01–05.

**Referentielessen (goudstandaard):** `les-01` t/m `les-05`. Dat is géén kortere
samenvatting dan les 06+, maar wel: korte zinnen, concrete tabellen, expliciet
Nederlands-contrast waar het helpt, `box tip` / `box warn` alleen als het echt
iets oplost, en altijd `crosslinks` (uitleg + boek-pagina).

**Sjabloon per les (kopieer de structuur van les 01–05):**

1. `<div class="eyebrow">les NN · niveau X</div>`
2. `<h2>` — één heldere lesnaam (niet te academisch)
3. `<p class="lead">` — één à twee zinnen: wat kan de leerling **na** deze les?
4. **2–5× `<h3>`** — elk één idee; geen diepe geneste `<h4>`-bomen tenzij nodig
   (les 06 gebruikt nu `h4` onder `h3`; mag, maar houd het scanbaar)
5. **Tabellen** — voor paradigma's en woordenlijsten (zoals les 02)
6. **Korte `<ul>` / `<ol>`** — voor gebruikspatronen, niet voor lange theorie
7. **`<div class="box tip">`** — trucs, geheugensteuntjes
8. **`<div class="box warn">`** — contrast met Nederlands of veelgemaakte fout
9. **`<div class="crosslinks">`** — exact het relevante `uitleg.html#hN` + boek
10. **Oefeningen** — zie Fase 5b / aparte oefeningen-pagina (niet in de weg
    van de leestroom)
11. **`<div class="lesson-nav">`** — vorige / volgende les

**Werkwijze (batch per niveau of per 5 lessen):**

1. Open `uitleg.html` op het hoofdstuk dat bij deze les hoort (via bestaande
   crosslink).
2. Maak een **inventaris**: welke definities, tabellen en regels **moeten** in
   de cursus (MVP voor de leerling); verplaats detail en uitzonderingen naar
   uitleg (verwijs ernaar).
3. Herschrijf de les-body in cursus-taal: zelfde feiten, minder jargon; waar
   jargon onvermijdelijk is (Aorist, Annexed State): **één zin** uitleg + link
   naar uitleg.
4. Controleer alle `<span class="tar">` tegen `woordenlijst.csv`.
5. Lees hardop in je hoofd: past dit bij het tempo van les 03–04?

**Status:** Les 01–05 voldoen aan dit sjabloon. Les 06–36 zijn inhoudelijk vaak
al nuttig maar **niet** overal op hetzelfde didactische niveau uitgewerkt; dit
is de grootste openstaande inhoudstaak na UI/technische klussen.

### Fase 5b — Oefeningen voor les 6–36

De engine in `cursus.js` is af; alleen **vraagdata toevoegen** is nog werk. Werkwijze per les:

1. Open de les-sectie in `cursus.html` (zoek `<section id="les-NN">`).
2. Plak vlak voor de `<div class="lesson-nav">` aan het einde van de sectie:
    ```html
    <div class="exercises" data-lesson="les-NN">
      <script type="application/json">
    [ … vragen … ]
      </script>
    </div>
    ```
3. Schrijf 4–6 vragen die het **kernidee** van de les toetsen. Mix de types — leg het tafereel via het boek/CSV vast, niet uit het hoofd.
4. Lokaal testen: `python -m http.server 8080 --bind 127.0.0.1`, open `cursus.html#les-NN`, klik elke vraag minstens één keer goed en één keer fout om de feedback te zien.
5. Pas `?v=2` cache-bust aan in `cursus.html` als je nog meer CSS/JS-wijzigingen doet.

**JSON-formaat per vraagtype**:

```json
{ "type": "mc",
  "q": "Vraagtekst (mag HTML zoals <span class=\"tar\">…</span> bevatten)",
  "options": ["a", "b", "c", "d"],
  "correct": 1,
  "explain": "Korte uitleg na het antwoord (optioneel)" }

{ "type": "fill",
  "q": "Vul aan: <span class=\"tar\">x <span class=\"blank\">?</span> y</span>",
  "correct": "d",
  "accept": ["d", "ḏ"],
  "placeholder": "een letter",
  "explain": "…" }

{ "type": "translate",
  "q": "Vertaal: 'ik ben Mimoun'",
  "correct": "necc d Mimun",
  "accept": ["necc d Mimun", "necc d mimun"],
  "placeholder": "necc d …" }

{ "type": "match",
  "q": "Koppel elk woord aan zijn betekenis",
  "pairs": [
    { "left": "<span class=\"tar\">baba</span>", "leftIsTar": true, "right": "mijn vader" },
    …
  ] }
```

**Tips** voor goede vragen:
- Houd les 6 t/m les 10 (werkwoorden) gericht op vervoegings-patronen — vooral `mc` met "welke vorm hoort bij persoon X" en `fill` voor het invullen van een prefix/suffix.
- Voor les 11–15 (naamwoorden) werkt `match` (mannelijk ↔ vrouwelijk, enkelvoud ↔ meervoud) heel goed.
- Voor les 16–20 (zinnen) gebruik vooral `translate` om VSO-volgorde te oefenen.
- Voor les 21+ (geavanceerd) houd het kort — 3 à 4 vragen per les is genoeg.

### Fase 7 — Visuele verfijning (nog niet begonnen)

Subtiele animaties die niet afleiden:
- Fade-in bij scroll (Intersection Observer, 300ms ease-out, 8px translate)
- Reading progress bar (2px streep bovenaan, alleen op cursus/uitleg)
- Active-state glide in sidebar
- Soft hover-lift op cards (al deels aanwezig)
- Respecteer `@media (prefers-reduced-motion: reduce)`

**Niet doen**: parallax, draaiende elementen, knipperingen, pop-ups, frameworks, externe libraries.

### Fase 8 — Niveau- en woordsoort-correcties (laag-prioriteit)

De auto-classificatie in Fase 6 is een redelijke startschot, maar niet perfect:
- Veel werkwoorden die geen NL `-en` infinitief in vertaling hebben (bv. `Aardig`, `aap`, `0,5 dirham (munt)`) belanden onder `ww` terwijl het znw zijn.
- Sommige A1-woorden die niet in cursus 1–3 staan en niet in `BASIS_A1` vallen op B1 of B2.
- Lange Tarifit-woorden (≥11 letters) krijgen automatisch C2, ook als ze eigenlijk vrij eenvoudig zijn (bv. samenstellingen).

Manier om te corrigeren: edit handmatig de `niveau` of `woordsoort` kolom in `assets/woordenlijst/woordenlijst.csv`. **Het script `_classify-words.py` overschrijft alle waarden bij her-uitvoering** — dus alleen draaien als er nieuwe lessen of nieuwe woorden zijn toegevoegd, of als je de heuristiek hebt aangepast en alle handmatige correcties opnieuw wilt verliezen. Voor incrementele edits volstaat een directe CSV-aanpassing.

Een betere lange-termijn aanpak zou zijn: een aparte `woordenlijst-overrides.csv` waar handmatige correcties in staan, die `_classify-words.py` met voorrang inleest. Niet nu nodig.

## 6. Tips voor de volgende agent

### Tools die werken

- **`SemanticSearch`** voor het verkennen van de codebase als je iets niet weet — werkt goed.
- **`Grep`** voor exacte string-matches in CSV / uitleg / boek-tekst.
- **`browser_navigate` + `browser_take_screenshot`** voor visuele checks. Lokale server moet draaien (`python -m http.server 8080 --bind 127.0.0.1` of `serve.ps1`).
- **PyMuPDF** is geïnstalleerd voor PDF-tekstextractie als je opnieuw boek-tekst nodig hebt: `import fitz; doc = fitz.open('assets/boek/tarifit-boek.pdf'); doc[0].get_text()`.

### Valkuilen

- **Powershell `python -c @"..."@`** met `print()` valt vaak om door cp1252-encoding bij speciale Tarifit-tekens. Schrijf liever naar een tijdelijk bestand met UTF-8 en lees dat dan.
- **Decomposed vs precomposed Unicode**: `t̲` (t + U+0331) is byte-wise verschillend van `ṯ` (U+1E6F). De CSV gebruikt **precomposed**. Bij string-matching moet je hier op letten.
- **Voorbeelden niet verzinnen**. Als een voorbeeld niet in CSV of boek staat (`woord-audit.md` Sectie 2 bevat de twijfelgevallen), markeer het met een `[ONBEVESTIGD]`-comment of vervang door een verifieerbare. Liever weglaten dan iets verkeerds opschrijven.
- **Drie inconsistenties uit oude uitleg die je moet vermijden**:
  1. `dj`/`ǧ` voor de "j van joke" — gebruik `ž` (Fase 6 conventie, CSV-conform).
  2. `dz`/`ǧǧ` voor de geminate — gebruik `žž`.
  3. `xad` als "sterker dan ad" — beschrijf het als modale variant (waarschuwing/dreiging), niet als temporele gradatie.

### Werkwijze stapsgewijs (door gebruiker gevraagd)

1. **Eén batch tegelijk**. Niet vooruitlopen.
2. Bij elke batch: lees relevant deel van `review-uitleg.md`, lees relevant boek-pagina's uit `_boek-tekst.txt` als je context nodig hebt.
3. Schrijf nieuwe sectie-content, maak Python-replacement-script, run, lint, visueel testen.
4. Cleanup werkbestanden.
5. Korte samenvatting van wat in deze batch is veranderd.
6. Vraag "ga door" voordat je de volgende batch begint.

## 7. Server starten

```powershell
# Vanaf project-root
.\serve.ps1
# of
python -m http.server 8080 --bind 127.0.0.1
```

Open dan http://127.0.0.1:8080/uitleg.html (of `cursus.html`, `woordenlijst.html`, `boek.html`).

## 8. Status-overzicht

| Fase | Status |
|---|---|
| Fase 0 (gebruiker plaatst PDFs en CSV) | klaar |
| Fase 1 (boek.html met 2 PDF-tabs) | klaar |
| Fase 2 (woordenlijst.html dynamisch) | klaar |
| Fase 3 (review-uitleg.md + woord-audit.md) | klaar |
| Fase 4 (volledige `uitleg.html` herschreven, h1–h20) | klaar |
| Fase 5a (oefening-engine + les 1–5 vragen) | klaar |
| Fase 5b (oefenvragen voor les 6–36) | volgende |
| Fase 6 (visuele verfijning) | wachtrij |

**Volgende concrete actie**: Fase 5b — oefeningen toevoegen aan `<section id="les-06">` t/m `<section id="les-36">` in `cursus.html`. De engine staat al klaar in `cursus.js`; alleen JSON-vraagdata schrijven en in een `<div class="exercises" data-lesson="les-NN">` plakken vóór de `<div class="lesson-nav">`.
