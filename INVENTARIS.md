# INVENTARIS — Fase 0

Geen bestanden gewijzigd. Deze inventaris is gemaakt met scripts die `nl/cursus.html`,
`nl/uitleg.html`, `nl/oefeningen.html`, `en/course.html` en `en/grammar.html` structureel
uitlezen (anchors, kruisverwijzingen, `<span class="tar">`-tokens). Ruwe scriptoutput staat
in `_project/generated/_fase0_*.json` / `.txt` voor eigen verificatie.

---

## 1. Ankerkaart

Alle 36 lessen zijn structureel intact: elke les heeft precies één vorige- en één
volgende-link, de keten 01→36 is gesloten zonder gaten, elke `uitleg.html#hN`-anchor bestaat
(uitleg.html heeft alleen hoofdstuk-brede anchors `h1`–`h20`, geen subhoofdstuk-anchors), en
elke `oefeningen.html#oef-les-NN`-anchor bestaat. Er zijn dus geen **technisch kapotte**
(404-achtige) links. Er zijn wel **inhoudelijk misleidende** kruisverwijzingen: de
`crossname`-tekst die op de cursuspagina staat, komt op vier plekken niet overeen met de
werkelijke koptekst/sectie op het doelanker. Die vier zijn gemarkeerd (❌) en komen overeen
met bevinding B8.

| Les | Titel | Niveau | Uitleg-link | Boekpagina (op uitleg-anchor) | Oef-link | Status |
|---|---|---|---|---|---|---|
| 01 | Klanken & alfabet | 1 | #h3 — Hoofdstuk 2: Klanken, schrijfwijze & uitspraak | p. 21–33 | #oef-les-01 | OK |
| 02 | Persoonlijke voornaamwoorden | 1 | #h6 — Hoofdstuk 5: Voornaamwoorden | p. 65–71 | #oef-les-02 | OK |
| 03 | "Ik ben..." — zinnen zonder werkwoord | 1 | #h14 — gelabeld *"Hoofdstuk 13: 'Be'-constructies"* | p. 113–127 | #oef-les-03 | ❌ H13 heet echt "Aspect, modus en ontkenning"; het relevante §13.4 heet **"Zijn"-constructies**, niet "Be"-constructies (Engels woord in NL-tekst, en fout aangeduid als losstaand hoofdstuk i.p.v. sectie 13.4) |
| 04 | Familiewoorden | 1 | #h4 — Hoofdstuk 3: Naamwoorden, sectie 3.6 | p. 35–50 | #oef-les-04 | OK |
| 05 | Begroetingen & dagelijkse uitdrukkingen | 1 | #h9 — Hoofdstuk 8: Pseudo-werkwoorden | p. 83–86 | #oef-les-05 | OK |
| 06 | Wat is een werkwoord in Tarifit? | 2 | #h5 — Hoofdstuk 4: Werkwoorden | p. 51–64 | #oef-les-06 | OK |
| 07 | Vervoeging: ik/jij/hij/zij | 2 | #h5 — Hoofdstuk 4: Werkwoorden | p. 51–64 | #oef-les-07 | OK |
| 08 | Vervoeging: wij/jullie/zij | 2 | #h5 — Hoofdstuk 4: Werkwoorden | p. 51–64 | #oef-les-08 | OK |
| 09 | Aspect: afgerond vs lopend | 2 | #h5 — gelabeld "Hoofdstuk 4 + 13" | p. 51–64 | #oef-les-09 | ⚠️ Wijst naar twee hoofdstukken tegelijk (H4 werkwoorden + H13 aspect/modus/ontkenning) — technisch geen kapotte link, maar symptoom van B2/B4: de aspectstof en `qa` horen inhoudelijk bij elkaar maar staan in twee hoofdstukken |
| 10 | Toekomst met `ad` | 2 | #h8 — Hoofdstuk 7: Verbale complex | p. 77–82 | #oef-les-10 | OK |
| 11 | Mannelijk vs vrouwelijk | 3 | #h4 — Hoofdstuk 3: Naamwoorden | p. 35–50 | #oef-les-11 | OK |
| 12 | Enkelvoud vs meervoud | 3 | #h4 — Hoofdstuk 3: Naamwoorden | p. 35–50 | #oef-les-12 | OK |
| 13 | "Mijn, jouw, zijn, haar..." | 3 | #h6 — Hoofdstuk 5: Voornaamwoorden | p. 65–71 | #oef-les-13 | OK |
| 14 | "Deze" en "die" | 3 | #h7 — Hoofdstuk 6: Aanwijzende voornaamwoorden | p. 73–75 | #oef-les-14 | OK |
| 15 | Vrije & verbonden staat | 3 | #h4 — Hoofdstuk 3: Naamwoorden | p. 35–50 | #oef-les-15 | OK (zie B1 — circulaire verwijzing met Les 16/17, geen kapotte link maar een structuurprobleem) |
| 16 | Zinsvolgorde: VSO | 4 | #h15 — Hoofdstuk 14: Zinsbouw | p. 129–134 | #oef-les-16 | OK (zie B1) |
| 17 | Voorzetsels | 4 | #h10 — Hoofdstuk 9: Voorzetsels | p. 87–96 | #oef-les-17 | OK (zie B1) |
| 18 | Telwoorden 1–10 | 4 | #h11 — Hoofdstuk 10: Telwoorden | p. 97–102 | #oef-les-18 | OK |
| 19 | Vraagwoorden | 4 | #h13 — Hoofdstuk 12: Vragen stellen | p. 107–109 | #oef-les-19 | OK |
| 20 | Ontkenning: "niet" | 4 | #h14 — gelabeld "Hoofdstuk 13: Ontkenning" | p. 113–127 | #oef-les-20 | ⚠️ H14 heet voluit "Aspect, modus en ontkenning" — het label noemt alleen het laatste deel (§13.5); geen echte fout, wel onvolledig |
| 21 | Willen, kunnen, beginnen | 5 | #h17 — Hoofdstuk 16: Hulpwerkwoorden | p. 139–140 | #oef-les-21 | OK |
| 22 | Voornaamwoorden-suffixen | 5 | #h6 — Hoofdstuk 5: Voornaamwoorden | p. 65–71 | #oef-les-22 | OK |
| 23 | En, of, maar, als | 5 | #h18 — Hoofdstuk 17: Voegwoorden | p. 141–146 | #oef-les-23 | OK |
| 24 | Tijd-uitdrukkingen | 5 | #h14 — gelabeld "Hoofdstuk 13 + 10" | p. 113–127 | #oef-les-24 | ⚠️ Twee hoofdstukken tegelijk — symptoom van B2 (`ṯuɣa`-duplicaat met Les 31) |
| 25 | Bijzondere uitspraak: gevocaliseerde R | 6 | #h3 — Hoofdstuk 2: Klanken, schrijfwijze & uitspraak | p. 21–33 | #oef-les-25 | OK (zie B6 — zelfde anker als Les 01) |
| 26 | Bijvoeglijke naamwoorden | 6 | #h12 — gelabeld "Hoofdstuk 11: Bijvoeglijke naamwoorden" | p. 103–105 | #oef-les-26 | ❌ H11 heet echt **"De naamwoordgroep"** (§11.2 gaat over adjectieven); de crossname verzint een hoofdstuktitel die niet bestaat |
| 27 | Collectief vs telbaar | 6 | #h4 — Hoofdstuk 3: Naamwoorden | p. 35–50 | #oef-les-27 | OK |
| 28 | Tribale namen, `bu-`, `mu-` | 6 | #h4 — Hoofdstuk 3: Naamwoorden | p. 35–50 | #oef-les-28 | OK |
| 29 | Causatief: laat iemand X doen | 7 | #h5 — gelabeld "Hoofdstuk 4.2.2" | p. 51–64 | #oef-les-29 | ❌ §4.2.2 is **`mm-`** (wederkerig/middel), niet het causatief. Het causatief `ss-` staat in **§4.2.1** |
| 30 | Middel `mm-` & passief `twa-` | 7 | #h5 — gelabeld "Hoofdstuk 4.2.3–4.2.5" | p. 51–64 | #oef-les-30 | ❌ Uitleg heeft alleen §4.2.1 (`ss-`) t/m §4.2.3 (`twa-`); §4.2.4/4.2.5 **bestaan niet**. Correcte range is §4.2.2–4.2.3 |
| 31 | Pseudo-werkwoorden: `aqqa, ṯɣiř, ay` | 7 | #h9 — Hoofdstuk 8: Pseudo-werkwoorden | p. 83–86 | #oef-les-31 | OK qua link; zie wel B2 (inhoudelijke problemen in de les zelf — zie §"Interne tegenstrijdigheid" onderaan) |
| 32 | Betrekkelijke bijzinnen | 7 | #h16 — Hoofdstuk 15: Betrekkelijke bijzinnen | p. 135–138 | #oef-les-32 | OK |
| 33 | Cleft-zinnen | 7 | #h16 — gelabeld "Hoofdstuk 15.3" | p. 135–138 | #oef-les-33 | OK — geverifieerd: §15.3 "Cleft-zinnen" bestaat echt in uitleg.html, dit label is **correct** (in tegenstelling tot de 4.2.x-labels hierboven) |
| 34 | Een verhaal lezen | 8 | #h19 — Hoofdstuk 18: Voorbeeldteksten | p. 147+ | #oef-les-34 | OK |
| 35 | Het sprookje van de parel-jongen | 8 | #h19 — Hoofdstuk 18: Voorbeeldteksten | p. 147+ | #oef-les-35 | OK |
| 36 | Praktische dialogen | 8 | #h19 — Hoofdstuk 18: Voorbeeldteksten & dialogen | p. 147+ | #oef-les-36 | OK |

**Samenvatting**: 4 crossnames zijn feitelijk onjuist (Les 03, 26, 29, 30 — dit dekt bevinding
B8 volledig en bevestigt hem woord voor woord tegen de echte hoofdstukkoppen). Les 33's
"15.3"-verwijzing is bij nader onderzoek juist **correct**, dus die hoeft niet in de B8-fix
opgenomen te worden. Les 09/20/24 wijzen naar een breed hoofdstuk zonder technische fout,
maar signaleren wel de structuurproblemen uit B2/B4/B9.

---

## 2. Concept-eigenaarskaart

Aantallen zijn automatische treffers van het concept-token/trefwoord per les (cursus.html) en
per hoofdstuk (uitleg.html) — bedoeld als kwantitatieve onderbouwing, niet als exacte
telling van "betekenisvolle" voorkomens (bv. bij `ad` en `a` kunnen enkele treffers ruis zijn).
Volledige cijfers staan in `_project/generated/_fase0_concepts.json`.

| Concept | Gebruikt in lessen (cursus) | Uitgelegd in hoofdstuk (uitleg) | Duiding |
|---|---|---|---|
| `qa` | 09(8), 16(2), 21(2), 27(1), 31(12), 32(1), 36(6) | h5(9), h8(3), h9(10), h10(2), **h14(15)**, h15(3), h16(1), h17(2), h18(1) | Piek in Les 09 (introductie) én Les 31 (uitleg) — bevestigt B2: `qa` wordt in Les 09 geïntroduceerd maar pas in Les 31 (22 lessen later) echt uitgelegd, en wordt tussendoor in 16/17/21/36 al gebruikt. |
| `ṯuɣa` | 24(4), **31(8)**, 34(10), 35(6) | h9(12), h14(8) | Les 31 heeft bijna dubbel zoveel treffers als Les 24 zelf — consistent met B2's "half duplicaat". |
| `ad` (incl. `xad`) | 09(2), **10(17)**, 11(1), 21(6), 32(2), 34(3) | h8(18), h5(5), h14(5), h16(3), h17(4), h18(4) | Heeft, anders dan `qa`, wél een eigen les (10) vlak na introductie — geen probleem, ter vergelijking. |
| `waa … ca` (ontkenning) | 19(2), **20(25)**, 21(4), 31(1), 33(1), 34(10), 35(1), 36(1) | **h14(32)**, h8(16), h11(8), h13(5) | Grotendeels netjes geconcentreerd in Les 20; kleine vooruitwijzing in Les 19. |
| bezitssuffixen | **04(1)**, 07(1), **13(1)**, **17(6)**, 18(1), 20(1), 35(5), 36(2) | h6(3), h10(3), h11(2), h14(5) | Bevestigt B9: verspreid over 04/13/17/22 (zie ook "voornaamwoord-clitica" hieronder voor Les 22), zonder één centrale les. |
| voornaamwoord-clitica | 21(1), **22(1)**, 23(1), 32(1) | h6(7), **h8(8)**, h9(6), h10(4), h18(6), h20(5) | Trefwoord komt in cursus.html zelf nauwelijks letterlijk voor — het concept leeft vooral impliciet in de voorbeeldzinnen (zie B3). |
| clitic-fronting | **32(1)** | h6(2), **h8(4)**, h13(1), h16(1), **h18(5)**, h20(2) | Alleen expliciet benoemd in Les 32 ("kenmerk 3") — bevestigt B3: geen eigen les, ondanks dat het al vanaf Les 20 nodig is in voorbeeldzinnen. |
| vrije/verbonden staat | 14(1), **15(14)**, 16(4), 17(4), 22(2), 26(4), 31(1), 32(1), 34(4), 35(3) | **h4(10)**, h10(8), h2(4), h6(2), h12(2), h14(2), h15(5), h20(3) | Concentratie in Les 15 (eigen les), maar Les 16/17 leunen er zwaar op terug (B1) en Les 14 gebruikt het al vóór Les 15. |
| vijf aspectvormen | 06(1), 08(1), **09(24)**, 10(2), 20(4), 21(6), 30(7), 31(4), 34(4), 35(3) | **h5(78)**, h14(39), h17(7), h20(12) | Les 09 is verreweg de dichtste (24), maar Les 20 heeft er al 4 nodig — bevestigt B4 (Les 09 leert er 3, Les 20 heeft er 5 nodig). |
| gevocaliseerde r | 03(2), 11(2), 13(2), 14(4), **15(9)**, 16(5), 17(3), 18(2), 22(2), 23(1), **25(10)**, 26(5), 27(1), 28(1), 32(4), 35(2), 36(1) | **h4(17)**, h3(13), h7(9), h11(6), h10(3), h12(3), h14(4) | De macron-schrijfwijze (ā/ī/ū) wordt al vanaf Les 03 gebruikt in woorden, lang vóór hij in Les 25 wordt uitgelegd — bevestigt B6 letterlijk. |

Bovenstaande cijfers zijn onafhankelijk gegenereerd (niet overgenomen uit de bevindingenlijst)
en komen voor elk concept overeen met de gestelde bevindingen B1–B4, B6 en B9.

---

## 3. Tokenlijst-conflicten

Zoals gevraagd **niet opgelost**, alleen geïnventariseerd. Volledige lijst (64 genormaliseerde
paren waarbij `nl/cursus.html` en `nl/uitleg.html` een verschillende spelling gebruiken voor
wat na normalisatie van b/ḇ, d/ḏ/ḍ, t/ṯ/ṭ, r/ř/ṛ, s/ṣ, z/ẓ en lange klinkers (ā/ī/ū) dezelfde
vorm is) staat in **`TODO-TAALCHECK.md`**, sectie A. De 11 door de audit al genoemde paren
(břa/ḇřa e.a., bevinding B12) staan daar met exacte vindplaats + boekpagina in sectie B.

Puur-hoofdletter-verschillen (zin-begin) en losse letters (uit het alfabet-overzicht) zijn
uit deze lijst gefilterd — dat zijn geen spellingsconflicten.

---

## 4. Parity-check NL/EN

`en/course.html` heeft **exact 36 lessecties**, met dezelfde niveau-indeling (1–8) en dezelfde
les→niveau-toewijzing als `nl/cursus.html`. Structureel dus volledige pariteit — geen
ontbrekende of extra lessen, geen niveau-verschuivingen.

Wel gevonden bij het doorlopen van de titels (niet gevraagd, maar direct zichtbaar):

- **Les 20, EN-titel**: `"Disclaimer: 'not'"` — dit is een foutieve vertaling van "Ontkenning"
  (moet "Negation" zijn; "Disclaimer" betekent iets heel anders). Dit is Engelse cursus-tekst,
  geen Tarifit-vorm, dus buiten de hardste regel — maar wel meteen zichtbaar en de moeite van
  het vermelden waard voor een eventuele latere opschoning.
- **Les 28, EN-titel**: `"tribal names, bu-, mu-"` mist een hoofdletter (NL heeft "Tribale
  namen"). Cosmetisch.
- **Les 31**: de titel/body-tegenstrijdigheid `ay`/`aɣ` (zie hieronder) staat **identiek** ook
  in `en/course.html` — is dus geen NL-only probleem.

Volledige regel-voor-regel vergelijking staat in `_project/generated/_fase0_parity_titles.txt`.

---

## Interne tegenstrijdigheid (geen cursus-vs-uitleg, maar binnen cursus.html zelf)

Los van de hierboven gevraagde punten, dit sprong meteen op bij het inlezen van Les 31 en is
al onderdeel van bevinding B2 — hier expliciet vastgelegd zodat hij niet verloren gaat:

- `nl/cursus.html:2284` — kop: `<h2>Pseudo-werkwoorden: aqqa, ṯɣiř, ay</h2>`
- `nl/cursus.html:2285` — lead-tekst: *"**Vier** kleine woordjes..."*
- Werkelijke inhoud van de les: **vijf** subkopjes — `aqqa` (2317... ai), `ṯɣiř`, **`aɣ`**
  (niet `ay`!), `qa`, `ṯuɣa`.
- Dezelfde tekst staat identiek in `en/course.html` ("Pseudo-verbs: aqqa, ṯɣiř, ay").

Conform de opdracht **niet zelf gewijzigd** — dit hoort bij de openstaande beslissingen in
Fase 1 (en staat ter referentie ook in `TODO-TAALCHECK.md`, sectie C).

Klein, niet-Tarifit observatie terzijde: op drie plekken in `nl/cursus.html` en één plek in
`nl/uitleg.html` is het Nederlandse woord "woordjes"/"straatbordjes" gecorrumpeerd tot
"woorǧes"/"straatborǧes" (waarschijnlijk een copy/OCR-artefact — de `ǧ` hoort daar niet, dit
is geen Tarifit-teken op die plek). Puur Nederlandse spelling, dus buiten de hardste regel,
maar genoteerd voor het geval dat relevant is bij Fase 1.

---

**Einde Fase 0. Wacht op akkoord voordat Fase 1 (het plan) wordt opgesteld.**
