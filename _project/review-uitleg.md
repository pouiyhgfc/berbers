# Kritische review van `uitleg.html`

> **Status**: eerste pass voor hoofdstukken 1–3. Hoofdstukken 4–18 volgen in een vervolg-ronde nadat jij hierop hebt gereageerd. Dit document is niet uitputtend — het focust op de issues die er echt toe doen voor de kwaliteit van de cursus.

## Werkwijze

- **Bron 1**: OCR-tekst van het boek Mourigh & Kossmann (2019), uit `assets/tarifit-boek.pdf`. De OCR is gemaakt met ABBYY FineReader, kwaliteit redelijk maar **niet perfect** — vooral fonetische tabellen en speciale tekens (ḏ, ɛ, ɣ, etc.) komen vaak verkeerd over. Bij twijfel staat de bevinding hieronder als "niet hard te verifiëren in OCR".
- **Bron 2**: `woordenlijst.csv` — de leidende bron voor spelling van Tarifit-woorden.
- **Vergelijking**: per hoofdstuk lees ik de relevante boek-pagina's en de uitleg-sectie, en noteer wat afwijkt of beter kan.

Categorieën die ik gebruik per issue:
- **[FOUT]** — uitleg klopt niet met boek of CSV
- **[ONDUIDELIJK]** — correct, maar verwarrend of te complex uitgelegd
- **[ONTBREEKT]** — concept staat in boek, niet in uitleg, en hoort er wel in
- **[STIJL]** — vorm-issue dat over alle hoofdstukken speelt, maar hier concreet geïllustreerd
- **[SPELLING]** — Tarifit-woord wijkt af van CSV (CSV is leidend)

---

## Algemene observaties (gelden voor de hele uitleg)

### A1. Stijl: de emoji-overdaad

De uitleg leunt zwaar op emoji's als visuele markers: `📖` voor paginareferenties, `💡` voor inzichten, `⚠️` voor waarschuwingen, `✅` voor "gecontroleerd", `🚨` voor belangrijke punten, `🅰️ 🅱️ 🅲️` voor woordklassen, `🇳🇱` voor vergelijking met Nederlands, `🟢` voor markering. Twee redenen om hier vanaf te stappen:

1. Dit is precies het patroon waaraan AI-detectoren een tekst herkennen. Modellen zetten standaard zulke markers in om "leerzaam" over te komen.
2. Voor een academisch onderbouwde cursus oogt het kinderachtig. De inhoud is volwassen — de typografie hoort dat te zijn ook.

**Voorstel**: emoji's volledig verwijderen. Vervang `📖` door een nette `<small class="page-ref">Boek p. X</small>` of een eyebrow-stijl, vervang `⚠️`-blokken door de bestaande `<div class="box warn">` uit `styles.css` (die staat al klaar, wordt nauwelijks gebruikt), vervang `💡`-blokken door `<div class="box tip">`.

### A2. Stijl: AI-clichés

Frasen die je vaak terugziet en die je daadwerkelijk minder "AI" maken als je ze schrapt:
- "Het idee in één zin: …" — vaak overbodig, gewoon meteen het idee opschrijven
- "Het is belangrijk om te beseffen dat …" — meestal kun je dit weglaten
- "In essentie / kortom / samenvattend …" wanneer er net al iets gezegd is
- "Voor wie geen Arabisch kent: er zijn goede YouTube-video's …" — generiek advies, voegt weinig toe

### A3. Schrijfwijze-spanning: CSV gebruikt andere conventies dan de uitleg

| Letter in uitleg | Letter in CSV | Probleem |
|---|---|---|
| `t̲` (t + combining onderstreep) | `ṯ` (precomposed) | Visueel hetzelfde, byte-wise verschillend — copy-paste levert mismatch op |
| `b̲` (b + combining onderstreep) | `ḇ` (precomposed) | idem |
| `ḏ` (precomposed) | `ḏ` (precomposed) | OK, hetzelfde |
| `c` voor š/sh | `c` | OK |
| `tc` voor č/tch | `c` (zie `cḏeḥ`) of `c` los | Niet altijd consistent in CSV — `tc` komt nauwelijks voor in CSV |

**Voorstel**: bij herschrijven van uitleg consequent de CSV-notatie volgen (`ṯ`, `ḇ`, `ḵ` precomposed). Dat sluit naadloos aan op zoekfunctie in woordenlijst en op de tekst-laag van het OCR-PDF.

### A4. Wat we niet weten: dialect-specifieke uitspraak

Het boek gaat expliciet over Nador / Iqeṛɛiyen Tarifiyt. Niet over Al Hoceima of Beni Iznasen. De uitleg noemt dit één keer in hoofdstuk 1, maar bij specifieke fenomenen (bv. `l` → `ř`, `r` als vocaal) wordt niet meer herhaald dat dit Nador-specifiek is. Voor sprekers uit andere Rif-gebieden kan dat verwarrend zijn.

**Voorstel**: bij vermeldingen van dialect-specifieke uitspraakregels (vooral §2.4, §2.8, §2.9 in uitleg) één zin opnemen die dit benoemt.

---

## Hoofdstuk 1 — Wat is Tarifit?

**Boek p. 9–19 (Introduction).** Uitleg-sectie `#h2` in `uitleg.html`.

### 1.1 [FOUT/ONDUIDELIJK] "Tarifit" vs `t̲arifect̲`

Uitleg zegt: *"Eigen naam: tmazixt (algemeen) of tarifit (specifiek voor 'Riffijns')"*.

Dit klopt **half**. De CSV en het boek geven:
- `t̲mazixt̲` = Berbertaal (zelfreferentie, mannelijke vorm `maziɣ` voor "Berberman")
- `t̲arifect̲` = Riffijnse taal (zelfreferentie, mannelijke vorm `arifi` voor "Riffijn")

Dus `tarifit` is feitelijk de gelatiniseerde academische schrijfwijze van `t̲arifect̲`. Het boek noemt dit expliciet in §1.3: *"Tarifiyt … is a regular feminine form of arifi"*.

**Voorstel**: één zin toevoegen die dit verheldert. Iets als: *"De academische naam Tarifiyt (gebruikt in dit boek en op deze site) is de Latijnse omzetting van het Berberse woord `t̲arifect̲` — letterlijk 'het Riffijnse'. Talen zijn in Tarifit altijd vrouwelijk (zie §3.2)."*

### 1.2 [ONTBREEKT] Boek-glossen die op deze site terugkomen

Het boek heeft op p18–19 een complete lijst afkortingen (`P` perfectief, `I` imperfectief, `NP` negatief perfectief, `NI` negatief imperfectief, `FS` Free State, `AS` Annexed State, `IO` indirect object, `M`/`F` geslacht, `Q` vraagpartikel `ma`, `QA` partikel `qa`, `XAD` modaal partikel `xad`). Wie het boek erbij wil pakken loopt hier tegenaan.

**Voorstel**: een kort kader bovenaan de uitleg (of in hoofdstuk 1) met de meest gebruikte afkortingen. Hoeft niet uitgebreid — de volledige lijst staat op p18–19 voor wie meer wil.

### 1.3 [ONDUIDELIJK] "Verwant aan Arabisch in dezelfde verre zin als Nederlands aan Hindi"

Niet uit het boek (boek beschrijft de Berberse taalfamilie zelf, niet de Afro-Aziatische context). De vergelijking is taalkundig redelijk — Berber en Arabisch zijn beide Afro-Aziatisch maar zitten in verschillende takken (Berber vs. Semitisch). Nederlands en Hindi zijn beide Indo-Europees in verschillende takken (Germaans vs. Indo-Iranisch). Dus didactisch best, maar Hindi voelt willekeurig — Engels als Germaanse-tak en Latijn als Italische-tak ligt dichter bij wat Nederlandse lezers herkennen.

**Voorstel**: behoud de metafoor maar pak een herkenbaarder paar. Iets als: *"Arabisch en Tarifit horen tot dezelfde grote taalfamilie (Afro-Aziatisch), maar zitten in verschillende takken — net zoals Engels en Russisch allebei Indo-Europees zijn maar verre familie."*

### 1.4 [ONTBREEKT] Spaanse invloed / koloniaal verleden

Boek p11–12: *"the Mediterranean coast was occupied by the Spanish from 1912–1956 … Moreover, Spanish is the official language of the enclave of Melilla"*. Dit is direct relevant voor het hoge aantal Spaanse leenwoorden in Tarifit (`payas` matras, `kisu` kaas, `aspanyu` Spanjaard, `mucc` kat ← Spaans `gato`-ish). Bij hoofdstuk 1 zou een halve alinea hierover passen.

### 1.5 [SPELLING/STIJL] Algemene "controle"-claim

Slot van hoofdstuk: *"✅ Hoofdstuk 1 — gecontroleerd met boek p. 9–18"*. De controle-claim suggereert volledige verificatie, terwijl er feitelijk wel iets te corrigeren is (zie 1.1). Als zo'n claim er staat, moet hij ook waar zijn — anders is het ruis.

**Voorstel**: deze "✅"-regel uit alle hoofdstukken halen. Vervang door een neutrale bron-vermelding: *"Bron: boek p. 9–19."*

---

## Hoofdstuk 2 — Klanken, schrijfwijze en uitspraak

**Boek p. 21–33 (Sounds, writing, phonology).** Uitleg-sectie `#h3`.

Dit is een dik hoofdstuk in de uitleg en in het boek. De inhoud is **grotendeels correct**, maar er zit een aantal specifieke fouten en onduidelijkheden in.

### 2.1 [FOUT] §2.4 "Spirantisering" — `tin` vs `tin`-voorbeeld

Uitleg zegt: *"Minimaalpaar uit het boek: tin (schaduw) vs. tin (waarschijnlijk) — het enige verschil is de harde t versus de zachte t."*

Probleem: in plat Latijns schrift staan er twee identieke woorden. De diakrieten (`t̲in` zacht vs `tin` hard) zijn cruciaal voor het minimaalpaar — die zijn vermoedelijk weggevallen door een copy-paste of generatie-stap. Bovendien staat in de CSV:
- `t̲iri` "schaduw" (vrouwelijk variant) — niet `t̲in`
- `t̲iři` "schaduw" of "waarschijnlijk" — beide bestaan

Het echte minimaalpaar uit het boek (p26 / §2.3.1): naar verwachting iets als `t̲in` (zachte t) "schaduw" vs `tin` (harde t) — maar in OCR niet hard te bevestigen. Dit voorbeeld moet of correct getypeset (mét diakrieten) worden, of vervangen door een ander minimaalpaar dat zonder ambiguïteit getoond kan worden.

**Voorstel**: vervangen door een visueel duidelijker minimaalpaar uit boek of CSV. Bijvoorbeeld de werkwoorden `mřes` "trouwen" vs. `mřec` (vrouwelijke vorm trouwen) — duidelijk zichtbaar verschil in schrift.

### 2.2 [SPELLING] Voorbeelden in §2.9 (gevocaliseerde r)

Uitleg gebruikt drie voorbeelden:
| Uitleg | CSV-vorm | Probleem |
|---|---|---|
| `yekker → yekkaa` "hij stond op" | CSV heeft `kkaa` "opstaan" — past | OK |
| `surdu → suadu` "vlo" | CSV heeft `cuaḏu` "vlo" | **`suadu` staat niet in CSV — `cuaḏu` is de leidende vorm** |
| `irden → iaden` "tarwe" | CSV heeft `iaḏen` "tarwe (alleen mv.)" | **`iaden` mist de `ḏ` — moet `iaḏen` zijn** |

Het algemene principe in §2.9 (er → aa, ur → ua, ir → ia) klopt met het boek. De voorbeelden zelf moeten met de CSV-vormen.

### 2.3 [ONDUIDELIJK] §2.5 Faryngalisering — tabel met "d" en "d (spirantized)"

De tabel toont:
- `d` → ض
- `d` (spirantized) → ظ

Beide gerenderd als gewone `d`. Wie de tabel snel scant ziet niet wat het verschil is. In Berber-notatie zou dit `ḍ` (donker hard) vs `ḍ` mét spirantisering moeten zijn — visueel hetzelfde teken, twee verschillende klanken. Dit moet ofwel met expliciete IPA-notatie [dˤ] vs [ðˤ] erbij, of de hele rij vervalt en wordt in lopende tekst uitgelegd.

### 2.4 [FOUT/ONBEVESTIGD] §2.10 onregelmatige verdubbeling — `w → kkw`

Uitleg zegt: *"w → kkw, voorbeeld: yedwef (hij werd) → yeddakkwaf (hij wordt altijd)"*.

Het algemene boek-principe over `w → kkʷ` bij verdubbeling staat in §2.3.5 / §2.3.8. Maar `yedwef` en `yeddakkwaf` als voorbeeld kan ik in OCR niet hard verifiëren — boek schrijft typisch `ḍweř` "terugkeren / worden" (in CSV: `ḍweř`). De vervoeging klopt qua patroon, maar de spelling van het lemma in dit voorbeeld matcht niet met de CSV.

**Voorstel**: vervangen door een voorbeeld dat hard uit het boek + CSV te halen is. Boek gebruikt deze regel bij `aaw → aakkʷ` (zoals in `yeddakkʷaḥ` "hij gaat naar huis", uit `aaggʷeḥ`).

### 2.5 [FOUT] §2.10 onregelmatige verdubbeling — `ř → dz`

Uitleg zegt: *"ř → dz"*. Boek (te zien in TOC §2.3.7 en CSV-evidentie) gebruikt voor de geminate van `ř` de notatie **`ǧ`** (de "j" van Engels *joke*). De `dz`-notatie is zeldzaam en niet wat in dit boek wordt aangehouden. CSV heeft consistent `ǧ`-vormen: `ameǧatc` (ei) is de vrouwelijke vorm van wat in mannelijk geschreven wordt met `ǧ`.

Dit is ook intern inconsistent met §2.8 in dezelfde uitleg — daar staat: *"De dubbele ll is veranderd in ǧ (een klank als de j in het Engelse joke)"*. In §2.10 staat dan plotseling `dz`. Dat is dezelfde klank, twee verschillende notaties in één hoofdstuk.

**Voorstel**: consequent `ǧ` (CSV-vorm), `dz` schrappen.

### 2.6 [ONTBREEKT] Schwa-regel die in boek wel staat

Boek (§2.2): de schwa volgt vaste fonologische regels — wegval in open lettergreep, plaatsing tussen specifieke clusters. Uitleg noemt dit globaal ("hij staat nooit in een open lettergreep") maar geeft geen concrete regels die je kunt toepassen. Voor wie het boek leest is het hoofdstuk over schwa heel formeel, maar één concrete vuistregel zou helpen: *"Vuistregel: schwa schuift naar de voorlaatste medeklinker van een cluster — `xdem` "werken" wordt `xedmey` "ik werk", de schwa schuift voor de tweede medeklinker."*

### 2.7 [SPELLING] §2.8 — `dziret` voor "nacht"

Uitleg: *"dziret ('nacht') komt van het Marokkaans Arabisch l-lila"*.

CSV heeft: `ǧiřet̲` "nacht". Verschil: `dz` vs `ǧ`, en `ř` vs `ř` (hetzelfde) en `t` vs `t̲`. De CSV-vorm is `ǧiřet̲`. Zie ook 2.5 hierboven — dit is dezelfde inconsistentie.

### 2.8 [STIJL] §2.6 "η (ng-klank)" is heel kort

Boek besteedt er een hele subparagraaf aan (§2.3.4 "ŋ"). Uitleg vat het in twee zinnen samen — dat kán, maar het voorbeeld `gwaman ← n waman` is precies één van de gevallen waar je in lopende spraak een `ng` hoort waar geschreven `n w` staat. Een tweede voorbeeldje (uit boek of CSV) zou helpen.

---

## Hoofdstuk 3 — Zelfstandige naamwoorden

**Boek p. 35–50 (The noun).** Uitleg-sectie `#h4`.

### 3.1 [STIJL] Klasse-icoontjes 🅰️ 🅱️ 🅲️

Zie A1. Vervang door tekstuele kop ("Klasse I — Berber-stijl"). De informatie zelf in de drie klassen is grotendeels correct.

### 3.2 [SPELLING] Voorbeelden Klasse II

Uitleg geeft als Klasse II-voorbeelden:
| Uitleg | CSV-vorm |
|---|---|
| `ddexxan` "rook" | `ddexxan` "rook" — **OK** |
| `ssabun` "zeep" | `ṣṣabun` "zeep (collectief)" — **mist `ṣ`-dot** |
| `řxedmet̲` "werk" | `řxeḏmet̲` "werk" — **mist `ḏ`-streepje** |
| `t̲t̲umubin` "auto" | `ttumubin` "auto" — **CSV heeft enkele `t`, geen `t̲`** |
| `arrif` "de Rif" | CSV heeft `Arif` "het Rif (gebied)" — **andere spelling** |

De CSV-vormen zijn in alle gevallen leidend.

### 3.3 [SPELLING] §3.2 "Mannelijk en vrouwelijk" — voorbeeldtabel

Uitleg geeft `aɛabib / t̲aɛabibt̲` "stiefzoon / stiefdochter". CSV heeft:
- `aabib` "stiefzoon" (geen `ɛ`)
- `t̲aabift̲` "stiefdochter" (geen `ɛ`, en `-ift̲` ipv `-ibt̲`)

Het boek (p38) gebruikt `aabib`. De `ɛ` lijkt ten onrechte aan beide vormen toegevoegd in de uitleg.

### 3.4 [FOUT] §3.2 Categorie "talen zijn altijd vrouwelijk"

Uitleg zegt het juist: *"De mannelijke vorm verwijst dan naar de man: amaziy (Berberman), aɛrab (Arabische man), aspanyu (Spaanse man)"*.

Maar `amaziy` zou volgens de CSV `maziɣ` zijn (zonder `a-`-prefix in de CSV-vorm; `ɣ` ipv `y`). En de spelling-conventie in het boek voor de stam-eind-letter wisselt (`y` vs `ɣ`) afhankelijk of er een `t̲` op volgt (assimilatie-regel uit §2.4.2 / uitleg §2.12). Dit hoort eigenlijk verklaard te worden: *"`maziɣ` (man) wordt `t̲mazixt̲` (taal/vrouw) — de `ɣ` wordt `x` voor de vrouwelijke `t̲`-uitgang door de assimilatie-regel"*.

### 3.5 [ONTBREEKT/CRUCIAAL] §3.4 De Staat (Free State / Annexed State)

Dit is volgens het boek (p38–39) **het concept dat het meest verschilt van Nederlands** — en de uitleg behandelt het, maar de uitleg doet het te kort.

Boek §3.1.4 noemt **vijf gebruiks-contexten** voor de Free State (FS):
- isolatie (een woord op zichzelf)
- subject of predicaat in een non-verbale zin
- direct object
- getopicaliseerd element (vóór de hoofdzin)
- na voorzetsels `aɣ` (tot) en `bra` (zonder)

En **vier voor de Annexed State** (AS):
- subject ná het werkwoord
- na alle voorzetsels behalve `aɣ` en `bra`
- als post-topic
- na bepaalde pre-nominale elementen (zoals `bu-`, `ayt̲-`)

Dit is concrete, leerbare informatie. De uitleg behandelt het op een meer schematische manier — maar het missen van de uitzonderingen (`aɣ`/`bra` als FS-voorzetsels) is een gat.

**Voorstel**: bij herschrijven §3.4 uitbreiden met een tabel van FS-contexten en AS-contexten, met één voorbeeld per context.

### 3.6 [ONDUIDELIJK] §3.3 Meervoudspatronen — zes types is veel

De uitleg beschrijft zes meervoudspatronen (a- → i-, klinkerwisseling, suffix toevoegen, …). Boek behandelt het in §3.2.4 in vergelijkbare detail, maar schikt het met een **hoofd-onderscheid** vooraf: *externe* meervouden (alleen affix-verandering) vs. *interne* meervouden (klinker-verandering in de stam) vs. *gemengde* meervouden. Die hiërarchie-eerst-aanpak werkt didactisch beter dan een vlakke lijst van zes patronen.

**Voorstel**: bij herschrijven dezelfde hiërarchie aanhouden — eerst de twee hoofdcategorieën, dan binnen elk de subpatronen.

### 3.7 [ONTBREEKT] §3.7 Pre-nominale elementen — `u-`, `ayt̲-`, `bu-`, `m(u)-`

Uitleg behandelt deze kort, maar het boek heeft hier een rijker overzicht (p49). In het bijzonder:
- `u` (eigenaar, M) — bv. `u Aliman` "de Duitser"
- `ayt̲` (lid van groep) — bv. `ayt̲ Nnaḍuṛ` "Nadorianen"
- `bu` (eigenaar M / iemand met) — bv. `bu lqehwa` "koffie-eigenaar / koffie-drinker"
- `mu`-/m- (eigenaar V / iemand met) — bv. `m lqehwa` "koffie-vrouw"

Dit is praktisch voor wie eigennamen of beschrijvingen wil gebruiken. CSV bevat `bab` (eigenaar) en `m` (eigenaresse, V) als losse entries — deze zijn alléén pre-nominale elementen, niet zelfstandig gebruikt.

---

---

## Hoofdstuk 4 — Werkwoorden

**Boek p. 51–64 (The verb).** Uitleg-sectie `#h5`.

Dit is een dik en belangrijk hoofdstuk. De **conjugatietabel** in §4.1 is grotendeels in orde; de issues zitten vooral in de afgeleide vormen (§4.2) en aspect (§4.3).

### 4.1 [ONDUIDELIJK] §4.1 Vervoegingstabel — alleen `qqim` als voorbeeld

Uitleg geeft de complete vervoeging van `qqim` "zitten". Het boek (p51, tabel "Normal conjugation") gebruikt **vier** voorbeeldwerkwoorden naast elkaar omdat de uitgangen subtiel verschillen voor werkwoorden eindigend op een klinker (`cfa`, `wda`) of op `y`/`z` (`yez`). Bijvoorbeeld:
- `wda` "vallen": 2SG = `tewdid` (-id), niet `-ed`
- `yez` "graven": 2SG = `teyzed` of `teyzid` afhankelijk van aspect

Voor cursus-niveau is één werkwoord (`qqim`) prima. Maar de uitleg zou minimaal moeten **noemen** dat klinker-eindigende stammen variaties krijgen, met verwijzing naar boek p51 voor de volledige tabel.

### 4.2 [FOUT] §4.2.1 ss-causatief — voorbeeld `iaḍ`

Uitleg geeft: *`iaḍ` (dragen) → `ssiaḍ` (aankleden)*. CSV heeft `iaḏ` "kleden, dragen" en `ssiaḏ` "iemand kleden" — beide met zachte `ḏ`, niet de donkere `ḍ`. Spelfout in uitleg.

### 4.3 [FOUT/MISLEIDEND] §4.2.2 mm- als "wederkerig" — reflexief mist

Uitleg classificeert `mm-` als "elkaar" (wederkerig). Boek p55–56 zegt expliciet:

> *"Note that the middle derivation is not used in reflexives, which are expressed by means of the phrase ixefn-"*

Met andere woorden: voor "ik sla mezelf" gebruik je **geen** `mm-`-werkwoord, maar de constructie `ixef nnes` (lett. "zijn hoofd / zelf") + werkwoord. Voorbeeld uit boek: `yewta ixefnnes` "hij sloeg zichzelf".

Dit is een fundamenteel onderscheid (wederkerig "elkaar" vs. reflexief "zichzelf") dat in de uitleg ontbreekt — een Nederlandstalige zal anders denken dat je `mm-` kunt gebruiken voor beide.

### 4.4 [SPELLING] §4.2.2 voorbeelden van middel/wederkerig

| Uitleg | CSV | Probleem |
|---|---|---|
| `ny` (doden) | `ney` "doden" | uitleg mist de `e` |
| `mney` (vechten) | `mney` "vechten" | OK |
| `ndaq` (gooien) | `nḍaa` "gooien" | **echte fout** — `ndaq` lijkt een typo, CSV heeft `nḍaa` |
| `mmendaq` (gegooid worden) | (afleiding) | hangt af van `nḍaa` als basis: dan `mmenḍaa` |
| `qřeb` (omdraaien) → `mneqřeb` | CSV: `qřeb` ✓, `nneqřeb` "zich omdraaien" | uitleg heeft `mneqřeb` met enkele `n` — moet `nneqřeb` met dubbele |

### 4.5 [ONTBREEKT] §4.2.2 mm- heeft veel allomorfen

Boek p56–58 noemt vijf allomorfen voor de "middel" derivatie:
- `mm-` (standaard)
- `m-` (verkorte vorm bij sommige werkwoorden)
- `mř-` (vóór werkwoorden die met `a` beginnen, zoals `mřadas` "dichtbij elkaar zijn")
- `n-` / `nn-` (vooral bij stammen met labiale medeklinkers)
- `nnu-` (zoals `nnuqzem` "geopend worden")

Uitleg vermeldt alleen `mm-`. Dat verklaart waarom `mřaya` (mř-), `mney` (m-), `nnedfes` (nn-), `nnuqzem` (nnu-) er allemaal anders uitzien — wat de leerling anders verwarrend vindt.

### 4.6 [STIJL] §4.3 Aspect — emoji-explosie

Deze paragraaf opent met `🚨 Dit is het belangrijkste concept`, daarna `🇳🇱 Nederlands denkt in TIJD`, `🟢 Tarifit denkt in ASPECT`, met `⭐` in de kop zelf. Vier emoji's in twee alinea's. Inhoudelijk is de uitleg correct — die emoji's voegen niets toe en maken het kinderachtig oogend voor wat juist hét academische zwaartepunt is.

**Voorstel**: emoji's eruit, vervang door een nuchtere kop ("Aspect — het verschil met Nederlands") en gebruik bestaande `<div class="box warn">` voor de waarschuwing. De inhoud van de uitleg op zich is goed.

### 4.7 [ONTBREEKT] §4.3 Aorist na Perfectief in narratieve sequenties

Uitleg behandelt Aorist alleen "met partikels" (`ad`, `xad`). Maar boek p113–114 noemt een belangrijk **derde** gebruik:

> Aorist wordt gebruikt voor opeenvolgende werkwoorden in een verhaal — als de eerste actie in Perfectief staat, kunnen vervolgacties in Aorist staan, geïnterpreteerd als "en toen X-en, en toen Y-en".

Dit is praktisch belangrijk voor wie verhalen leest of vertelt. Hoort in §4.3 een korte vermelding te krijgen.

### 4.8 [FOUT] §4.3 voorbeeld `xa tdu` "ze zal zeker wegvliegen"

`xa` is correct (irrealis-partikel `xa(d)` van §7.1.1). Maar:
- `tdu` zou de Aorist 3SG:F moeten zijn van `ḏu` "vliegen" (CSV-vorm). Met de t-prefix wordt dat `t̲ḏu` — niet `tdu` zonder spirantisering.
- "wegvliegen" is een over-vertaling — `ḏu` betekent gewoon "vliegen". Een specifiekere bron-context ontbreekt; in OCR niet hard te verifiëren.

Vervang met een geverifieerd voorbeeld, bv. `xa yeyya` "hij gaat zeker komen" (uit boek-context).

### 4.9 [FOUT] §4.3 voorbeeld `Mřič tudes` "Melilla is dichtbij"

`Mřič` ✓ (CSV). `tudes` zou 3SG:F Perfectief zijn van `aḏes` "dichtbij zijn" (CSV) — patroon `a-` → `u-`, plus prefix `t-`. Dat geeft `t̲uḏes`, niet `tudes`. De spirantisering ontbreekt op twee plekken.

### 4.10 [DUBBELING] §4.4 partikels qa/tuya/aqqa/t̲ɣiř hoort in h8

In de uitleg-structuur staat §4.4 "De partikels qa en tuya — pseudo-werkwoorden", maar dat is precies wat hoofdstuk 8 (Pseudo-verbs) ook behandelt. Boek behandelt ze **alleen** in hoofdstuk 8 (p83–86) en in hoofdstuk 13 (p115–118 voor aspect-interactie).

Dubbeling kost ruimte en geeft kans op inconsistentie. Tegelijk heeft de leerling op dit punt in h4 wel iets nodig over `qa` (komt al in tabel als "qa + Imperfectief"). 

**Voorstel**: in §4.3 alleen kort `qa` introduceren ("zie h8 voor uitgebreid"), en §4.4 weghalen — alle pseudo-werkwoorden in h8.

### 4.11 [FOUT] §4.5 "gaan" — `qaggʷeḥ` is geen werkwoord

Uitleg zegt: *"Verwant: `qaggʷeḥ` 'naar huis gaan'"*. Dit is een samentrekking van `qa + aggʷeḥ`. CSV heeft `aaggʷeḥ` "naar huis gaan" als zelfstandig werkwoord, en `qa` als partikel. De combinatie betekent dus "hij is nu naar huis aan het gaan" (qa + Imperfectief van aaggʷeḥ).

**Voorstel**: aanpassen naar *"Verwant: `aaggʷeḥ` 'naar huis gaan' (vaak gebruikt met partikel `qa`)"*.

---

## Hoofdstuk 13 — Aspect, modus en ontkenning

**Boek p. 113–127 (Aspect, mood and negation).** Uitleg-sectie `#h14`.

Dit hoofdstuk werkt h4 §4.3 verder uit en behandelt ontkenning systematisch. Het is goed gestructureerd, maar mist een paar concrete constructies die in het boek prominent staan.

### 13.1 [DUBBELING] §13.1 herhaalt h4 §4.3-tabel

De openings-tabel "Wanneer welk aspect?" overlapt grotendeels met de tabel in h4 §4.3 ("Wat is aspect concreet?"). Beide tonen dezelfde combinaties (Imperfectief alleen vs. `qa` + Imperfectief, Perfectief, `ad` + Aorist). Het verschil is dat §13.1 uitgebreider is (incl. ontkenning-rijen).

**Voorstel**: in h4 alleen het *concept* van aspect introduceren (geen tabel), en de complete tabel verplaatsen naar §13.1. Dat scheelt verwarring.

### 13.2 [ONTBREEKT] §13.2 — `qa` als unmarked bij locatieven

Boek p115–116: bij locatieve uitdrukkingen ("ergens zijn") is `qa` de **standaard** keuze. Voorbeeld uit boek:
- `uma-s qa-t̲ ḏi t̲aḏḏart̲` "zijn broer is thuis" — met `qa`, gewoon
- `Mřič ḏayes ispunya` "in Melilla zijn de Spanjaarden" — *zonder* `qa`, drukt afstandelijkheid uit

Dit is een nuttig praktisch onderscheid voor wie wil weten *wanneer* je `qa` weglaat. Nu staat in §13.2 alleen *welke aspecten* na `qa` kunnen, niet *of* je `qa` standaard zou moeten gebruiken.

### 13.3 [SPELLING] §13.2 voorbeelden

| Uitleg | CSV-vorm | Probleem |
|---|---|---|
| `igemmaa` "vullen" | `ɛemmaa` "vullen" | mist `ɛ`-prefix in stam |
| `ayarraf` "waterkruik" | `ayaṛṛaf` | mist donkere `ṛṛ` |
| `užedjid` "koning" | `ajeǧiḏ` | uitleg gebruikt `dj`, CSV gebruikt `ǧ` (zie ook h2-issue 2.5/2.7 — zelfde inconsistentie) |
| `qaa t̲aaḥed yaa barra` | (`qa` + `t̲aaḥed`) | typo: `qaa` met dubbele a |

### 13.4 [DUBBELING] §13.3 deelt voorbeelden met §4.4

Het voorbeeld `zzman t̲uya t̲nayen n duru tsekkʷa` "vroeger was twee duro veel waard" staat letterlijk in §4.4 én §13.3. Eén kan weg, of de twee secties moeten gemerged worden. Zie ook h4 issue 4.10.

### 13.5 [SPELLING/ONDUIDELIJK] §13.3 `t̲uya-t̲` als "hij was"

Uitleg geeft `t̲uya-t̲ d ameddukeř inu` "hij was mijn vriend (maar nu niet meer)". 

`-t̲` is een direct object clitic. Voor 3SG:M is dat `-t̲` (`hem`); voor 3SG:V is dat `-t̲` (`haar`) — zelfde vorm, verschillende functie. Dat is verwarrend zonder uitleg. De gloss zou expliciet moeten maken dat hier 3SG:M-DO bedoeld is. Een betere illustratie zou een werkwoord met geschreven 3SG:M-uitgang zijn waar het verschil duidelijk is.

### 13.6 [GROOT GAT] §13.4 mist twee belangrijke "zijn"-constructies

De uitleg behandelt drie typen "zijn"-constructies (non-verbaal met `d`, met werkwoord `iři`, bezit met `yaa`). Twee belangrijke constructies uit boek p112 ontbreken:

**A. De `yifan`-constructie voor possessieve vragen.** Concreet:
- `wi yifan t̲t̲umubin-a?` "wiens auto is dit?" (lett. *wie bezit deze auto*)
- `wi t̲-yifan?` "van wie is het?"
- `wi s-yifan?` "van wie ben je een kind?" / "wie is je vader?"

`yifan` is een onregelmatige vorm (volgens boek vermoedelijk een fossiel van een verloren werkwoord "bezitten"). Voor wie eigendom-vragen wil leren stellen is dit cruciaal — staat nergens in uitleg.

**B. Similatief met `gg` "doen, lijken op".** Voorbeeld uit boek:
- `yegga am wayrad` "hij is als een leeuw"

Met deze constructie zeg je dat iets ergens **op lijkt**. CSV heeft `gg` "doen, maken, lijken op" — dus de derde betekenis ("lijken op") staat al in CSV maar wordt in uitleg niet als "zijn"-variant uitgelegd.

### 13.7 [SPELLING] §13.4 voorbeelden

| Uitleg | CSV / boek | Probleem |
|---|---|---|
| `Llah yedja` "God bestaat" | `Ḷḷa(h)`, en boek heeft `yedzan` als regulier Perfectief | uitleg `yedja` is enkele `j` waar het `dz` of `ǧa(n)` zou zijn |
| `yar-i ijjen t̲t̲umubin` | `ijjen`, `ttumubin` | `t̲t̲` ipv `tt` (decomposed vs. precomposed: CSV gebruikt `tt`) |
| `yaas ijj uma-s` | `ijjen` (CSV) | `ijj` zonder `-en` is verkorte spreektaalvorm — oké maar inconsistent met regel hierboven, kies één |

### 13.8 [STIJL] §13.5 — `ša` vs `sa` vs `ca`

Uitleg zegt: *"ca (ja, geschreven als `ša` in het boek)"*.

De feitelijke schrijfwijze in het boek is **`sa`** — een romanisering met diakritisch teken (carón) op de `s` dat vermoedelijk in OCR zonder diakriet wordt weergegeven (`š` → `s`). Maar de notatie waar de uitleg op wijst (`ša`) is in het boek nooit zo gespeld. Dit is verwarrend voor wie het boek erbij pakt. CSV heeft consequent `ca` (learntarifit-conventie), wat klopt.

**Voorstel**: corrigeren naar *"ca (in het boek geschreven als `š` met carón, dus visueel `š` of in plain-text vaak `s`)"*. Of simpeler: alleen vermelden dat de uitleg `ca` aanhoudt, zonder verwijzing naar de boek-notatie.

### 13.9 [ONTBREEKT] §13.5.3 — boek heeft 6 postverbale negatoren, niet 4

Uitleg lijst: `bu`, `ḥedd`, `walu`, `ura d`. Boek p125–126 noemt minstens twee extra:
- `qaɛ` "totaal/geheel" — bv. `waa dinni bu ffaaq qaɛ` "er is daar helemaal geen verschil"
- `ɛemmaas` "nooit" — bv. `waa ggu ɛemmaas` "ik doe het nooit"

Beide staan ook in CSV (`qaɛ`, `ɛemmaas`). Vooral `ɛemmaas` is praktisch onmisbaar voor "nooit"-zinnen.

### 13.10 [ONTBREEKT] §13.5 — syntactische regels rond `bu`

Boek p124 geeft drie concrete regels die in de uitleg ontbreken:
1. **Een naamwoord na `bu` staat in de Annexed State.** Voorbeeld uit boek: `waa das-teggen bu wexxam` "ze gaan geen huis voor hem maken" — `wexxam` (AS), niet `axxam` (FS).
2. **`bu` kan niet samen met `ca`** voorkomen — kies één.
3. **`bu` is verplicht in sommige constructies**, bv. `waa yaas bu t̲amɣaaṯ` "hij heeft geen vrouw" (eigendoms-ontkenning vereist `bu`).

Praktische, leerbare regels — ontbreken volledig.

### 13.11 [SPELLING/ONDUIDELIJK] §13.5 voorbeelden van ontkenning

| Uitleg | CSV | Probleem |
|---|---|---|
| `ssawař` "spreek!" (Imperfectief in `wiř ssawař`) | CSV heeft `ssiweř` "praten, spreken" | `ssawař` is een vervoegde vorm — Imperatief 2SG:M zou `ssiweř` zijn (gewoon de stam). De vorm `ssawař` die uitleg geeft is een Imperfectief-stam — die is correcter na `wiř`/`waa`, maar dan moet de gloss "spreek!" worden vervangen door "spreek niet" (negatieve imperatief = `wiř/waa` + Imperfectief 2SG-vorm) |
| `t̲-t̲iwyey` (in `necc waa t̲-t̲iwyey ca`) | `awi` "nemen, trouwen" | structuur lijkt: `t̲-` 3SG:F-DO + `t̲iwyey` 1SG-Imperfectief. Klopt patroon-wise, maar de dubbele `t̲t̲` aan het begin (clitic + prefix) verdient een gloss-uitleg |

### 13.12 [STIJL] "✅ Hoofdstuk 13 — gecontroleerd" weghalen

Zoals in alle hoofdstukken — claim klopt niet (er staan dingen die niet kloppen), beter neutrale bron-vermelding.

---

---

## Hoofdstuk 5 — Persoonlijke voornaamwoorden

**Boek p. 65–71 (Personal pronouns).** Uitleg-sectie `#h6`.

### 5.1 [FOUT] §5.1 "wij" = `nessin` is verkeerd

Uitleg geeft `nessin` voor "wij". CSV heeft `neccin`. Boek p65 (te lezen via voorbeelden in latere paragrafen) heeft ook `neccin`. **`nessin` is een typo** — de `ss` in plaats van `cc` (de "sh"-klank).

### 5.2 [ONTBREEKT/ONDUIDELIJK] §5.2.1 DO-tabel — wanneer welke vorm?

De tabel onderscheidt drie kolommen: "Na werkwoord (I)", "Na werkwoord (II)", "Vóór werkwoord". Voor 3SG:M staan er bv. `t` (I), `iṯ` (II), en `t̲(t̲)` (vóór). Maar de uitleg legt **niet uit wanneer** je welke variant gebruikt:

Boek p66 is concreet: na een werkwoord met klinker-eindigende stam in Perfectief krijg je `it`, na medeklinker-eindigende stam `t`. Plus: na 3SG:M-DO en 2/3PL:F-DO komt het deictic clitic in de vorm `id` (niet `d`). Voorbeelden uit boek:
- `yessiwd-it̲-id` "hij heeft hem hier gebracht" (3SG:M-DO + `id` na M)
- `yessiwd-isent̲-id` "hij heeft jullie (V) hier gebracht"

Zonder deze regel is de tabel niet bruikbaar — de leerling ziet drie kolommen en weet niet welke te kiezen.

### 5.3 [ONTBREEKT] §5 — geen sectie over emphasizers (boek §5.3)

Boek p68/71 heeft een aparte paragraaf over twee emphasizers:
- **`nnit̲`** "zelf, op eigen kracht" (klemtoon op werkwoord-onderwerp). Voorbeeld: `a t̲-awyey nnit̲` "ik zal haar zelf trouwen".
- **`simant̲ n-`** "zelf" + persoonlijk voornaamwoord. Voorbeeld: `usiy-d necc simant̲ inu` "ik kwam zelf".

Beide praktisch nuttig voor "zelf"-uitdrukkingen — ontbreken volledig in uitleg. CSV heeft `simant` "zelf (reflexief voornaamwoord)" — dat is dezelfde stam.

### 5.4 [ONDUIDELIJK] §5.2.5 — `inu` "onregelmatig" zonder uitleg

Uitleg meldt: *"`inu` 'van mij' (onregelmatig!)"* maar laat het daarbij. Boek p67 voetnoot zegt waarom: voor 1SG met `n` "van" is de regelmatige vorm `*ni`, maar in Iqeṛɛiyen Tarifit is dit altijd `inu`. Dat geldt **alleen** voor `n`. Bij andere voorzetsels gebruik je gewoon `-i`: `kiḏi` "met mij", `yari` "bij mij" (1SG-suffix). De uitleg zou minimaal moeten zeggen: *"De 1SG-vorm bij `n` is altijd `inu`, niet `ni`. Bij andere voorzetsels is 1SG gewoon `-i`."*

### 5.5 [SPELLING] §5.2.5 voorbeelden bij `aked` "met"

| Uitleg | CSV/boek | Probleem |
|---|---|---|
| `kiḏes ~ kic` "met hem" | boek p67 heeft `kides ~ kis` | uitleg `kic` ipv `kis` — kan een variant zijn maar dan moet beide vermeld; CSV heeft niet `kic` als losse vorm |
| `kiḏem ~ kim` "met jou (V)" | boek `kim ~ kidem` | OK |
| `kiḏi` "met mij" | CSV heeft `akiḏ` als basisvorm `aked + i` → `kiḏi` | OK |

### 5.6 [SPELLING] §5.2.6 — `mmi-t̲ney` versus `mmi-tney`

Boek p67 expliciet: *"the presence of an element t before plural pronouns"* — gewoon `t`, geen spirantisering. Uitleg gebruikt `t̲ney` (zacht), `t̲sen` (zacht). CSV heeft niet de exacte combinaties maar consistent geen `t̲` waar geen spirantisering geldt.

Voorstel: aanpassen naar `mmi-tney`, `mmi-tsen` (gewone harde `t`).

### 5.7 [ONTBREEKT] §5 mist een uitleg over hoe DO-clitica vóór schwa-eindigende werkwoorden werken

Boek p66: *"If d is used after a Perfective belonging to the class which has no stem-final vowel in the imperative, but i or a in the Perfective, the final vowel a is absent; instead, schwa is found, e.g. yus-ed 'he has come'"*. 

Dat verklaart waarom `yus-eḏ` (uitleg §5.2.3) er zo uitziet — niet `yusa-ḏ` zoals je naïef zou verwachten. Voor leerlingen die patronen proberen te herkennen is dit relevant.

---

## Hoofdstuk 6 — Aanwijzende voornaamwoorden

**Boek p. 73–75 (Deixis and demonstrative pronouns).** Uitleg-sectie `#h7`.

### 6.1 [ONTBREEKT] §6.1 — assimilatie-regel "vocalized r reappears" mist

Boek p73 noemt vier assimilatie-regels bij deictic-suffixen. Drie staan in uitleg:
1. Na klinker → `y` ingevoegd vóór `-a`/`-in` ✓
2. `-enni` na klinker → `-nni` ✓
3. Na schwa+enkele medeklinker → medeklinker geminate ✓

Maar de **vierde** mist:
4. **Na woorden met gevocaliseerde `r` (`-aa`-eind) verschijnt de `r` weer in de afgeleide vorm** — bv. `awessaa` "oude man" → `awessar-a` "deze oude man" (de stam-`r` komt terug). Geldt **niet** voor `-enni`: `awessaa-nni` (geen `r`).

Dit is geen randverschijnsel — het verklaart waarom je opeens een `r` ziet die er in de basisvorm niet is. Hoort er bij.

### 6.2 [ONTBREEKT] §6.2 mist drie sets demonstratieve voornaamwoorden

Uitleg toont één set (`wa`/`win`/`wenni` etc.). Boek p70 heeft daarnaast nog drie sets die in de uitleg ontbreken:

**Set A — Emphatische vormen** (proximale "deze, met nadruk"):
- M:SG: `wa-nit̲a`, `wa-nit̲at̲`, `wa-nit̲ati`
- V:SG: `t̲a-nit̲a`, `t̲a-nit̲at̲`, etc.
- Voor "deze hier (specifiek)" — dichter dan gewoon `wa`

**Set B — VAGUE-vormen** (`winat̲`, `t̲inat̲`, `inat̲en`, `t̲inat̲in`):
- Vergelijkbaar met "dat ding" / Engels "thingummy" / Frans "ce truc-ci"
- Praktisch in spreektaal

**Set C — Met `man` "welke"** (`man wen`, `man t̲en`, `man yin`, `man t̲in`):
- Voor vragen "welke (man)?" "welke (vrouw)?"
- Loopt vooruit op h12 (Vragen)

Voor cursus zijn Set A en C wel belangrijk. Set B is detail.

### 6.3 [FOUT/ONTBREEKT] §6.2 — hoe je de losse vormen wel/niet gebruikt

Boek p69 expliciet: *"This combination of pronoun and deictic functions only as an independent demonstrative pronoun ('this one is blue'), and is not used in apposition ('this man')"*.

Dat betekent dat je voor "deze man" **niet** `wa aayaz` kunt zeggen — dat moet `aayaz-a` zijn (suffix-vorm uit §6.1). De `wa`-vormen worden **alleen** zelfstandig gebruikt: `wa d aayaz` "dit is een man".

Dat onderscheid staat niet in §6.2. Een leerling kan denken dat `wa aayaz` werkt zoals Nederlands "deze man" — fout.

### 6.4 [ONTBREEKT] §6.3 emphatic plaats-aanwijzers

Uitleg toont `ḏa`, `ḏin`, `ḏiha`, `ḏinni`. Boek p71 heeft ook `ḏanit̲a`, `ḏanit̲at̲`, `ḏanit̲ati` (emphatic "echt hier") — staat ook in CSV (`ḏanit̲a`). Idem `ssanit̲a` voor pad.

### 6.5 [STIJL] §6 — gemiste link naar boek §11.2

De uitleg in §6.1 noemt `aayaz-a` "deze man" als suffix-constructie, maar legt niet uit dat dit pas mogelijk is **omdat het naamwoord in de Free State staat**. Voor wie h3 §3.4 nog niet helemaal beheerst: een korte verwijzing zou helpen.

---

## Hoofdstuk 7 — Het verbale complex (clitica)

**Boek p. 77–82 (The verbal complex).** Uitleg-sectie `#h8`.

Dit hoofdstuk is **goed gestructureerd** — de drie subsecties (preverbale partikels, verplaatsbare clitica, fronting) volgen het boek precies. De issues zijn vrij lokaal.

### 7.1 [INCONSISTENT] §7.1 `xad` als "sterker dan ad"

Zelfde issue als in h4 (4.8). Uitleg classificeert `xad` als "sterker dan ad — meer zekerheid of nadruk". Boek p77 (TOC §7.1.1, beschrijving p77) presenteert `xa(d)` als een **modaal partikel** met aparte semantische nuance, niet als gradatie van `ad`. CSV heeft `xaḏ` "irrealis-partikel met meer zekerheid" — dichter bij uitleg's interpretatie maar nog steeds niet "sterker = meer-toekomst". Het is meer "modale modus", niet temporele kracht.

**Voorstel**: aanpassen naar *"`xa(d)` — modale variant van `ad`. Drukt sterkere aanname of verwachting uit dat de actie zal plaatsvinden, vaak met de connotatie van een waarschuwing of dreiging."* En dan een passend boek-voorbeeld in plaats van `xa t̲du`.

### 7.2 [FOUT] §7.1 voorbeeld `xa t̲du`

Zelfde fout als h4 issue 4.8: `tdu` zonder spirantisering — moet `t̲ḏu` zijn (3SG:F prefix `t̲` + stam `ḏu` "vliegen", beide zacht door regels). En de vertaling "ze zal zeker wegvliegen" is over-vertaald — `ḏu` is gewoon "vliegen", "weg" zit niet in het werkwoord.

### 7.3 [SPELLING] §7.3 voorbeeld `meelik`

Uitleg gebruikt `meelik` "als (counterfactueel)" in de lijst van voegwoorden die clitic-fronting triggeren. CSV heeft `meɛlik`. Spelfout: ontbrekende `ɛ` (ayin). Boek p79 heeft ook `meelik` in OCR — maar OCR mist consequent de `ɛ`. CSV is leidend.

### 7.4 [GOED] §7.2/§7.3 structuur is correct

De volgorde "IO – DO – ḏ – voorzetsel" klopt met boek p78. De vijf contexten waarin clitic-fronting verplicht is (na ad/xad/waa, in bijzinnen, in clefts, bij vraagwoorden, na bepaalde voegwoorden) komen letterlijk overeen met boek p79–80. Dit is het soort hoofdstuk waar je relatief weinig hoeft aan te passen — vooral spelling en `xad`-uitleg.

### 7.5 [ONTBREEKT] §7.1 — de partikel `qa` ontbreekt in deze paragraaf

Uitleg behandelt in §7.1 vier preverbale partikels: `ad`, `xad`, `ya`, `waa`. Maar **`qa`** wordt niet genoemd, terwijl het volgens boek p77 ook een preverbal element is (`qa` "present relevance"). Het wordt later wel behandeld in §4.4, §8.1, §13.4 — overal verspreid.

**Voorstel**: in §7.1 een korte verwijzing opnemen naar `qa` met cross-link naar h8/h13: *"Het partikel `qa` (zie h8 en h13) is ook preverbal maar gedraagt zich anders dan ad/xad/waa — het kan ook met non-verbale predicaten."*

### 7.6 [STIJL/CLAIM] §7 — de "✅ gecontroleerd"-regel

Idem als andere hoofdstukken. Bij herschrijven weghalen.

---

---

## Hoofdstuk 8 — Pseudo-werkwoorden

**Boek p. 83–86 (Pseudo-verbs).** Uitleg-sectie `#h9`.

### 8.1 [STRUCTUUR] §8 mist twee van de vijf pseudo-werkwoorden

Boek p83 lijst **vijf** pseudo-werkwoorden in deze volgorde: `qa`, `tuya`, `aqqa`, `t̲ɣiř`, `ay`. Uitleg behandelt er **drie** (`aqqa`, `t̲ɣiř`, `ay`) en zegt: *"Voor `qa` en `t̲uya` — zie Hoofdstuk 4.4 hierboven."*

Probleem: `qa` en `t̲uya` zijn nu verspreid over drie plekken (h4 §4.4, h8, h13 §13.2/13.3). Dat geeft dubbele uitleg met inconsistentierisico (zie h13 issue 13.4). Het boek behandelt ze hier omdat ze in syntaxis-typologie pseudo-werkwoorden zijn — een aparte klasse die DO-clitica accepteert maar geen eigen aspect-morfologie heeft.

**Voorstel**: alle vijf pseudo-werkwoorden in h8 behandelen. In h4 alleen kort verwijzen (`qa` / `tuya` zijn pseudo-werkwoorden — zie h8 voor details).

### 8.2 [ONDUIDELIJK] §8.3 `ay` — IO of DO?

Uitleg geeft *"`ay-am` 'alsjeblieft, hier (voor jou V)!'"* met de implicatie dat `am` een DO is. Boek p85 expliciet: 

> *"It is always followed by an Indirect object pronoun indicating the recipient; in addition there may be a Direct object pronoun indicating the object that is presented."*

Dus `ay-am` = "ay + IO 2SG:F" (= "voor jou (V)"), en `ay-am-t̲` = "ay + IO 2SG:F + DO 3SG:M" (= "hier heb je het (V), voor jou"). De structuur "IO + (optioneel DO)" wordt in uitleg niet expliciet gemaakt, terwijl dat juist het mechanisme is.

### 8.3 [ONTBREEKT] §8.2 — `t̲ɣiř` ook als gewoon werkwoord

Boek p84–85: *"It is also possible to have a construction in which `tɣir` is a defective verb with only an aspectual stem, but conjugated according to the normal conjugation."* Voorbeelden uit boek:
- `t̲ɣirey d ssehh` "ik dacht dat het waar was" (1SG-vervoeging)
- `t̲ɣiren azenna yewda-d` "zij dachten dat de hemel was gevallen" (3PL:M)

Uitleg geeft alleen pseudo-vormen (`t̲ɣiř-asen`). De vervoegde vorm ontbreekt — terwijl die in praktijk veel voorkomt.

### 8.4 [SPELLING] §8.1 inconsistente notatie `t̲` / `ṯ`

Uitleg gebruikt door elkaar:
- `aqqa t̲xaḏent̲` (decomposed `t̲`)
- `aqq-eṯ` (precomposed `ṯ`)
- `aqq-awem-t̲` (decomposed)

Visueel hetzelfde, byte-wise verschillend. Eén notatie kiezen — CSV gebruikt precomposed `ṯ`, dat is dan leidend.

### 8.5 [STIJL] §8 — emoji's en "✅ gecontroleerd"

Standaard issues: `🎯`, `📖`, `📌`, `✅` — bij herschrijven weghalen.

---

## Hoofdstuk 9 — Voorzetsels

**Boek p. 87–95 (Prepositions).** Uitleg-sectie `#h10`.

### 9.1 [FOUT/INCOMPLEET] §9.1 — drie FS-uitzonderingen, niet twee

Uitleg's openingsregel: *"Bijna alle voorzetsels worden gevolgd door Annexed State. Uitzonderingen: `aṛ` 'tot' en `břa` 'zonder'."*

Boek p87, tabel-noot expliciet: drie voorzetsels nemen Free State (gemarkeerd met `+FS`):
- `aṛ` "tot" ✓
- `břa` "zonder" ✓
- **`amecnaw`** "zoals" — MIST in algemene regel

Verderop in §9.1.13 wordt `amecnaw` wel gemarkeerd als "(+FS)" in de tabel, maar de algemene regel bovenaan klopt niet. Een leerling die alleen de regel onthoudt, zit fout bij `amecnaw`.

### 9.2 [ONTBREEKT] §9.1.4 `yaa` voor bezit — kan niet rechtstreeks met naamwoord

Uitleg toont de bezitsconstructie: *"`nettat̲ yaas ijj uma-s` 'ze heeft een broer'"*. Klopt. Maar het boek (p84) noemt expliciet een belangrijke beperking:

> *"It is impossible to have `yaa` followed by a full noun in a possessive construction. The possessor can only be expressed lexically by means of topicalization."*

Dat betekent: je kunt **niet** zeggen `*yaa baba ttmenyat` voor "vader heeft geld". De juiste vorm is via topicalisatie: `baba, yaas ttmenyat` (lett. "vader, bij hem geld"). Dit is een concrete fout-preventie-regel die ontbreekt.

Bovendien moet onderscheid gemaakt worden tussen `yaa` als voorzetsel ("naar/bij") en `yaa` als bezitsmarker. Boek p84 heeft hiervoor twee voorbeelden naast elkaar:
- `iruḥ yaa baba` "hij ging naar mijn vader" (voorzetsel-betekenis)
- `baba, yaas ttmenyat` "mijn vader heeft geld" (bezit-betekenis)

### 9.3 [ONTBREEKT] §9.1.8 `i` (datief) — double-marking is de standaard

Uitleg geeft één voorbeeld zonder uitleg over double-marking: *"`yews-as-t̲ i Mimun` 'hij gaf het hem (aan Mimoun)'"*. Maar de truc hier — dat de IO-clitic `as-` **dezelfde** persoon als `i Mimun` aanduidt — wordt niet expliciet gemaakt. Boek p84 zegt dat dit **regelmatig** is: *"Often the phrase i + noun/free pronoun is doubled by an Indirect object pronoun."*

**Voorstel**: in uitleg toevoegen: *"In Tarifit is het normaal dat de datief-IO twee keer wordt uitgedrukt — één keer als clitic op het werkwoord (`as-`), één keer met `i + NP` daarna. Dit is geen redundantie maar de standaardconstructie."*

### 9.4 [ONTBREEKT] §9.1.8 `umi` als datief-alternatief

Boek p85: *"In phrases where one would expect the preposition standing alone, the element `umi` is used."* Voorbeeld uit boek: `ḏyenni umi yenya ussen` "die mensen voor wie hij de jakhals had gedood".

`umi` staat in CSV ("aan wie"). Wordt vooral gebruikt in relatieve bijzinnen en met vraagwoorden. Komt in h15 wel terug, maar in h9 zou een korte vermelding helpen.

### 9.5 [SPELLING] §9.2 `azemmaḏ` is fout — moet `ajemmaḏ`

Uitleg-tabel: `azemmaḏ i / n` "aan de andere kant van". CSV heeft `ajemmaḍ` "tegenoverliggende kant" — met `j` (niet `z`) en `ḍ` (niet `ḏ`). Boek-OCR heeft `azemmaḏ` (waarschijnlijk OCR voor `aǧemmaḍ` — `ǧ` wordt `z` of `g` in OCR). 

CSV is leidend: `ajemmaḏ` of `ajemmaḍ`.

### 9.6 [ONTBREEKT] §9.2 mist twee samengestelde voorzetsels uit boek

Boek p87 (TOC §9.2-lijst) noemt zeven samengestelde voorzetsels. Uitleg geeft er zeven, maar de samenstelling klopt niet helemaal. Twee uit boek die in uitleg ontbreken:
- `awriḏ i / n` "naar (hierheen)" — gerelateerd aan CSV-bijwoord `awrud` "hierheen"
- `ayirin i / n` "naar (daarheen)" — CSV-bijwoord `ayirin` "daarheen"

Beide zijn directionele samengestelde voorzetsels, complementair aan `qibaṛi` ("vóór") en `awaṛn` ("achter"). Voor wie ergens "heen" wil aangeven, ontbreekt nu de constructie.

### 9.7 [SPELLING] §9.1.6 voorbeeld `kim`

In de uitleg-tabel staat onder `aked`: vorm voor voornaamwoord `kid- ~ akid-`. Voorbeeld in tekst: *"`kiḏem ~ kim` 'met jou (V)'"*. `kim` als verkorte vorm staat in boek p67 (5.2.5-tabel) als alternatief van `kiḏem` voor 2SG:F. CSV heeft niet `kim` als losse entry, maar wel `aked` en `akiḏ`. OK qua structuur.

### 9.8 [STIJL] §9 — emoji's en "✅ gecontroleerd"

Idem.

---

## Hoofdstuk 10 — Telwoorden en hoeveelheden

**Boek p. 97–102 (Quantifiers).** Uitleg-sectie `#h11`.

### 10.1 [SPELLING-CLUSTER] §10.1 — systematisch missende `ɛ` en `ḇ`

Een opvallend cluster van mismatches met de CSV. De vier-, zeven- en tien-getallen plus tientallen missen consequent diakritische tekens:

| Cijfer | Uitleg | CSV | Wat ontbreekt |
|---|---|---|---|
| 4 | `aabɛa` | `aaḇɛa` | `ḇ` (zachte b) |
| 7 | `sebɛa` | `seḇɛa` | `ḇ` |
| 10 | `ɛecra` | `ɛecṛa` | `ṛ` (donkere r) |
| 40 | `aabein` | `aaḇɛin` | `ḇ` én `ɛ` |
| 70 | `sebein` | `seḇɛin` | `ḇ` én `ɛ` |
| 90 | `t̲esein` | `tesɛin` | `ɛ` (en `t` ipv `t̲`) |

Boek-OCR heeft de `ɛ` ook lastig (komt vaak als `e` of `c` over) — maar CSV is leidend en heeft consequent `ɛ`. Bij herschrijven systematisch corrigeren.

### 10.2 [FOUT] §10.2 voorbeeld `cmeɛ`

Uitleg: *"`cmeɛ marra arrud nnem` 'verzamel al je kleren!'"*. 

Boek p93 originele zin: `jmeɛ marra arrud-nnem` (OCR `zmee marra arrud mem`). CSV heeft `jmeɛ` "verzamelen" — niet `cmeɛ`. **`cmeɛ` is een typo voor `jmeɛ`** (de `j` is de "zachte j" van Frans `déjà`).

CSV heeft `cmes` voor "verpakken, inpakken" en `cnef` voor "roosteren" — maar niet `cmeɛ`. De uitleg verwart vermoedelijk twee werkwoorden.

### 10.3 [FOUT] §10.2 voorbeeld `kuř aɛecci`

Uitleg: *"`kuř aɛecci` 'elke avond'"*. Wacht, ik zie in de uitleg-tekst staan: *"kuř aeessi"* — de uitleg gebruikt `aeessi` zonder `ɛ`. CSV heeft `aɛecci` "namiddag". Dus moet `aɛecci` worden, met `ɛ`.

### 10.4 [ONDUIDELIJK] §10.1 — `ict̲en` als zelfstandige V-vorm

Uitleg geeft `ict̲en` voor "één vrouw" (zelfstandig). CSV heeft alleen `ict̲` — als pre-nominale vorm voor V-naamwoorden. Boek p89 (in tabel) heeft `iken` of `ist̲en` (OCR onduidelijk). 

Welke vorm correct is, is onduidelijk: `ict̲en`, `ist̲en` of `iken`. Mogelijk variatie. **Voorstel**: bij herschrijven vragen aan een native speaker, of vasthouden aan de CSV-vorm `ict̲` (alleen pre-nominal) en geen zelfstandige V-vorm tonen totdat verifieerbaar.

### 10.5 [ONDUIDELIJK] §10.2 `ca` heeft twee functies

Uitleg-tabel onder "Veel / weinig / iets" geeft `ca` "iets" met voorbeeld `ca n waman` "wat water". Maar `ca` is in CSV gedefinieerd als "post-verbaal ontkennings-partikel" (niet als kwantor).

In feite heeft `ca` twee functies:
- **post-verbal ontkenningspartikel**: `waa ssiney ca` "ik weet niet"
- **indefinite kwantor**: `ca n waman` "wat water" (in boek p89 als `sa n waman`)

De CSV vermeldt alleen de eerste functie. Voor de uitleg zou een korte noot moeten staan: *"`ca` werkt als ontkennings-partikel (zie h13) én als indefinite kwantor (`ca n X` 'wat/iets X')"*. Anders denkt de leerling dat het hetzelfde woord is met één betekenis.

### 10.6 [SPELLING] §10.2 `mma` "wie/waar dan ook"

Uitleg: *"`mani mma t̲exseḏ` 'waar je maar wilt'"* met `mma` als universele "ook"-marker.

Boek p93 voetnoot: *"the adverb has the form `manat̲`, e.g. `sa n marraṭ` 'some times'"*. Dat is een ander verschijnsel. Voor "wie/waar dan ook" gebruikt boek p93 `manat̲`, niet `mma`. CSV heeft `marra` "alle". 

Mogelijk is `mma` een verkorte spreektaalvorm. Maar CSV/boek hebben dit niet bevestigd. Bij herschrijven verifiëren.

### 10.7 [ONTBREEKT] §10.1 — adverbiale telwoorden

Boek p91–92 heeft een hele paragraaf over **adverbiale telwoorden** voor tijdsuitdrukkingen — speciale vormen die alleen voorkomen bij "jaren", "maanden", "dagen", "keer":
- `eam` "één jaar", `eamayen` "twee jaar" (Arabische dualis), `t̲eřt̲ snin` "drie jaar"
- `cḥaa` "één maand", `sehrayen` "twee maanden", `t̲řata cuhuṛ` "drie maanden"
- `nnhaa` "één dag", `yumayen` "twee dagen", `t̲řata iyyam` "drie dagen"
- `t̲waṛa` "één keer", `maaṛatayen` "twee keer", `t̲řata imuṛan` "drie keer"

Uitleg noemt alleen `ɛamayen` (Arabische dualis) als alternatief voor "twee" zonder uitleg. De hele systematiek van adverbiale tellen-vormen ontbreekt — terwijl je dit nodig hebt zodra je tijd-uitdrukkingen gaat maken.

### 10.8 [STIJL] §10 — emoji's en "✅ gecontroleerd"

Idem.

---

---

## Hoofdstuk 11 — De naamwoordgroep

**Boek p. 103–105 (The Noun Phrase).** Uitleg-sectie `#h12`.

Een korte sectie die grotendeels in orde is. Vooral spelling-issues.

### 11.1 [SPELLING] §11.2 — `jjdid` → `jjḏiḏ`

Uitleg gebruikt `jjdid` "nieuw" als voorbeeld van een invariant bijvoeglijk naamwoord. CSV heeft `jjḏiḏ` met **twee** zachte `ḏ`'s. Uitleg mist beide spirantiseringen.

### 11.2 [SPELLING] §11.2 — `gama` → `qama`

Uitleg's voorbeeld `gama n jjdid` "het nieuwe bed". CSV heeft `qama` "bed" — met `q` (diepe k), niet `g`. **Echte fout** — `qama` en `gama` zijn fonetisch verschillende klanken.

### 11.3 [GOED] §11.2 Free-State-regel voor bijvoeglijk

De regel *"Bijvoeglijke naamwoorden staan altijd in Free State, ook als het naamwoord in Annexed State staat"* klopt met boek (§3.1.4 / p36). Voorbeeld `n waayaz ameqqṛan` is correct geanalyseerd.

### 11.4 [ONDUIDELIJK] §11.1 NP-volgorde-formule incompleet

De formule *"[Onbepaald] [Hoeveelheid] (n) [Naamwoord]-[bezit-suffix]-[deze/die] [Bijvoeglijk] [n + bezit-NP] [marra]"* staat netjes, maar mist:
- positie van **clitica** rond bijvoeglijk naamwoord
- positie van predicatief **`d`** in non-verbal predicaten (relevant voor h13 §13.4)

Voor cursus is de formule oké, voor uitleg een beetje schraal.

### 11.5 [STIJL] §11 — emoji's en "✅ gecontroleerd"

Idem als andere hoofdstukken.

---

## Hoofdstuk 12 — Vragen stellen

**Boek p. 107–109 (Interrogation, vier subsecties).** Uitleg-sectie `#h13`.

Dit hoofdstuk heeft **twee complete gaten**: de boek-paragrafen §12.3 en §12.4 ontbreken volledig in de uitleg.

### 12.1 [GROOT GAT] §12 mist boek §12.3 — vraagwoorden over naamwoorden

Boek §12.3 (p109) gaat over de constructie *"welke X?"* / *"wat voor X?"*. Tarifit gebruikt hiervoor:
- `man wen` (M) / `man t̲en` (V) — "welke (van die)"
- `man yin` (M:PL) / `man t̲in` (V:PL) — "welke (van die mannen/vrouwen)"
- `mana`, `manawy-`, `manay-` — "welk (algemeen)"

Voorbeeld uit boek: `mana ttumubin t̲awyeḏ?` "welke auto heb je gepakt?". CSV heeft `man`, `mana`, `manawy-`, `manay-` allemaal als entries. Uitleg behandelt deze niet — een leerling die "welke" wil zeggen heeft hier dus geen aanknopingspunt.

### 12.2 [GROOT GAT] §12 mist boek §12.4 — vraagwoorden als voegwoorden

Boek §12.4 (p109): vraagwoorden kunnen ook gebruikt worden als **subordinators** in indirecte vragen. Voorbeeld:
- `waa ssiney mani t̲eqqim` "ik weet niet waar ze is gebleven"
- `waa ssiney meřmi t̲awḏ` "ik weet niet wanneer ze aankomt"

Bij negatieve hoofdzin met `waa-ssi` ("ik weet niet") werkt dit anders dan bij positieve hoofdzin (`yessen`) — daar gebruik je `illa`/`belli` (zie h16). Dit hele onderscheid ontbreekt.

### 12.3 [ONTBREEKT] §12.2 — vraagwoord-vragen zijn cleft-zinnen

Boek p107: vraagwoord-vragen worden behandeld als een speciaal type cleft-zin. Dat heeft drie gevolgen die in uitleg niet expliciet staan:
1. **Clitic-fronting is verplicht** na het vraagwoord
2. **`ya` wordt gebruikt ipv `ad`** (zie h7 §7.3)
3. **Geen `i`** als relatieve marker (in tegenstelling tot gewone clefts)

Voorbeeld van wat een leerling moet weten: *"wat zal je doen?"* = `min ya t̲eggeḏ?`, niet `*min t̲a t̲eggeḏ?`. De uitleg behandelt dit gedeeltelijk in h15 §15.4 maar zou hier al moeten worden geïntroduceerd.

### 12.4 [ONDUIDELIJK] §12.2 — `wi ~ u` voor "wie"

Uitleg geeft *"`wi ~ u`"* als varianten voor "wie". CSV heeft alleen `wi` "wie". Boek p107: alleen `wi`. De `u` als variant is niet gedocumenteerd in CSV of OCR-tekst — vermoedelijk een typo of misinterpretatie. **Voorstel**: `u` weghalen.

### 12.5 [SPELLING] §12.2 voorbeeld `mayemmi t̲et̲rud?`

`t̲et̲rud` is van `ru` "huilen" (CSV) — 2SG-Imperfectief vorm. De spelling oogt OK qua patroon. Boek-OCR niet hard te verifiëren.

### 12.6 [STIJL] §12 — idem

---

## Hoofdstuk 14 — Zinsbouw

**Boek p. 129–134 (Sentence structure).** Uitleg-sectie `#h15`.

Deze sectie is **goed**, met een paar uitbreidings-mogelijkheden.

### 14.1 [GOED] VSO-classificatie

De uitspraak *"Tarifit is een VSO-taal"* klopt met boek p129. Het basisvoorbeeld `qa yewca baba t̲t̲menyat̲ i Mimun` met de gloss is duidelijk en correct.

### 14.2 [ONTBREEKT] §14.2 mist onderscheid topicalisatie vs. focalisatie

Boek p131–132 maakt expliciet onderscheid tussen:
- **Topicalisatie** (uitleg §14.2): element vooraan + voornaamwoord-anafoor in zin, FS-vorm
- **Focalisatie / cleft** (boek §14.4): element vooraan met `d` ervoor + relatieve bijzin, syntactisch een eigen constructie

De uitleg behandelt cleft-zinnen wel, maar pas in h15 §15.3 — niet in h14 waar boek het zou plaatsen. Het zou helpen om in §14.2 een korte introductie van cleft als focalisatie-strategie te geven, met cross-link naar §15.3.

### 14.3 [SPELLING/ONDUIDELIJK] §14.3 — `uyi-ya` "deze melk"

Uitleg geeft `d asemmam, uyi-ya` "het is zuur, deze melk". CSV heeft `ayi` "melk" — niet `uyi`. De `uyi`-vorm in de uitleg is de **Annexed State** van `ayi` (`a` → `u` na voorzetsel of in post-topic-positie). Maar de uitleg legt dit niet uit — een leerling ziet `uyi-ya` ineens en weet niet of dat een ander woord is.

**Voorstel**: gloss-noot toevoegen: *"`uyi` is de AS-vorm van `ayi` 'melk' — naamwoorden in post-topic-positie staan in AS (zie h3 §3.4)"*.

### 14.4 [GOED] §14.2 voorbeelden

De vier topicalisatie-voorbeelden (`necc / landris inu / Fatima / nhar-a` als topic) zijn prima en illustreren goed dat verschillende elementen vooraan kunnen.

### 14.5 [STIJL] §14 — emoji's `🚨 ⭐ 🇳🇱` plus "✅ gecontroleerd". Idem.

---

## Hoofdstuk 15 — Betrekkelijke bijzinnen

**Boek p. 135–138 (Relative clauses and related constructions).** Uitleg-sectie `#h16`.

### 15.1 [INCOMPLEET] §15.2 — vier kenmerken zou er **vijf** moeten zijn

Uitleg geeft vier kenmerken voor bepaalde betrekkelijke bijzinnen:
1. Geen voornaamwoord dat verwijst naar het hoofd
2. Bij onderwerps-bijzinnen: participium-vorm
3. Clitic fronting
4. `ad` wordt `ya`

Boek p123 expliciet noemt **vijf** kenmerken — kenmerk 5 mist:
- 5. **In voorzetsel-bijzinnen staat het voorzetsel (zonder voornaamwoord-suffix) direct achter de relatieve marker `i`**, in zijn "isolated form" (zie h9 §9.1).

Voorbeeld uit boek: `missa i x ssaasey řkas-nni` "de tafel waar ik dat glas op heb gezet". Hier staat `x` direct na `i` (relatieve marker), zonder pronominaal suffix. Dat is een bijzondere syntactische regel die in uitleg ontbreekt.

### 15.2 [SPELLING] §15.2 voorbeelden — `dja` versus `ǧa`

Uitleg's voorbeeld bij voorzetsel-bijzin: *"`t̲aḥenjiat̲ [i yaa dja umeddukeř]` 'een meisje dat een vriendje heeft'"*. Het woord `dja` zou `ǧa` moeten zijn (Perfectief van `iři` "zijn") in CSV-conventie. Boek-OCR schrijft `dza` (`dz` is OCR-rendering van precomposed `ǧ`). 

CSV heeft `iři` als basis maar niet `ǧa` als losse Perfectief-vorm (geconjugeerd vorm staat niet in CSV). Boek noemt `yedzan` (`yeǧan`) als regulier Perfectief. Dus `dja` in uitleg = `ǧa` in boek-conventie. Inconsistent met h2 §2.5 die `ǧ`-notatie voorschreef.

### 15.3 [ONDUIDELIJK] §15.2 voorbeeld `wenni [ixeddmen řebda] ad yedweř d t̲ayaa`

`t̲ayaa` "rijk" — CSV heeft niet `t̲ayaa` als losse vorm. Boek-OCR (p124) schrijft `tazqq`, wat OCR is voor `t̲aẓqqʷa` of vergelijkbaar. Niet duidelijk welke vorm correct is.

CSV heeft `řweqqaḏ` of `řbu`-stam-werkwoorden voor "rijk" niet expliciet. Wel `aṛṛzeq` "(financieel) fortuin". Maar `t̲ayaa` als adjectief "rijk" is niet in CSV te vinden. Mogelijk een verzonnen of dialectaal-specifieke vorm.

**Voorstel**: bij herschrijven verifiëren met native speaker, of voorbeeld vervangen door geverifieerde adjectief-constructie.

### 15.4 [GOED] §15.3 cleft-zinnen + §15.4 vraagwoord-vragen

Beide secties zijn correct en consistent met boek p125. Het tweetal-onderscheid (cleft heeft `d` + `i`; vraagwoord-vragen hebben **geen** `d` en **geen** `i`) is duidelijk gemaakt. Voorbeelden kloppen.

### 15.5 [STIJL] §15 — idem

---

---

## Hoofdstuk 16 — Hulpwerkwoorden

**Boek p. 139–140 (Operator verbs and complementizers).** Uitleg-sectie `#h17`.

### 16.1 [GOED] §16.1 hoofdregel

De kern *"Tarifit gebruikt twee volledige vervoegde werkwoorden naast elkaar"* is correct en sluit aan op boek p126 (let op: in het boek staat dit bij §16, niet p139 zoals uitleg meldt — kleine onnauwkeurigheid in pagina-referentie). Voorbeeld `xsey ad meřcey` met letterlijke gloss "ik wil ik zal trouwen" is helder.

### 16.2 [SPELLING] §16.1 voorbeelden

| Uitleg | CSV | Probleem |
|---|---|---|
| `bda` "beginnen" | `bḏa` | mist `ḏ` (zachte d) |
| `xs` "willen" | `xs` ✓ | OK |
| `mřec` "trouwen" | `mřec` ✓ | OK |

### 16.3 [ONTBREEKT] §16.1 — "be"/"become"-werkwoorden als operator-categorie

Boek p126 zegt expliciet: *"'Be' and 'become'-verbs are followed by a full stative predicate, mostly (but not necessarily) a non-verbal clause."* Uitleg behandelt `dweř` "worden" wel apart, maar plaatst het niet in de bredere **categorie** "be/become-operator-werkwoorden". Daardoor is het verband met h13 §13.4 (zijn-constructies) niet expliciet.

### 16.4 [ONTBREEKT] §16.2 — `waa-ssi` als verkorte vorm

Boek p127: *"With the lexicalized clipped version `waa-ssi`, it is possible to do without a complementizer, e.g. `waa-ssi a d-yas niy lla` 'ik weet niet of hij komt of niet'."* CSV heeft `waa-ssi` als losse expressie ("ik weet niet"). Praktisch, dagelijks gebruik — ontbreekt volledig in uitleg.

### 16.5 [ONTBREEKT] §16.2 — `ssen` als operator vs. complementizer

Boek p127: het werkwoord `ssen` "weten" kan in twee constructies voorkomen:
- **Operator** (zonder `illa`/`belli`): `yessen ad yessiwer` "hij weet hoe te spreken"
- **Complementizer** (met `illa`/`belli`): `yessen illa ad ariy` "hij weet dat ik zal schrijven"

Uitleg geeft alleen het tweede. Het verschil "weten hoe" vs. "weten dat" is praktisch nuttig — ontbreekt.

### 16.6 [STIJL] §16 — idem

---

## Hoofdstuk 17 — Voegwoorden

**Boek p. 141–146 (Coordination and subordination).** Uitleg-sectie `#h18`.

### 17.1 [GOED] §17.1 algemene regels

De `d` "en" alleen voor NP-coordinatie, niet zinnen — klopt met boek p128. De `řa ... řa` "noch ... noch"-constructie is correct (CSV: `ra... ra` "noch... noch"). De waarschuwing dat `d` niet voor zinnen werkt is precies de soort fout-preventie die je wilt.

### 17.2 [SPELLING] §17.2 — `mara` → `mařa`, `meelik` → `meɛlik`

| Uitleg | CSV | Probleem |
|---|---|---|
| `mara` "als (hypothetisch)" | `mařa` | mist `ř` |
| `meelik` "als (counterfactueel)" | `meɛlik` | mist `ɛ` (ayin) |
| `mři` "als (counterfactueel)" | `mři` ✓ | OK |
| `umi` "toen" | `umi` ✓ | OK |
| `ṛami` "wanneer" | `ṛami` ✓ | OK |
| `xmi`, `xemmi` | `xmi`, `xemmi` ✓ | OK |
| `puřki` "omdat" | `puřki` ✓ | OK |
| `aṛ` "tot" | `aṛ` ✓ | OK |
| `qbeř` "voordat" | `qbeř` ✓ | OK |

`meelik` is dezelfde fout als h7 issue 7.3.

### 17.3 [FOUT] §17.2 voorbeeld `umi t̲-yenya, t̲ḥedd`

Uitleg: *"`umi t̲-yenya, t̲ḥedd` 'toen hij hem gedood had, stond ze op'"*. Boek p129 heeft de zin als `umi t̲-yenya, tbedd` — `tbedd` (3SG:F Perfectief van `bedd` "opstaan", CSV: `beḏḏ`).

`t̲ḥedd` in uitleg is een **typo**: de `ḥ` is verkeerd. Moet `t̲beḏḏ` of `tbedd` zijn (afhankelijk van spirantisering-keuze). De `ḥ` is mogelijk verward met de naam-prefix `ḥ-` of een verkeerd OCR.

### 17.4 [GROOT GAT] §17.2 — clitic-fronting/ya regels per voegwoord ontbreken

Boek p131–132 maakt expliciet voor elk voegwoord onderscheid:
- **Causes clitic-fronting + `ya`**: `umi`, `ṛami`, `xmi`, `xemmi`, `amen`, `qbeř`, `aṛ` (in temporeel gebruik)
- **Causes geen fronting, `ad` blijft `ad`**: `ḥama`, `ḥuma`, `puřki`, `lianna`, `daxataṛ`, `min-zi`, `henda`, `baš`

Dit is **leerbare** informatie — bepaalt of je `min ya t̲eggeḏ` of `min ad t̲eggeḏ` zegt na het voegwoord. Uitleg behandelt clitic-fronting in §7.3 in algemene termen, maar de **specifieke** regel per voegwoord komt nergens terug.

### 17.5 [ONDUIDELIJK] §17.2 voorbeeld `mři ḏ-usiy ifi cciy`

`ifi` "zou hebben" wordt gebruikt zonder uitleg. Boek p105: dit is een specifieke counterfactueel-vorm — bij `mři` of `meɛlik` (counterfactueel) wordt de uitkomstzin met de **Perfectief** uitgedrukt waar Nederlands "zou ... hebben" gebruikt. Voorbeeld uit boek: `mři teɣrid ifi t̲ufiḏ řxedmet̲ t̲esbeh` "als je had gestudeerd, zou je een goede baan hebben gevonden".

`ifi` zelf staat niet in CSV als losse vorm — het is een onregelmatig partikel-achtig element. **Voorstel**: kort uitleggen dat `ifi` de typische "zou (hebben)"-marker is in counterfactuele zinnen. Anders blijft het voor de leerling ondoordringbaar.

### 17.6 [ONTBREEKT] §17.2 — `ɛlaxaṭaṛ` (omdat) ontbreekt

CSV heeft `ɛlaxaṭaṛ` "omdat" als veelgebruikt voegwoord. Uitleg's tabel noemt alleen `puřki` en `lianna`. `ɛlaxaṭaṛ` is in alledaagse Tarifit minstens zo gebruikelijk als de andere twee.

### 17.7 [STIJL] §17 — idem

---

## Hoofdstuk 18 — Voorbeeldteksten en dialogen

**Boek p. 147–188 (Texts).** Uitleg-sectie `#h19`.

Dit is **bewust kort gehouden** in uitleg — slechts een lijst van wat in het boek staat plus 5 zinnen. Dat is een ontwerpkeuze: de teksten zijn meer leesmateriaal dan grammatica-stof.

### 18.1 [DOELLOOSHEID] §18 — wat moet de leerling hiermee?

Uitleg geeft een lijst (18.1–18.5) en een paar voorbeeld-zinnen, zonder leerdoel. Voorstel bij herschrijven:
- Per tekst aangeven *waarom* die geschikt is (bv. "18.1 toont topicalisatie en relatieve bijzinnen in actie", "18.5 begroetingen leveren standaard-zinnen voor dagelijks gebruik")
- Maximaal 5 dialoog-zinnen uit boek §18.5 met gloss en uitleg

### 18.2 [SPELLING] §18 voorbeelden

| Uitleg | Boek/CSV | Probleem |
|---|---|---|
| `aqq-ec mliḥ?` "ben je goed?" | klopt | OK |
| `yekkaa ijj uzedjid` "er was eens een koning" | `ijj wajeǧiḏ` (correct AS) | uitleg `uzedjid` heeft `dj` ipv `ǧ`, en de `u-` ipv `w-` als AS-prefix is informeler. CSV-conventie zou `wajeǧiḏ` zijn |
| `yaas ijjen yiyyaa n yaaḏen yemyaa` | `yaas ijjen yiyyaa n yaaḏen yemɣaa` (?) | `yemyaa` "het is groot/groeit" — CSV heeft `myaa` "groeien", maar 3SG:M Perfectief zou `yemɣaa` zijn (zonder z'n verandering). Uitleg gebruikt `yaa` ipv `ɣaa`. Spelling-mismatch. |

### 18.3 [ONTBREEKT] §18 — geen gloss bij voorbeelden

De voorbeeldzinnen worden zonder ontleding gepresenteerd. Een leerling kan niet uitvogelen welke morfemen welke functie hebben — terwijl boek h18 juist uitvoerig glosst per regel. Een korte gloss-lijn onder elk voorbeeld zou enorm helpen.

### 18.4 [STIJL] §18 — idem (`✅ gecontroleerd` is hier extra ironisch want het hoofdstuk is grotendeels niet inhoudelijk gereviewd)

---

## Eindsamenvatting (sectie `#h20`)

### S.1 [GOED] De 10 belangrijkste concepten

De lijst van 10 punten is een nuttige cheat-sheet. Inhoudelijk klopt vrijwel alles:
- Klinkers (3 + schwa) ✓
- Drie R's ✓
- Drie noun-klassen ✓
- Geslacht via `t̲a-...-t̲` ✓
- Free/Annexed State (met de regel "na werkwoord/voorzetsel → AS, behalve `aṛ`/`břa`") ✓ — maar `amecnaw` mist in de uitzonderingen-lijst (zelfde als h9 issue 9.1)
- 5 werkwoordsvormen ✓
- Aspect i.p.v. tijd ✓
- VSO-volgorde ✓
- Voornaamwoord-volgorde IO–DO–ḏ ✓
- Preverbale partikels (`ad`/`qa`/`t̲uya`/`waa`) — `xad` mist, maar voor samenvatting acceptabel

### S.2 [INCOMPLEET] punt 9 mist voorzetsel-suffix

Punt 9 *"Voornaamwoorden plakken vast: aan werkwoord, voorzetsel of familiewoord. Volgorde: IO – DO – ḏ"* is onvolledig — de **suffixen op voorzetsels zelf** (zoals `kiḏes` "met hem", `xafi` "op mij", `nnes` "van hem") vormen een eigen set die niet in de IO–DO–ḏ-volgorde past. Dat zijn losse pronominale suffixen, behandeld in h5 §5.2.5.

**Voorstel**: punt 9 splitsen in twee delen — (a) verbale clitica met IO–DO–ḏ-volgorde, (b) pronominale suffixen op voorzetsels en familiewoorden.

### S.3 [STIJL] — `🎓` `🎯` `🛑` emoji's

Eindsamenvatting opent met `🎓`, alle vijf cursus-tips beginnen met `🎯`, sluit af met `🛑 EINDE VAN ALLE HOOFDSTUKKEN`. Idem als rest.

---

## Algemene observatie aan het einde

Na alle 18 hoofdstukken plus eindsamenvatting komt het volgende patroon herhaaldelijk terug:

1. **Stijl-issues zijn overal hetzelfde** — emoji's, "✅ gecontroleerd"-claims, AI-clichés. Bij het herschrijven kan dit in één pass voor alle hoofdstukken tegelijk worden weggehaald.
2. **CSV-spelling-mismatches** zijn systematisch — vooral missende `ḏ`/`ḇ`/`ɛ`/`ṛ` waar CSV ze wel heeft. De volledige lijst staat in [woord-audit.md](woord-audit.md).
3. **Drie hoofdstukken hebben grote inhoudelijke gaten** die meer dan spelling vergen:
   - **h12** (Vragen): boek-secties §12.3 (welke X?) en §12.4 (vraagwoorden als voegwoorden) ontbreken volledig
   - **h13** (Aspect/ontkenning): twee complete "zijn"-constructies missen (`wi yifan` voor possessieve vragen, `gg` voor similatief), plus drie syntactische regels rond `bu`
   - **h17** (Voegwoorden): per-voegwoord regels over clitic-fronting en `ya`/`ad`-keuze ontbreken
4. **Drie inconsistenties zitten verspreid over meerdere hoofdstukken**:
   - `dj` vs `ǧ`-notatie (h2, h13, h15, h18) — kies één
   - `qa`/`tuya` worden 3× behandeld (h4, h8, h13) — moet 1× in h8
   - `xad` als "sterker dan ad" (h4, h7) — boek beschrijft het als modaal-variant, niet temporele gradatie
5. **Eén hele paragraaf-cluster ontbreekt**: boek §5.3 over emphasizers (`nnit̲`, `simant̲`).

---

## Status: review compleet

| Hoofdstuk | Status |
|---|---|
| h1–h18 + eindsamenvatting | ✓ allemaal gereviewd |
| Woord-audit (CSV-cross-check) | ✓ in [woord-audit.md](woord-audit.md) |

De review-fase (Fase 3) is klaar. Volgende stap is **Fase 4** — herschrijven van `uitleg.html` op basis van deze review. Mijn voorgestelde aanpak:

- **Batch 1**: h1 + h2 (klanken + algemene introductie) — visueel ook waarbij stijl-overhead wordt vastgelegd voor de rest
- **Batch 2**: h3 + h4 (naamwoorden + werkwoorden — kern)
- **Batch 3**: h5 + h6 + h7 (voornaamwoorden + clitica)
- **Batch 4**: h8 + h13 samen (alle pseudo-werkwoorden + aspect — moet samen om de dubbeling op te lossen)
- **Batch 5**: h9 + h10 (voorzetsels + telwoorden)
- **Batch 6**: h11 + h12 + h14 + h15 (syntaxis)
- **Batch 7**: h16 + h17 + h18 + eindsamenvatting (slot)

Ik stop hier. Geef "ga door" als je akkoord bent met de hele review en de batch-aanpak voor Fase 4 — dan begin ik met Batch 1 van het herschrijven. Of laat weten als je eerst nog dingen wilt aanpassen aan de review zelf.
