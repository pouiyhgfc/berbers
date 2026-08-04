# BOUWPLAN-CURSUS-UITVOERING.md — spec voor Claude Code (Sonnet)

Dit is de uitvoeringsversie van `BOUWPLAN-CURSUS-V2.md`. V2 legt uit *waarom*; dit document legt
*exact* vast wat er gebouwd wordt, zodat er niets te beslissen of te raden valt. Bij twijfel wint
dit document.

**Wijzigingen t.o.v. V2** (bewust, om foutloos bouwen mogelijk te maken):
1. Oud-les 06+07 (vervoeging ev/mv) samengevoegd → **38 lessen**; nummers na 06 schuiven −1.
   Reden: splitsen van de 22 vervoegingszinnen zou een handmatige selectie vergen.
2. `boek:`-veld vervalt: boekpagina's worden **afgeleid** uit de zin-ids (`id:p101-03` → p.101).
3. Manifests gebruiken alleen **2-niveau §-ankers** (`s13-4`, nooit `s5-2-6`).
4. Fase 0-besluiten blokkeren niet meer: spelling-check start in waarschuwmodus, les 01 en 37
   krijgen bewerkbare selectie/bereik-bestanden met een deterministische default.

---

## 0. IJzeren regels (gelden in elke fase)

- **R1** Wijzig NOOIT een Tarifit-string. Niet in CSV's, niet in HTML, niet in JSON. Scripts
  kopiëren Tarifit alleen. Elke diff die een bestaande Tarifit-string verandert = fout.
- **R2** Verzin NOOIT een zin, woord of vertaling. Alle inhoud komt uit `zinnen.csv`,
  `woordenlijst.csv` of `uitleg.html`.
- **R3** Elke validator faalt **hard** (exit 1) met een lijst van concrete vindplaatsen; nooit
  stil doorbouwen.
- **R4** Alle paden relatief aan de repowortel. Python 3, alleen standaardbibliotheek.
- **R5** Bestaande bestanden buiten de hieronder genoemde worden niet aangeraakt.
- **R6** CSV lezen altijd met `encoding='utf-8-sig'` (BOM in woordenlijst), schrijven met
  `utf-8`, `csv.QUOTE_ALL`.

## 1. Vereisten vooraf

1. `assets/woordenlijst/woordenlijst.csv` heeft na de classificatie-merge exact deze header:
   `"tarifit","nl","en","cefr","woordsoort","thema","tags"`.
   Fase 1 bevat het merge-script (`promoot_classificatie.py`) dat
   `woordenlijst-geclassificeerd.csv` (staat in de repo-map `bron/aanlevering/`) hierin omzet:
   `cefr_nieuw`→`cefr`, `thema` blijft, `tags_nieuw`→`tags`, kolommen `cefr_oud`/`zekerheid`
   vervallen, koprij-als-data op de oude regel 1787 wordt niet meegenomen. Rijvolgorde behouden.
2. `zinnen.csv` header (bestaand, niet wijzigen): `tarifit,nl,en,gloss,hoofdstuk,les,bron,tags`.
   In `tags` staan `id:pNNN-NN` (1.208/1.208 uniek, gecontroleerd) en `context:<sectie>`.
3. `assets/oefeningen/exercises-nl.json` bestaand schema: object met keys `les-NN`, waarde =
   lijst van oefeningen `{"type":"mc","q":str,"options":[str],"correct":int,"explain":str}`;
   HTML toegestaan in `q`/`explain`; Tarifit altijd in `<span class="tar">…</span>`.

## 2. Mappen en nieuwe bestanden

```
bron/
  lessen/            01-begroeten.md … 38-izran.md   (manifest + NL-tekst)
  lessen/en/         01.md … 38.md                    (alleen vertaalde tekst; fase 7)
  kaarten/           alfabet.md, getallen.md, glossen.md
  selecties/         les-01-begroetingen.txt          (één zin-id per regel)
  besluiten/         les-37-sprookje.txt              (regel 1: "paginabereik 134 141")
  morfemen.csv       kolommen: vorm,soort,boekpagina  (start: zie §4.6)
  register-spelling.csv                                (optioneel; ontbreken = waarschuwmodus)
  aanlevering/woordenlijst-geclassificeerd.csv
  sjablonen/pagina-nl.html, pagina-en.html
_project/scripts/
  promoot_classificatie.py  gen_ankers.py  bouw_cursus.py
  check_bronnen.py  check_register.py  check_dekking.py
nl/blok-1.html … blok-8.html   nl/lezen.html   (gegenereerd)
en/blok-1.html … blok-8.html   en/lezen.html   (gegenereerd, fase 7)
```

`nl/cursus.html` wordt in fase 8 vervangen door een gegenereerd overzicht; tot die tijd blijft
hij staan.

## 3. Het lesbestand — exact formaat

```markdown
---
id: 08
slug: ad-toekomst
blok: 2
titel: "Toekomst en wens — ad + aorist"
doel: "Zeggen wat je gaat doen of wat je wilt dat gebeurt."
grammatica: [s7-1]
zinnen:
  - context: "the-aorist"
  - context: "modal-preverbal-clitics"
kernwoorden: auto
status: af
---
<!-- TEKST VOLGT — schrijffase -->

{{zinnen}}
{{kernwoorden}}
{{oefeningen}}
```

Regels:
- `id` = tweecijferig, gelijk aan bestandsnaamprefix. `status` ∈ {af, concept, dun}.
- `zinnen:`-items zijn óf `context: "<exacte string>"` óf `selectie: "bron/selecties/<file>"`
  óf `ids: [pNNN-NN, …]`. Contextstrings letterlijk uit §5 kopiëren (aanhalingstekens,
  apostrofs, tildes, dubbele punten zijn onderdeel van de string).
- `kernwoorden:` = `auto` of expliciete lijst van tarifit-lemma's die in de woordenlijst staan.
- Body: vrije Markdown + de drie placeholders (elk exact één keer, in deze volgorde toegestaan
  maar niet verplicht qua positie) + optionele blokken `::: verdieping "Titel"` … `:::`.
- YAML-parsing: eenvoudige eigen parser volstaat (key: value, lijsten met `-`); geen
  YAML-dependency toevoegen.

Kaartbestanden (`bron/kaarten/*.md`): zelfde vorm, zonder `blok`/`doel`, met `type: kaart`;
zinnen-eis geldt niet.

## 4. Deterministische regels

**4.1 §-ankers (gen_ankers.py).** In `nl/uitleg.html` en `en/grammar.html`: elke `<h2>` (en
`<h3>`) waarvan de tekst matcht op `^(\d+)\.(\d+)(?:\.(\d+))?\s` krijgt — als het element nog
géén id heeft — `id="s{n1}-{n2}"` resp. `id="s{n1}-{n2}-{n3}"`. Bestaande ids (`h1`…`h20`)
blijven onaangeroerd. Idempotent: tweede run wijzigt niets. Output: aantal toegevoegde ankers +
gesorteerde lijst naar stdout.

**4.2 Boekpagina.** Per les: verzamel alle geclaimde zin-ids, pak `p(\d+)` eruit; toon
"boek p.{min}–{max}" (of "p.{n}" bij één pagina) in de leskop. Geen handmatige paginavelden.

**4.3 Kernwoorden-auto.** Tokens van de tarifit-kolom van de geclaimde zinnen: split op
whitespace en `.,;:!?()«»„""”`; strip randstreepjes; vergelijk exact (lowercase) met de
woordenlijst, waarbij een woordenlijst-cel met " / " als variantenlijst telt
(`"a / wa / waḏ"` → drie sleutels). Sorteer treffers op (cefr A1<A2<B1<B2, alfabetisch).
Eerste 12 in het kernwoordenblok, de rest in een `<details>`-lijst eronder. Toon per woord:
tarifit · nl · cefr-badge · thema.

**4.4 Tarifit-detectie in proza (check_bronnen R2-handhaving).** Detectieset:
`TAR_CHARS = "ḏṯřǧčɛɣƔḥṛṣṭẓḍạẹịụʷ"`. Elke regel van een lesbody die buiten
`{{…}}`-placeholders, buiten `::: verdieping`-koppen en buiten `` `backticks` `` een teken uit
deze set bevat → fout "vrij Tarifit in proza" met bestandsnaam+regelnummer. In `` `backticks` ``
is Tarifit alleen toegestaan als het token voorkomt in woordenlijst-varianten ∪ tokens van
geclaimde zinnen ∪ `morfemen.csv`; anders zelfde fout.

**4.5 Gedeelde claims en de les-kolom.** Meerdere lessen mogen dezelfde context claimen
(bewust beleid: 11+12, 14+17, 05+25). `bouw_cursus.py` schrijft in `zinnen.csv` kolom `les` =
laagste claimende lesnummer; niet-geclaimde `text`-zinnen → `leesboek`; overige niet-geclaimd →
`buiten-cursus`. Kolom `hoofdstuk` en `bron` niet aanraken.

**4.6 morfemen.csv startinhoud** (affixen/partikels die in proza-backticks mogen; uitbreidbaar):
`ad,partikel,101` · `war,partikel,113` · `ca,partikel,113` · `qa,partikel,77` ·
`ṯuɣa,partikel,77` · `aqqa,partikel,78` · `d,clitic,65` · `n,voorzetsel,81` · `i,voorzetsel,84` ·
`x,voorzetsel,82` · `zi,voorzetsel,82` · `di,voorzetsel,81` · `s,voorzetsel,83` ·
`ɣaa,voorzetsel,82` · `ss-,prefix,52` · `mm-,prefix,53` · `twa-,prefix,54`.

**4.7 Selectie-defaults.**
- `bron/selecties/les-01-begroetingen.txt`: genereer eenmalig (fase 4) = de eerste 10 ids van
  context `"dialogues"`, gesorteerd op (paginanummer, volgnummer). Bestand daarna handmatig
  bewerkbaar; generator leest altijd het bestand.
- `bron/besluiten/les-37-sprookje.txt`: default regel `paginabereik 134 141`. Les 37 claimt alle
  `"text"`-zinnen binnen dat bereik; `status: concept` tot Idries het bereik bevestigt.
- Les 36 (dialogen) claimt `"dialogues"` **minus** de ids uit les-01-selectie (generator sluit
  uit).

**4.8 Zinnenblok-weergave.** Standaard: tabel tarifit|nl per geclaimde sectie, met
sectiekopje = contextstring vermenselijkt (koppeltekens→spaties, quotes behouden). Les 36:
dialoogweergave (om-en-om, sprekersregels, geen tabel). Les 38: coupletweergave (groepen
gescheiden door lege regel op paginawissel). `nl/lezen.html`: alle `leesboek`-zinnen
gegroepeerd per pagina, doorlopend, tarifit-regel met nl-regel eronder.

## 5. De 38 manifests (verbatim overnemen)

Notatie hieronder: **NN slug — titel** · doel · grammatica · zinnen (exacte contextstrings) ·
bijzonderheden. Verwacht zinsaantal tussen ⟨⟩ — check_dekking vergelijkt hierop (gedeelde
claims tellen in elke les mee).

**Blok 1 — Eerste woorden**
- **01 begroeten — Begroeten & afscheid** · "Iemand begroeten en afscheid nemen." · [s18-2] ·
  selectie: "bron/selecties/les-01-begroetingen.txt" ⟨10⟩
- **02 klank-1 — Klank & spelling I: klinkers, e, w/y** · "De drie klinkers, de schwa en w/y
  lezen en uitspreken." · [s2-2, s2-7] · "vowels" + "semivowels-and-high-vowels" ⟨18⟩
- **03 wie-ben-ik — Zeggen wie je bent** · "Jezelf voorstellen: naam, herkomst, beroep." ·
  [s13-4, s5-1] · "'be'-constructions" + "free-pronouns" ⟨39⟩
- **04 klank-2 — Klank & spelling II: de drie R's en ř** · "r, rr en ř horen en lezen." ·
  [s2-4, s2-5] · "r-and-rr" + "l-and-r" ⟨6⟩ · status: dun
- **05 familie — Familie & 'mijn/jouw'** · "Over je familie praten met bezitsuitgangen." ·
  [s5-2] · "bound-pronouns" ⟨8⟩ · gedeeld met 25

**Blok 2 — Het werkwoord**
- **06 vervoeging — De vervoeging: alle personen** · "Een werkwoord vervoegen voor ik t/m
  zij-mv." · [s4-1] · "conjugation" ⟨22⟩
- **07 aspect — Afgerond of bezig: perfectief & imperfectief** · "Zeggen of iets gebeurd is of
  aan de gang is." · [s4-3, s13-1] · "the-imperfective" + "the-perfective" ⟨17⟩
- **08 ad-toekomst — Toekomst en wens: ad + aorist** · "Zeggen wat je gaat doen of wilt dat
  gebeurt." · [s7-1] · "the-aorist" + "modal-preverbal-clitics" ⟨21⟩
- **09 qa-tugha — Nu en vroeger: qa en ṯuɣa** · "Heden benadrukken en over vroeger praten." ·
  [s8-1, s8-2] · "qa-'present-relevance'" + "tugha-'past'" ⟨29⟩
- **10 aqqa-tyir — Kijk! Lijkt! Alsjeblieft: aqqa, tɣiř, aɣ** · "Presenteren, schijnen en
  aanreiken." · [s8-3, s8-4, s8-5] · "aqqa-'presentative'" + "tyir-'it-seems'" +
  "ay-'here-you-are'" ⟨14⟩

**Blok 3 — Het naamwoord**
- **11 mannelijk-vrouwelijk — Mannelijk & vrouwelijk** · "Het geslacht van naamwoorden
  herkennen." · [s3-2] · "the-structure-of-the-noun-phrase" ⟨15⟩ · gedeeld met 12
- **12 meervoud — Meervoud** · "Meervouden herkennen en vormen." · [s3-3] ·
  "the-structure-of-the-noun-phrase" ⟨15⟩ · gedeeld met 11
- **13 staat — De staat: vrij & verbonden** · "Weten wanneer een naamwoord van vorm wisselt." ·
  [s3-4] · "state" + "pre-nominal-elements" ⟨14⟩
- **14 bezit-n — Bezit met n** · "'De zoon van…' zeggen met n." · [s9-1] · "n-'of'" +
  "irregular-variations-of-n-'of'-and-ijjen-'one'" ⟨17⟩ · gedeeld met 17
- **15 aanwijzen — Deze & die** · "Aanwijzen wat dichtbij of ver is." · [s6-1] ·
  "emphasizers" ⟨3⟩ · status: dun
- **16 adjectieven — Bijvoeglijke naamwoorden** · "Eigenschappen geven aan mensen en dingen." ·
  [s11-2] · "adjectives" ⟨15⟩
- **17 telwoorden — Telwoorden 1–10 en ijjen** · "Tellen tot tien en 'één' correct gebruiken." ·
  [s10-1] · "numerals" + "irregular-variations-of-n-'of'-and-ijjen-'one'" ⟨21⟩ · gedeeld met 14
- **18 hoeveelheden — Alles, veel, weinig, niets** · "Hoeveelheden en 'iedereen/niemand'
  uitdrukken." · [s10-3] · "universal-quantifiers" +
  "non-universal-quantifiers-and-indefinites" +
  "other-non-universal-quantifiers-and-indefinites" + "'whoever',-'wherever',-etc." ⟨44⟩

**Blok 4 — De zin**
- **19 vso — Volgorde: het werkwoord voorop** · "Een basiszin bouwen in VSO-volgorde." ·
  [s14-1] · "general-outline-of-sentence-structure" ⟨15⟩
- **20 topicalisatie — Iets vooraan zetten** · "Nadruk geven door topicalisatie." ·
  [s14-2, s14-3] · "topicalization" + "post-topic" ⟨23⟩
- **21 vragen — Vragen stellen** · "Ja/nee-vragen en vraagwoordvragen maken." · [s12-1] ·
  "yes-no-questions" + "content-questions" + "interrogation-on-nouns" +
  "question-words-as-subordinators" + "question-word-questions" ⟨30⟩
- **22 ontkenning — Ontkenning** · "Zinnen ontkennen met war … ca en verwanten." · [s13-5] ·
  "the-preverbal-negative-particles" +
  "the-negative-stem-forms-of-the-verb-and-negation-of-non-verbal-sentences" +
  "the-postverbal-negative-element-bu" + "other-postverbal-negative-elements" +
  "negative-constructions-with-ma" ⟨39⟩
- **23 voorzetsels-1 — Voorzetsels I: di, x, zi, ɣaa, s** · "De vijf kernvoorzetsels
  gebruiken." · [s9-1] · "prepositions" + "di-'in'" + "x-'on'" + "zi-'from'" +
  "ghaa-'towards,-at'" + "s-'with-(instrumental)'" ⟨28⟩
- **24 voorzetsels-2 — Voorzetsels II: de rest & samengesteld** · "Overige en samengestelde
  voorzetsels gebruiken." · [s9-1, s9-2] · "aked-~-ak-'with-(comitative)'" + "jaa-'between'" +
  "i-'to'-(dative)" + "adu-~-sadu-'under'" + "ar-'until'" + "bra-~-mbra-'without'" +
  "am-'like'-and-amecnaw-'like'" + "compound-prepositions" ⟨37⟩

**Blok 5 — Clitica**
- **25 object-suffixen — Hem, haar, aan mij + richting-ḏ** · "Objectsuffixen en de
  richtingsclitic gebruiken." · [s5-2] · "bound-pronouns" + "indirect-object-pronouns" +
  "the-deictic-clitic-d-'hither'" ⟨20⟩; verdieping-zinnen: "combinations-of-verbal-clitics" +
  "combination-of-preverbal-clitics" ⟨+3⟩ · gedeeld met 05
- **26 fronting — Wanneer clitica naar voren springen** · "Cliticasprong herkennen en
  toepassen." · [s7-2, s7-3] · "clitic-fronting" + "moveable-clitics" ⟨24⟩

**Blok 6 — Verbinden**
- **27 en-of-maar — En, of, maar** · "Zinnen en woorden verbinden." · [s17-1] ·
  "coordination" + "d-'and'" ⟨14⟩
- **28 als-wanneer — Als, wanneer, omdat** · "Tijd- en voorwaardelijke bijzinnen maken." ·
  [s17-2] · "temporal-subordination" + "hypothetical-and-counterfactual" +
  "other-subordinations-and-coordinations" ⟨28⟩
- **29 willen-kunnen — Willen, kunnen, beginnen** · "Werkwoorden combineren met een tweede
  werkwoord." · [s16-1] · "operator-verbs-and-complementizers" ⟨14⟩
- **30 relatieven — Betrekkelijke bijzinnen** · "'De man die…'-zinnen bouwen." ·
  [s15-1, s15-2] · "indefinite-relatives" + "subject-relatives" + "direct-object-relatives" +
  "indirect-object-relatives" + "prepositional-relatives" ⟨13⟩
- **31 cleft — Het is X die…** · "Nadruk leggen met cleft-zinnen." · [s15-3, s15-4] ·
  "focalization:-cleft-sentences" + "cleft-constructions" ⟨11⟩

**Blok 7 — Woordvorming & klank-verdieping**
- **32 causatief — Causatief ss-** · "'Doen …'-werkwoorden maken met ss-." · [s4-2] ·
  "the-causative-prefix-ss-" + "transitivity-and-valency" ⟨19⟩
- **33 mm-twa — mm- en twa-** · "Middel- en passiefvormen herkennen." · [s4-2] ·
  "the-middle-prefix-mm-" + "the-passive-prefix-twa-" + "combined-derivations" ⟨41⟩
- **34 keelklanken — Keelklanken & emfatische medeklinkers** · "De 'moeilijke' medeklinkers
  horen en lezen." · [s2-3] · "pharyngealization" + "back-consonants" +
  "labialized-consonants" + "stops-and-spirantized-consonants" +
  "lack-of-spirantization-in-word-final-consonant-clusters" +
  "lack-of-spirantization-after-alveolar-nasals" ⟨14⟩
- **35 geminatie — Verdubbeling & versmelting** · "Geminaten en assimilaties herkennen." ·
  [s2-6, s2-8] · "geminated-consonants" + "assimilations-with-t-and-t" +
  "other-consonant-assimilations" ⟨25⟩

**Blok 8 — Lezen & luisteren**
- **36 dialogen — De dialogen** · "Een heel gesprek volgen." · [s18-2] · "dialogues" minus
  les-01-selectie ⟨70⟩ · dialoogweergave
- **37 sprookje — Het sprookje** · "Een doorlopend verhaal lezen." · [s18-1] · selectie:
  paginabereik uit bron/besluiten/les-37-sprookje.txt ⟨variabel⟩ · status: concept ·
  regel-voor-regel-weergave
- **38 izran — Izran: Riffijnse liederen** · "Coupletten lezen en herkennen." · [s18-1] ·
  "songs-(izran)" ⟨42⟩ · coupletweergave · oefeningen: geen

**Kaarten** (bron/kaarten/): `alfabet.md` (lettertabel wordt in de schrijffase geoogst uit oude
les 01; nu placeholder), `getallen.md` (11–1000; placeholder + leemte-notitie "boek bevat geen
voorbeeldzinnen"), `glossen.md` · zinnen: "glosses-and-abbreviations" + "word-list" ⟨14⟩.

**Restregel:** alle `"text"`-zinnen buiten het les-37-bereik → `nl/lezen.html`.

## 6. Generator (bouw_cursus.py)

Stappen, in deze volgorde:
1. Lees woordenlijst, zinnen, morfemen, alle lesbestanden en kaarten; parse manifests.
2. Resolve claims → per les: zinnenlijst (volgorde: paginanr, volgnr), kernwoorden (§4.3),
   boekpagina's (§4.2), ankercheck-lijst.
3. Sjabloon: `bron/sjablonen/pagina-nl.html` = kopie van huidig `nl/cursus.html` waarin de
   binnenkant van de hoofdinhoud is vervangen door `{{INHOUD}}`, de sidebar-linklijst door
   `{{SIDEBAR}}` en `<title>` door `{{TITEL}}`. Head, CSS-links, header en footer byte-gelijk
   laten. (Fase 3 maakt dit bestand; daarna is het bron, geen kopie meer.)
4. Render per blok één pagina `nl/blok-N.html`. Per les, vaste volgorde:
   eyebrow (`Blok N · Les NN · status`) → `<h2 id="les-NN">` → doelregel → boekpaginaregel →
   lesbody met placeholders vervangen → navigatie vorige/volgende. `{{zinnen}}` → §4.8-weergave;
   `{{kernwoorden}}` → §4.3-blok; `{{oefeningen}}` → container `<div class="oefeningen"
   data-les="les-NN"></div>` (gevuld door bestaande engine). `::: verdieping "T"` →
   `<details class="verdieping"><summary>T</summary>…</details>`.
5. Render `nl/lezen.html` (restregel §5) en sidebar met alle 38 lessen + 3 kaarten + lezen.
6. Schrijf `zinnen.csv` terug met bijgewerkte `les`-kolom (§4.5). Geen andere kolom wijzigen;
   rijvolgorde behouden; daarna `git diff --stat` tonen.
7. Print bouwrapport: per les zinsaantal (vergelijk met ⟨⟩ uit §5; afwijking = warning),
   kernwoordental, status.

## 7. Validators

**check_bronnen.py** (exit 1 bij elke fout):
1. elk manifest parsebaar; `id` uniek en gelijk aan bestandsnaam; `blok` ∈ 1–8
2. elke contextstring bestaat exact in zinnen.csv (anders: fout + 3 dichtstbijzijnde suggesties
   via moeilijkheidsloze substring-match)
3. elke selectie-id bestaat; selectiebestanden bestaan
4. elke les ≥3 zinnen tenzij `status: dun`; `type: kaart` vrijgesteld
5. elk `grammatica:`-anker bestaat na gen_ankers in `nl/uitleg.html` (anders: fout + lijst
   beschikbare ankers van dat hoofdstuk)
6. Tarifit-in-proza-regel §4.4
7. kernwoorden-expliciete lemma's bestaan in woordenlijst
8. woordenlijst-header exact `tarifit,nl,en,cefr,woordsoort,thema,tags`; cefr ∈
   {A1,A2,B1,B2}; thema ∈ de 25 namen uit het classificatierapport

**check_register.py**: als `bron/register-spelling.csv` ontbreekt → print "register ontbreekt —
waarschuwmodus" en exit 0. Anders: elke niet-canonieke vorm in zinnen/woordenlijst/lessen →
fout met vindplaats.

**check_dekking.py** (rapport naar stdout + `_project/dekking.md`): tabel per les
(zinnen/kernwoorden/oefeningen/status/gedeeld-met), tabel per contextstring (geclaimd door),
lijst `buiten-cursus`, lijst gedeelde claims, dunne/concept-lessen.

**Makefile**: bestaande targets behouden; toevoegen
`cursus: ankers bouw` · `ankers` · `bouw` · `check-cursus: cursus check_bronnen check_register
check_dekking` en `check` uitbreiden met `check-cursus`.

## 8. Oefeningen (fase 6)

Nieuwe types in de engine (`cursus.js`, naast bestaande `mc`):
- `{"type":"ordenen","zin_id":"p118-03","q":"Zet in de juiste volgorde:","explain":str}` —
  engine haalt de bronzin op via `zinnen.csv`-export in `les-zinnen.js`, toont de woorden
  (whitespace-split) geschud (seed = zin_id, dus stabiel), gebruiker tikt op volgorde; goed =
  exacte bronvolgorde. **De zin zelf staat nooit in de JSON** — alleen het id (R1/R2).
- `{"type":"kies-in-tabel","q":str,"options":[str],"correct":int,"explain":str,"bron_id":"pNNN-NN"}`
  — als mc, maar options zijn cellen uit een paradigma dat in de les getoond is.
- bestaand `translate` alleen richting Tarifit→NL; veld `accept` = exact de nl-kolom van de
  bronzin (plus varianten vóór/na komma's uit diezelfde cel), veld `bron_id` verplicht.
Authoring-regels: elke oefening heeft `bron_id`; mc-afleiders komen uit andere geclaimde zinnen
van dezelfde les; per les mix `1× mc + 1× ordenen + 1× translate`, behalve les 02/04/34/35
(`2× mc`), les 36/37 (`1× mc + 1× translate`), les 38 (geen). De 27 oefeningen die alleen in
`assets/cursus/exercises-*.json` staan: overnemen naar de nieuwe les-keys waar hun onderwerp
landt (oud-19→13, oud-25→26, oud-30→17/kaart), daarna de weesbestanden verwijderen.

## 9. Fasen met definition-of-done

Eén fase per Claude Code-sessie. DoD = de genoemde commando's draaien zonder fouten en tonen het
genoemde resultaat. Bij een DoD-fout: repareren, niet door naar de volgende fase.

**F1 — data & fundament.** promoot_classificatie.py (draaien; woordenlijst-header check),
mappen uit §2, manifest-parser, morfemen.csv, check_bronnen punten 1-4 en 7-8.
DoD: `python3 _project/scripts/check_bronnen.py` op een repo met alléén proefles
`08-ad-toekomst.md` → `OK — 1 les, 21 zinnen, 0 fouten`.

**F2 — ankers.** gen_ankers.py voor nl/uitleg.html + en/grammar.html; check_bronnen punt 5.
DoD: twee keer draaien → tweede run "0 toegevoegd"; ankerlijst bevat s2-2, s7-1, s13-4.

**F3 — generator-kern.** Sjabloon-extractie (§6.3), bouw_cursus.py t/m stap 5 voor alleen
blok 2 met proefles 08. DoD: `nl/blok-2.html` bestaat, bevat `id="les-08"`, 21 zinnen, een
kernwoordenblok, en valideert als HTML (geen onafgesloten tags; controleer met
`python3 -c "import html.parser"`-based check in het script).

**F4 — alle manifests.** De 38 lesbestanden + 3 kaarten letterlijk uit §5, selectie-defaults
§4.7, restregel/lezen.html, les-kolom terugschrijven, check_dekking.
DoD: `make check-cursus` groen; dekkingstabel toont per les exact de ⟨⟩-aantallen uit §5
(les 37 uitgezonderd); `zinnen.csv`-diff raakt uitsluitend de kolom `les`.

**F5 — register & hardening.** check_register.py (waarschuwmodus), Tarifit-in-proza-check
(§4.4) actief, Makefile-integratie. DoD: een testles met vrij getypt `ṯaddaaṯ` in proza laat
check_bronnen falen met bestandsnaam+regel; na verwijderen groen.

**F6 — oefeningen.** §8 volledig. DoD: `exercises-nl.json` heeft keys les-01…les-37 volgens de
mix; elk item heeft `bron_id`/`zin_id` dat bestaat; engine toont in blok-2 de drie types; de
twee weesbestanden zijn weg.

**F7 — EN + UI.** en/blok-*.html via pagina-en.html en bron/lessen/en/ (zolang een EN-tekst
ontbreekt: NL-body met banner "vertaling volgt" — pariteit van data is per constructie).
UI: scrollspy (IntersectionObserver, `aria-current="true"`), voortgang per les
(localStorage-sleutel gelijk aan de oefenengine-prefix), `<details>`-standen onthouden,
tabelwrapper-overflow i.p.v. `.content`, dialoog/couplet-CSS, dun/concept-badges.
DoD: mobiel 390px-breed geen horizontale paginascroll; sidebar markeert actieve les bij
scrollen.

**F8 — cutover.** `nl/cursus.html` → gegenereerd overzicht (blokken, voortgang, kaarten,
lezen); redirectmap `#les-NN`(oud)→blokpagina+anker(nieuw) volgens de tabel hieronder in
`vercel.json`; oude cursus-HTML naar `_project/archief/`; CLAUDE.md-sectie "bronmodel cursus"
toevoegen. DoD: `make check` volledig groen; elke oude ankerlink test-gefetcht → 200 op de
nieuwe pagina.

**Oud→nieuw (voor de redirects):** 01→02+04+34+35 (kies 02) · 02→03 · 03→03 · 04→05 · 05→01 ·
06→06 · 07→06 · 08→06 · 09→07 · 10→09 · 11→08 · 12→11 · 13→12 · 14→14 · 15→15 · 16→13 · 17→19 ·
18→23 · 19→13 · 20→17 · 21→21 · 22→22 · 23→29 · 24→25 · 25→26 · 26→27 · 27→09 · 28→16 · 29→18 ·
30→17 · 31→04 · 32→32 · 33→33 · 34→30 · 35→31 · 36→37 · 37→36 · 38→37.

## 10. Wat Sonnet NIET doet

Geen lesteksten schrijven (alleen de placeholder-comment), geen Tarifit typen, geen zinnen
kiezen buiten de vastgelegde defaults, geen §-ankers verzinnen die de validator niet bevestigt,
geen ontwerpafwijkingen "ter verbetering". Het schrijfwerk (bodies van 38 lessen, oogst uit de
oude lessen volgens de tabel in V2 §5) is een aparte fase met Opus/Idries — de site bouwt en
valideert vóór die fase al volledig, met zichtbare "TEKST VOLGT"-markering per les.
