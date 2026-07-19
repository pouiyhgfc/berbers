# PLAN — Zinnenbank integreren in de website

**Doel.** De ~1100 geattesteerde zinnen uit `assets/zinnen/zinnen.csv` zichtbaar en bruikbaar maken
op de site: (1) een doorzoekbare zinnen-pagina NL+EN, (2) een dialoogweergave die de
boekdialogen reconstrueert, (3) geattesteerde voorbeeldzinnen per les in `cursus.html`.

**Vereist:** `PLAN-AI-DOCENTPROMPT-EN-ZINNENBANK.md` is volledig uitgevoerd én gecommit:
`zinnen.csv` bevat de gemigreerde zinnen (tags `id:pNNN-MM;context:…`, `bron` = `boek p. N`),
de NL-batch (stap 1.8) is gedraaid, `make check` is groen.
**Plaats dit bestand in:** `plan/PLAN-ZINNEN-WEBSITE.md`
**Werkwijze:** ongewijzigd — bron bewerken, `make build`, `make check`, dan pas committen.
**Branch:** `git checkout -b zinnen-website`. Elke fase = één commit.

---

## 0. Architectuurbesluit (lees eerst — dit stuurt alles)

De site heeft al een bewezen patroon voor precies dit probleem: **`woordenlijst.html` laadt zijn
CSV client-side** met `fetch('/assets/woordenlijst/woordenlijst.csv')` en rendert in de browser.
Voordeel: de CSV blijft de enige bron, een nieuwe zin is CSV pushen zonder HTML-wijziging, en er
is geen generator die HTML produceert die vervolgens hand-bewerkt wordt (= drift).

**Dit plan volgt dat patroon overal.** Dus:

- `zinnen.html` (NL+EN) → runtime fetch van `assets/zinnen/zinnen.csv`, zoals woordenlijst.
- Voorbeeldzinnen in lessen → een klein runtime-script dat per les-sectie zinnen injecteert.
  **Niet** statisch in `cursus.html` bakken: dat bestand is hand-geschreven canoniek, en
  gegenereerde blokken in canonieke bestanden is precies het soort vermenging dat
  `WIJZIGINGEN.md` verbiedt.
- Geen nieuwe generator naar HTML. De enige buildwijzigingen zijn checks.

Schaal is bewezen: woordenlijst rendert 1785 rijen client-side zonder problemen; 1100 zinnen is
kleiner.

**Hergebruik verplicht:** in `nl/woordenlijst.html` (regel ±403) staat een functie `normalize()`
die zoektermen én woorden platslaat naar een vergelijkbare vorm (NFD-strip + ḏ→d, ṯ→t, ḥ→h, ɣ→g,
ɛ→a, ř→r, ǧ→j, …). Die raakt de data **niet** aan — hij bestaat alleen zodat iemand die `7ar`,
`ghar` of `taddart` typt tóch `ḥar`/`ɣar`/`ṯaddarṯ` vindt. Deze functie wordt niet opnieuw
uitgevonden maar verplaatst naar `assets/js/tarifit-search.js`, gedeeld door woordenlijst en
zinnen (stap 1.1). Diezelfde platslag-tabel is bovendien de motor van de spellingdetector in
fase S: twee spellingen van hetzelfde woord slaan plat naar dezelfde vorm, en dát is hoe we
kandidaten vinden.

---

## 1. Scope

**Wel**
- **Fase S: spellingharmonisatie** — de zinnen komen uit het boek (OCR) en volgen niet overal de
  learntarifit-schrijfwijze van de woordenlijst; een detector + review + gecontroleerde toepassing
  trekt dat gelijk. Dit is de enige plek in dit plan die de `tarifit`-kolom mag wijzigen.
- `assets/js/tarifit-search.js` — gedeelde normalisatie + CSV-parser (uit woordenlijst gelicht).
- `nl/zinnen.html` + `en/zinnen.html` — doorzoekbare zinnenpagina met filters.
- Dialoogweergave binnen diezelfde pagina (tab/filter, geen aparte pagina).
- `hoofdstuk`/`les`-verrijking van de CSV via AI-classificatie mét `auto`-markering (fase 3.1).
- "Uit het boek"-blokken per les in `cursus.html` via runtime-injectie (fase 3.2).
- Navigatie, `check_links`, `check_parity`-uitbreiding, `CLAUDE.md`/`WIJZIGINGEN.md`.

**Niet** (bewust)
- De AI-tutor of `_ai/` — dat traject is af; dit plan raakt `_ai/` niet.
- Audio, TTS, spraak.
- Een oefengenerator op de site uit de zinnen (mooi vervolg, apart plan).
- `woordsoort`/`cefr`-opschoning van de woordenlijst.

---

## 2. Sessie-setup voor Claude Code

- `/model sonnet` volstaat.
- Lees: `CLAUDE.md`, dit plan, en **`nl/woordenlijst.html` volledig** — dat is de stijl- en
  patroonreferentie (fetch, foutafhandeling bij `file://`, tabelrendering, zoek-UX).
- Lees `nl/cursus.html` **niet** volledig in (180 KB); gebruik `grep` voor de les-ankers
  (`id="les-NN"`).
- CSV-kolommen: `tarifit,nl,en,gloss,hoofdstuk,les,bron,tags`. De `tarifit`-kolom is heilig:
  alleen het apply-script van fase S (stap S.3) mag erin schrijven, en uitsluitend goedgekeurde
  vervangingen. Elk ander script behandelt de kolom als read-only.
- NL/EN-pariteit is een bestaande eis: elke nieuwe pagina bestaat in beide talen, Tarifit-inhoud
  identiek, chrome (labels/uitleg) vertaald.

---

## Fase S — Spellingharmonisatie (eerst draaien, vóór fase 1)

De woordenlijst volgt de learntarifit-schrijfwijze; de zinnen komen uit de OCR van het boek en
wijken daar deels van af (diacritica kwijt of anders: `t`↔`ṯ`, `d`↔`ḏ`, `h`↔`ḥ`, `r`↔`ř`,
`s`↔`ṣ`, `z`↔`ẓ`, `g`↔`ɣ`, `j`↔`ǧ`, e/schwa-verschillen). Doel: dezelfde schrijfwijze overal —
zonder één foute verandering.

**Kernprincipe: detecteren is machinaal, beslissen is menselijk, toepassen is mechanisch.**
Geen script "verbetert" ooit zelfstandig een Tarifit-woord. De attestatie blijft intact: het
`id:`-tag + `bron` wijzen altijd terug naar de boekpagina, dus een geharmoniseerde zin blijft
verifieerbaar.

### Stap S.1 — Detector: `_project/scripts/check_spelling_zinnen.py`

Werkwijze:
1. Laad `woordenlijst.csv` → twee indexen: (a) set van exacte spellingen, (b) map
   `platgeslagen vorm → {canonieke spelling(en)}`. De platslag-functie is **exact dezelfde tabel**
   als `normalize()` in woordenlijst.html/tarifit-search.js — één keer in Python overgezet, met
   de JS-regel als bron in de docstring.
2. Tokeniseer elke zin uit `zinnen.csv`: splits op witruimte én op clitic-koppeltekens
   (`iaɛjeb-ayi` → `iaɛjeb`, `ayi`), strip leestekens.
3. Classificeer elk token:
   - **OK** — exacte match met de woordenlijst.
   - **KANDIDAAT** — geen exacte match, maar de platgeslagen vorm matcht wél een
     woordenlijstwoord met andere spelling. Dít zijn de vermoedelijke spellingafwijkingen.
   - **ONBEKEND** — geen match, ook niet platgeslagen. Meestal een vervoegde/verbogen vorm of een
     woord dat (nog) niet in de lijst staat. **Geen fout** — alleen tellen en apart rapporteren.
4. Schrijf `_project/rapporten/spelling-kandidaten.csv`, geaggregeerd per uniek paar
   (token → voorstel), gesorteerd op frequentie:

   | kolom | inhoud |
   |---|---|
   | `token` | spelling zoals in de zinnen |
   | `voorstel` | canonieke spelling uit de woordenlijst |
   | `betekenis_woordenlijst` | nl/en van dat woordenlijstwoord |
   | `aantal` | in hoeveel zinnen |
   | `voorbeeld_ids` | max 3 zin-id's |
   | `voorbeeld_en` | EN-vertaling van één voorbeeldzin |
   | `status` | leeg — vult Idries: `ja` / `nee` |

   De kolommen `betekenis_woordenlijst` en `voorbeeld_en` staan er niet voor de sier: ze zijn de
   controle op het echte gevaar (zie S.2).

Veiligheidsranden in de detector:
- tokens < 3 tekens worden nooit KANDIDAAT (te veel toevalstreffers) — apart lijstje;
- een platgeslagen vorm die op **meerdere** woordenlijstwoorden matcht → aparte sectie
  "ambigu", nooit een enkelvoudig voorstel;
- het script leest alleen; het schrijft nooit naar `zinnen.csv`.

### Stap S.2 — Review (doet Idries, patroonsgewijs)

Open het rapport en vul `status` per rij. Omdat het geaggregeerd is beslis je per *patroon*
("`taddart` → `ṯaddarṯ`, 41×: ja") en niet 1100 keer per zin. Vuistregels:

- **Betekenis moet kloppen.** Dit is het echte risico: emfatische medeklinkers zijn
  betekenis-onderscheidend — `ẓ`/`z`, `ṣ`/`s`, `ṭ`/`t` kunnen twee verschillende woorden zijn die
  alleen platgeslagen samenvallen. Vergelijk daarom altijd `betekenis_woordenlijst` met
  `voorbeeld_en`. Past het niet → `nee`.
- Twijfel = `nee`. Een niet-geharmoniseerd woord is een cosmetisch probleem; een verkeerde
  "correctie" is datacorruptie.
- De sectie "ambigu" beslis je per geval of laat je staan.

### Stap S.3 — Toepassen: `_project/scripts/apply_spelling_zinnen.py`

- Leest het rapport, gebruikt **uitsluitend** rijen met `status=ja`.
- Vervangt hele tokens (op woordgrenzen incl. koppeltekens), alleen in de `tarifit`-kolom.
- Draait eerst als dry-run: toont per vervanging 3 voor/na-voorbeelden; pas met `--apply` schrijft
  hij.
- Harde garanties, geverifieerd na afloop: alle andere kolommen byte-identiek; het aantal
  gewijzigde rijen wordt gemeld; elke wijziging herleidbaar tot een `ja`-rij.
- Daarna `make build && make check` — de `_ai/zinnen.md` volgt automatisch, en de AI-docent gaat
  er direct op vooruit: [L]-lookups tussen woordenlijst en zinnen matchen nu wél.
- Rapport + beslissingen committen (het rapport is de audit-trail), regel in `WIJZIGINGEN.md`.

### Stap S.4 — Restlijst is oogst

De ONBEKEND-lijst uit S.1 is geen afval: hoogfrequente onbekende tokens zijn óf verbogen vormen
(prima) óf woorden die je woordenlijst mist. Bewaar als
`_project/rapporten/onbekende-tokens.csv` (token, aantal, voorbeeld-ids) — dat is je werklijst
voor woordenlijst-uitbreiding, apart traject.

### Acceptatie fase S

Detector + rapport gedraaid · review gedaan · apply met dry-run-log · `make check` groen ·
0 wijzigingen buiten de `tarifit`-kolom. Commit: `fix(zinnen): spelling geharmoniseerd met
woordenlijst (review-gestuurd)`.

---

## Fase 1 — Doorzoekbare zinnenpagina

### Stap 1.1 — `assets/js/tarifit-search.js`

Licht uit `nl/woordenlijst.html`: `normalize()` (inclusief de internet-spellingsvarianten),
de CSV-parser en de fetch-met-nette-foutmelding (het `file://`-blok met de lokale-serverinstructie
bestaat daar al — hergebruik die tekst). Exporteer als gewone globals (site gebruikt geen modules).
Pas **beide** woordenlijst-pagina's aan zodat ze dit bestand laden en hun eigen kopie verwijderen.

> Acceptatie: woordenlijst werkt exact als voorheen (zoek op `7`, `gh`, `3`, accent-loos), maar de
> functies staan nog maar op één plek. Aparte commit vóór de rest van fase 1.

### Stap 1.2 — `nl/zinnen.html` + `en/zinnen.html`

Zelfde paginaskelet als `woordenlijst.html` (header, topnav, styles.css, lang-switch die naar
`../en/zinnen.html` resp. `../nl/zinnen.html` wijst).

**UI, van boven naar beneden:**
1. Zoekveld — zoekt genormaliseerd in `tarifit` én in de vertaalkolom van de paginataal.
2. Filterrij:
   - **Context** (chips, afgeleid uit `tags` → `context:…`): Alles · Dialoog · Woordenlijst · …
     (waarden dynamisch uit de data halen, niet hardcoden — de contextverdeling is pas na de
     migratie bekend).
   - **Hoofdstuk** (select, §-nummers uit kolom `hoofdstuk`; verbergen zolang de kolom leeg is —
     `if (rows.some(r => r.hoofdstuk))`).
   - **Pagina** (nummerveld, filtert op `bron`).
3. Resultaatteller ("312 van 1100 zinnen").
4. De lijst. Per zin een rij:
   - Tarifit prominent (zelfde klasse als het tarifit-vet in woordenlijst),
   - vertaling in paginataal eronder; **NL-pagina met lege `nl`-cel → toon `en` cursief met
     label "(EN)"** — nooit een lege regel, en het maakt meteen zichtbaar wat stap 1.8 van het
     vorige plan eventueel gemist heeft,
   - metadata klein: `boek p. 205` · §4.1 (indien gevuld) · context-chip,
   - kopieerknop voor de Tarifit-zin (klembord, met "gekopieerd"-flits).
5. Onderaan dezelfde data-uitleg als woordenlijst: "Data: `assets/zinnen/zinnen.csv` — nieuwe
   rijen alleen in de CSV, deze pagina laadt automatisch."

**Rendering:** 1100 rijen mag in één keer gerenderd worden (woordenlijst doet 1785), maar bouw de
rijen met één `innerHTML`-join, niet 1100 losse appends.

**Sortering standaard:** op `bron`-paginanummer oplopend, daarbinnen op `id:`-tag (die codeert de
volgorde op de pagina: `p052-01`, `p052-02`, …). Dat is de boekvolgorde — de natuurlijkste.

### Stap 1.3 — Navigatie en links

- Voeg `<a href="zinnen.html">Zinnen</a>` toe aan de topnav van **alle** NL- én EN-pagina's,
  tussen Woordenlijst en "Woord voorstellen". Gebruik `grep -l 'class="topnav"'` om geen pagina
  te missen; de EN-teksten volgen de bestaande EN-nav-labels.
- Draai `python _project/scripts/check_links.py` en los alles op wat hij meldt.

### Acceptatie fase 1

- Beide pagina's tonen alle zinnen; zoeken op `iaɛjeb`, `ia3jeb` en `pleased` vindt dezelfde rij.
- Filters combineren (context + pagina) werkt; teller klopt.
- Lang-switch schakelt naar dezelfde pagina in de andere taal.
- `make check` groen (dit raakt `_ai/` niet, dus dat moet triviaal zijn).
- Commit: `feat(site): doorzoekbare zinnenpagina NL+EN uit zinnen.csv`.

---

## Fase 2 — Dialoogweergave

De boekdialogen zijn reconstrueerbaar: zinnen met `context:dialogue` (of vergelijkbaar — check de
werkelijke tag-waarden na migratie) die dezelfde `bron`-pagina delen, gesorteerd op `id`, vormen
samen de dialoog van die pagina.

### Stap 2.1 — Weergavetoggle op `zinnen.html`

Bovenaan de lijst een toggle **Lijst | Dialogen**. In dialoogstand:

- Alleen zinnen met dialoog-context; gegroepeerd per `bron`-pagina als kaart
  "Dialoog · boek p. 52", zinnen in `id`-volgorde.
- Per regel: Tarifit + vertaling eronder in kleiner grijs (geen tabel — opmaak als
  gespreksregels, om en om licht ingesprongen zoals een chat, puur met CSS-klassen `dlg-a`/`dlg-b`
  op even/oneven regels).
- **Eerlijkheidsgrens:** de CSV weet niet wíé wat zegt. Even/oneven is een aanname voor de
  leesbaarheid. Zet één regel uitleg onder de toggle: "Sprekerwisseling is een weergave-aanname;
  het boek is leidend." Geen sprekersnamen verzinnen.
- Zoekveld blijft werken (filtert hele dialogen: een dialoog matcht als één regel matcht).

### Acceptatie fase 2

Toggle werkt in beide talen; dialogen staan in boekvolgorde; `make check` groen.
Commit: `feat(site): dialoogweergave op zinnenpagina`.

---

## Fase 3 — Zinnen in de lessen

Dit is de waardevolste en de gevoeligste fase: hij vereist dat de `les`-kolom gevuld wordt, en
dat gebeurt deels machinaal.

### Stap 3.1 — Verrijking: `les`- en `hoofdstuk`-kolom vullen (AI-classificatie, bewaakt)

Dit is **metadata toekennen, geen Tarifit produceren** — daarom mag het. Maar het blijft
machinale interpretatie, dus het wordt gemarkeerd en steekproefsgewijs gecontroleerd.

Werkwijze voor de agent:

1. Bouw eerst een **onderwerpenindex**: per les uit `nl/cursus.html` de `id`, titel en
   eyebrow-tekst (via grep, niet het hele bestand inlezen); per § uit `_ai/grammatica.md` de kop.
2. Classificeer per zin (batches van ±100): welke les(sen) en welke §('s) passen bij deze zin,
   op basis van de woorden in de zin + de vertaling. **Twijfel = leeg laten.** Liever 600 goed
   geclassificeerde zinnen dan 1100 gokjes.
3. Schrijf naar de CSV: `les` en/of `hoofdstuk` invullen én aan `tags` toevoegen:
   `les:auto;hoofdstuk:auto`. Handmatig gezette waarden (zonder `auto`-tag) worden **nooit**
   overschreven.
4. Diff-controle na elke batch: alleen de kolommen `les`, `hoofdstuk`, `tags` mogen wijzigen —
   `tarifit`, `nl`, `en`, `gloss`, `bron` byte-identiek.
5. Rapporteer per batch: aantal geclassificeerd / leeg gelaten, en de 10 laagste-zekerheid-gevallen
   voor Idries' steekproef.
6. `make build && make check` — de `_ai/zinnen.md`-groepering wordt hier direct beter van
   (zinnen verhuizen van "Zonder hoofdstuk" naar hun §), dus de AI-tutor profiteert gratis mee.

### Stap 3.2 — "Uit het boek"-blok per les (runtime-injectie)

Nieuw bestand `assets/js/les-zinnen.js`, geladen onderaan `nl/cursus.html` en `en/cursus.html`
(één `<script>`-regel per bestand — dat is de enige handmatige wijziging aan cursus.html):

- Fetcht `zinnen.csv` één keer, bouwt een index `les → zinnen`.
- Voor elke `section[id^="les-"]` met ≥1 bijbehorende zin: injecteer aan het eind van de sectie
  een blok:

  ```
  Uit het boek
  ─ iaɛjeb-ayi rḥar — ik ben blij (boek p. 205)
  ─ …                                    [max 5; knop "meer" toont de rest op zinnen.html,
                                          gefilterd op die les via ?les=NN]
  ```

- Kop NL "Uit het boek" / EN "From the book". Vertaling in paginataal, zelfde EN-fallback-regel
  als stap 1.2.
- Lessen zonder zinnen krijgen **niets** — geen leeg blok, geen "nog geen zinnen".
- `zinnen.html` leest de `?les=NN`-queryparameter en zet het filter alvast.
- Faalgedrag: als de fetch mislukt, verschijnt er gewoon niets. De cursus mag nooit breken op
  de zinnenbank.

### Acceptatie fase 3

- Steekproef van 20 auto-classificaties door Idries: ≥18 goed, anders criteria aanscherpen en
  batch opnieuw.
- Les-blokken verschijnen alleen bij lessen mét zinnen, in beide talen, met werkende
  "meer"-doorklik.
- `make check` groen; commit per stap (3.1 en 3.2 apart).

---

## Fase 4 — Borging en administratie

1. **`check_parity.py` uitbreiden:** de Tarifit-tokenvergelijking NL↔EN geldt nu ook voor
   `zinnen.html` — maar omdat beide pagina's uit dezelfde CSV renderen is pariteit hier per
   constructie gegarandeerd; de check hoeft alleen te bevestigen dat beide pagina's hetzelfde
   CSV-pad fetchen (goedkope greps). Belangrijker: `check_zinnen.py` draait al in `make check`
   en bewaakt de data zelf.
2. **`CLAUDE.md`** — bron-model-tabel uitbreiden:
   `| Zinnen op de site | assets/zinnen/zinnen.csv | nl+en/zinnen.html en les-blokken laden runtime |`
   plus bij de regels: *de kolommen `les`/`hoofdstuk` met tag `auto` zijn machinaal geclassificeerd;
   handmatige correctie = waarde aanpassen en `auto`-tag verwijderen.*
3. **`WIJZIGINGEN.md`** — rij toevoegen: een zin wijzigen = CSV bewerken; de site volgt vanzelf.
4. **`vercel.json`** — controleer dat `assets/zinnen/` niet door een bestaande regel wordt
   uitgesloten en dat de CSV met een normale cache-header geserveerd wordt (woordenlijst-CSV als
   referentie).

---

## Bijlage — Copy-paste-prompts voor Claude Code

**Fase S**
```
Lees @CLAUDE.md en @plan/PLAN-ZINNEN-WEBSITE.md fase S. Bouw check_spelling_zinnen.py (stap S.1):
zet de normalize()-tabel uit nl/woordenlijst.html regel ±403 één-op-één om naar Python en citeer
de JS-regel in de docstring. Het script leest alleen en schrijft nooit naar zinnen.csv.
Genereer het rapport en toon mij de top 30 kandidaten + de ambigu-sectie. STOP daarna — ik doe
de review. Bouw daarna apply_spelling_zinnen.py (S.3) met dry-run als standaard; pas na mijn
akkoord op de dry-run draai je --apply, gevolgd door make build en make check.
```

**Fase 1**
```
Lees @CLAUDE.md, @plan/PLAN-ZINNEN-WEBSITE.md (fase 0 + 1) en @nl/woordenlijst.html volledig —
dat laatste is het patroon dat je kopieert.
Voer stap 1.1 uit (gedeelde tarifit-search.js, woordenlijst-pagina's omzetten, aparte commit),
daarna 1.2 en 1.3. De tarifit-kolom is read-only; geen enkel script schrijft ernaar.
Draai check_links.py en make check; toon de uitvoer. NL en EN moeten allebei af zijn in
dezelfde commit.
```

**Fase 2**
```
Lees @plan/PLAN-ZINNEN-WEBSITE.md fase 2. Bouw de toggle Lijst|Dialogen op beide zinnen-pagina's.
Controleer eerst met een klein script welke context:-tagwaarden er echt in de CSV staan en
gebruik die — hardcode geen 'dialogue' zonder te kijken. Geen sprekersnamen verzinnen; de
aannameregel onder de toggle is verplicht.
```

**Fase 3.1**
```
Lees @plan/PLAN-ZINNEN-WEBSITE.md stap 3.1. Bouw de onderwerpenindex (grep, niet volledig
inlezen), classificeer in batches van 100, twijfel = leeg laten, tags les:auto/hoofdstuk:auto,
diff mag alleen les/hoofdstuk/tags raken. Rapporteer per batch en stop na elke batch voor mijn
steekproef. Overschrijf nooit een waarde zonder auto-tag.
```

**Fase 3.2**
```
Lees @plan/PLAN-ZINNEN-WEBSITE.md stap 3.2. Bouw assets/js/les-zinnen.js en voeg de ene
script-regel toe aan nl/cursus.html en en/cursus.html — verder blijft cursus.html onaangeraakt.
Max 5 zinnen per les, lessen zonder zinnen krijgen niets, fetch-fout = stil niets tonen.
Test de ?les=NN-doorklik naar zinnen.html.
```

---

## Definition of done

- [ ] Fase S: rapport + review + apply gedraaid; 0 wijzigingen buiten `tarifit`-kolom;
      onbekende-tokens-lijst bewaard als werklijst
- [ ] `assets/js/tarifit-search.js` bestaat; woordenlijst + zinnen delen normalisatie en parser
- [ ] `nl/zinnen.html` + `en/zinnen.html`: zoeken (ook internet-spelling), context/§/pagina-filters,
      kopieerknop, EN-fallback met label, boekvolgorde
- [ ] Dialoogweergave met aannameregel, gegroepeerd per boekpagina, in beide talen
- [ ] `les`/`hoofdstuk` gevuld waar zeker, tag `auto`, steekproef ≥18/20 goed
- [ ] "Uit het boek"-blokken in cursus.html via runtime-injectie; cursus breekt nooit op de fetch
- [ ] Topnav overal bijgewerkt, `check_links` groen, `make check` groen
- [ ] `CLAUDE.md` + `WIJZIGINGEN.md` beschrijven de nieuwe stroom en de `auto`-tagregel
