# TODO-TAALCHECK

Dit bestand bevat **geen oplossingen** — alleen inventarisatie van taalkundige
tegenstrijdigheden tussen `nl/cursus.html` en `nl/uitleg.html`, conform de harde regel: bij
twijfel over een Tarifit-vorm kies ik niet, jij beslist.

---

## A — Alle gevonden diacriticum-/klinkerconflicten (Fase 0, punt 3)

Automatisch gegenereerd: elk Tarifit-token uit `<span class="tar">` in beide bestanden is
genormaliseerd (ḇ→b, ḏ/ḍ→d, ṯ/ṭ→t, ř/ṛ→r, ṣ→s, ẓ→z, ā/ī/ū→a/i/u) en gegroepeerd. Onderstaande
64 paren hebben na normalisatie dezelfde vorm, maar worden in `cursus.html` en `uitleg.html`
met een andere diacriet/klinker gespeld. Puur hoofdletter-verschil (zinsbegin) en losse
letters (alfabet-tabellen) zijn er al uitgefilterd. Sortering: aantal voorkomens (hoog→laag).

| Cursus-vorm(en) | Uitleg-vorm(en) | Totaal (n) |
|---|---|---|
| `ḏi`(8), `di`(1) | `ḏi`(14) | 23 |
| `ṯaḏḏarṯ`(11) | `ṯaddarṯ`(1), `ṯaḏḏarṯ`(9) | 21 |
| `břa`(5) | `ḇřa`(13) | 18 |
| `tuɣa`(2), `ṯuɣa`(8) | `ṯuɣa`(7) | 17 |
| `ameqqran`(1), `ameqqṛan`(6) | `ameqqran`(9) | 16 |
| `ṯamɣārṯ`(6), `tamɣart`(1) | `ṯamɣārṯ`(7) | 14 |
| `mařa`(3), `Mara`(2) | `mařa`(4) | 9 |
| `ṯmazixṯ`(2) | `ṯmazixt`(1), `ṯmazixṯ`(5) | 8 |
| `ṯřaṯa`(3) | `ṯřaṯa`(2), `ṯřata`(3) | 8 |
| `mři`(2), `Mri`(1), `mri`(1) | `mři`(4) | 8 |
| `d-yusin`(4) | `ḏ-yusin`(4) | 8 |
| `ṯeqqim`(3) | `teqqim`(2), `ṯeqqim`(2) | 7 |
| `aked`(2) | `akeḏ`(5) | 7 |
| `jjdid`(4) | `jjḏiḏ`(3) | 7 |
| `ṯṯmenyaṯ`(2) | `ttmenyaṯ`(4) | 6 |
| `ṯṯumubin`(1) | `ttumubin`(5) | 6 |
| `ṯameqqṛanṯ`(3) | `ṯameqqranṯ`(3) | 6 |
| `adef`(2) | `aḏef`(4) | 6 |
| `ṯɣiř`(2) | `tɣiř`(4) | 6 |
| `qqimenṯ`(3) | `qqiment`(2) | 5 |
| `ṯitṯ`(2) | `ṯitt`(3) | 5 |
| `ṯiři`(1) | `ṯiři`(1), `tiři`(3) | 5 |
| `ṯameǧatc`(1) | `tameǧatc`(2), `ṯameǧatc`(2) | 5 |
| `ɛad`(3) | `ɛaḏ`(2) | 5 |
| `ṯeffeɣ`(2) | `teffeɣ`(1), `ṯeffeɣ`(1) | 4 |
| `ḏin`(1) | `ḏin`(2), `din`(1) | 4 |
| `wda`(1) | `wḏa`(3) | 4 |
| `yeṯxemmem`(2) | `yetxemmem`(2) | 4 |
| `ṯexseḏ`(1), `ṯexsed`(1) | `ṯexseḏ`(2) | 4 |
| `degg`(2) | `ḏegg`(2) | 4 |
| `ṯeqqimenṯ`(2) | `teqqiment`(1) | 3 |
| `iduraa`(1) | `iḏuraa`(1), `iduraa`(1) | 3 |
| `udef`(1) | `uḏef`(2) | 3 |
| `bda`(1) | `ḇḏa`(2) | 3 |
| `adbib`(2) | `aḏbib`(1) | 3 |
| `tuɣa-c`(1), `ṯuɣa-c`(1) | `ṯuɣa-c`(1) | 3 |
| `tuɣa-ayi`(1), `ṯuɣa-ayi`(1) | `ṯuɣa-ayi`(1) | 3 |
| `tuyi`(1), `ṯuyi`(1) | `ṯuyi`(1) | 3 |
| `zzu`(1) | `ẓẓu`(1), `zzu`(1) | 3 |
| `ṯessen`(2) | `tessen`(1) | 3 |
| `ṯettised`(2) | `ṯettiseḏ`(1) | 3 |
| `ḏinni`(1) | `ḏinni`(1), `dinni`(1) | 3 |
| `řemmed`(1) | `řemmeḏ`(1) | 2 |
| `ṯakeccutṯ`(1) | `ṯakeccutt`(1) | 2 |
| `azru`(1) | `azṛu`(1) | 2 |
| `ṯitṯawin`(1) | `ṯiṭṭawin`(1) | 2 |
| `ṯṯiřid`(1) | `ttiřid`(1) | 2 |
| `ṯṯettsed`(1) | `ttettsed`(1) | 2 |
| `ṯeṯrud`(1) | `ṯetrud`(1) | 2 |
| `wdi`(1) | `wḏi`(1) | 2 |
| `řmid`(1) | `řmiḏ`(1) | 2 |
| `udif`(1) | `uḏif`(1) | 2 |
| `ṯaɣyutc`(1) | `taɣyutc`(1) | 2 |
| `ṯanwatc`(1) | `tanwatc`(1) | 2 |
| `ṯifeřfrin`(1) | `ṯifeřfřin`(1) | 2 |
| `ṯaɛeddisṯ`(1) | `ṯaɛeḏḏisṯ`(1) | 2 |
| `iaḍ`(1) | `iaḏ`(1) | 2 |
| `ssiaḍ`(1) | `ssiaḏ`(1) | 2 |
| `ṯɣiř-ayi`(1) | `tɣiř-ayi`(1) | 2 |
| `ṯɣiř-asen`(1) | `tɣiř-asen`(1) | 2 |
| `ḏayi-ṯɣiř`(1) | `ḏayi-tɣiř`(1) | 2 |
| `ayarraf`(1) | `ayaṛṛaf`(1) | 2 |
| `d-yiwden`(1) | `ḏ-yiwden`(1) | 2 |
| `d-yesya`(1) | `ḏ-yesya`(1) | 2 |

**Let op**: dit is een automatische pas op basis van consonant/klinker-normalisatie. Niet elk
paar is per se een "fout" — sommige kunnen legitieme morfo-fonologische varianten zijn
(bv. `ř`/`t` aan het einde van een woord na assimilatie). Ik heb dit niet individueel
beoordeeld; dat is precies waarom het hier staat en niet is opgelost.

---

## B — De 11 door de audit genoemde paren (bevinding B12), met exacte vindplaats + boekpagina

| Paar | Cursus — vindplaats | Uitleg — vindplaats + hoofdstuk | Boekpagina (uitleg-sectie) |
|---|---|---|---|
| `břa` / `ḇřa` | Les 15 (`nl/cursus.html:1087`), Les 17 (`:1212`, `:1229`) | H3 Naamwoorden (`:783,795,803,961`), H9 Voorzetsels §9.1.12 (`:1848–1966`) | p. 35–50 (H3) en p. 87–96 (H9) |
| `aked` / `akeḏ` | Les 17 (`:1224`) | H5 Voornaamwoorden (`:1446`), H9 Voorzetsels §9.1.6 (`:1859,1922,1925`) | p. 65–71 (H5) en p. 87–96 (H9) |
| `bda` / `ḇḏa` | Les 21 (`:1488`) | H4 Werkwoorden (`:1267`), H16 Hulpwerkwoorden (`:2695`) | p. 51–64 (H4) en p. 139–140 (H16) |
| `jjdid` / `jjḏiḏ` | Les 26 (`:1939,1942,1943,1970`) | H11 De naamwoordgroep (`:2243,2248,2249`) | p. 103–105 |
| `ṯesɛa` / `tsɛa` | Les 18 (`:1292`, telwoordentabel "9") | H10 Telwoorden (`:2058`) | p. 97–102 |
| `ṯitṯ` / `ṯitt` | Les 11 (`:827`), Les 12 (`:895`) | H3 Naamwoorden (`:617,684,956`) | p. 35–50 |
| `ṯyatṯ` / `ṯɣattṯ` | Les 11 (`:809`, "bok/geit") | H3 Naamwoorden (`:603`) | p. 35–50 |
| `aɛabib` / `aabib` | Les 11 (`:798`, "stiefzoon/stiefdochter") | H3 Naamwoorden (`:586`, `aabib`/`ṯaabifṯ`); ook `waɛabib-inu`/`aɛabib-inu` in H17 Voegwoorden (`:2764`, voorbeeldzin) | p. 35–50 (H3) en p. 141–146 (H17, incidenteel) |
| `azru` / `azṛu` | Les 12 (`:880`, "steen/stenen") | H3 Naamwoorden (`:670`) | p. 35–50 |
| `mneqřeb` / `nneqřeb` | Les 30 (`:2218`, "zich omdraaien") | H4 Werkwoorden §4.2.2 (`:1051,1061`) | p. 51–64 |
| `ṯɣiř` / `tɣiř` | Les 31 (`:2284,2318,2322–2324`) | H8 Pseudo-werkwoorden §8.4 (`:1798,1806–1808`); ook incidenteel in H4 (`:1272`) en eindsamenvatting H20 (`:2906`) | p. 83–86 (H8) |

Bij `aɛabib`/`aabib` valt op dat de twee bestanden niet alleen in diacriet verschillen maar
ook in de vrouwelijke vorm: cursus geeft `ṯaɛabibṯ`, uitleg geeft `ṯaabifṯ` (laatste
medeklinker `ṯ` vs `f`) — dat is een extra divergentie bovenop de ɛ-aanwezigheid, dus twee
losse punten in hetzelfde woordpaar.

---

## C — Openstaande beslissingen die geen spellingsconflict zijn, maar wel taalkeuzes vergen

### C1 — Les 31: titel/lead noemt "vier ... ay", inhoud heeft vijf subkopjes met `aɣ`

- `nl/cursus.html:2284` — kop: *"Pseudo-werkwoorden: `aqqa, ṯɣiř, ay`"*
- `nl/cursus.html:2285` — lead: *"**Vier** kleine woordjes die zich gedragen als werkwoorden..."*
- Werkelijke subkopjes in de les: `aqqa`, `ṯɣiř`, **`aɣ`** (niet `ay`), `qa`, `ṯuɣa` — dat zijn
  er **vijf**, niet vier.
- Identiek probleem in `en/course.html:1889` e.v. ("Pseudo-verbs: `aqqa, ṯɣiř, ay`").
- Conform bevinding B2 expliciet **niet zelf gewijzigd** — ik leg dit aan jou voor: is de
  titel fout (moet `aɣ` zijn, en "Vijf") of is de body fout (was `ay` ooit bedoeld als apart,
  zesde element dat er nooit kwam)?

### C2 — Les 03/09/20/24/26/29/30: crossname-labels naar uitleg.html

Zie INVENTARIS.md §1 voor de volledige tabel. Vier crossnames zijn feitelijk onjuist tegen de
echte hoofdstuk-/sectiekoppen in `uitleg.html` (Les 03, 26, 29, 30). Dit zijn geen
Tarifit-vormen maar wel structurele beweringen over het boek/de uitleg, dus ik meld ze hier
naast INVENTARIS.md zodat ze niet los raken van de rest van de taalcheck. Voorgestelde
correcties volgen in Fase 1 (PLAN-HERSTRUCTURERING.md), niet hier.

---

## D — Ontbrekende Negatief Perfectief / Negatief Imperfectief-vormen (bevinding B4, uitgevoerd in Batch 1)

Les 09 se werkwoordentabel is uitgebreid naar vijf kolommen (Aorist/Perfectief/Imperfectief/
Neg. Perfectief/Neg. Imperfectief) in zowel `nl/cursus.html` als `en/course.html`. Voor de
zes werkwoorden in die tabel kon ik maar één van de tien ontbrekende cellen invullen met een
vorm die al schoon (niet uit ruwe OCR-brontekst gereconstrueerd) op de site staat:

| Werkwoord | Neg. Perfectief | Neg. Imperfectief |
|---|---|---|
| `cc` (eten) | — leeg — | — leeg — |
| `su` (drinken) | — leeg — | — leeg — |
| `qqim` (zitten/blijven) | — leeg — | — leeg — |
| `ru` (huilen) | — leeg — | — leeg — |
| `ari` (schrijven) | — leeg — | — leeg — |
| `řmeḏ` (leren) | ✅ `řmiḏ` (`uitleg.html:1224`) | — leeg — |

**Waarom leeg**: geen van deze vormen staat al ergens netjes gerenderd op de site (in een
`<span class="tar">`-tag in een tabel/lijst). Ik heb ze dus niet ingevuld — dat zou neerkomen
op zelf een Tarifit-vorm bedenken/afleiden, wat de hardste regel verbiedt.

**Wel een aanwijzing, geen bevestiging**: `_project/_boek-tekst.txt` bevat een sterk
gedegradeerde OCR-appendix (woordenboek-achtig) met mogelijk complete paradigma's voor
sommige van deze werkwoorden. Regelnummers ter info, **niet geverifieerd**:

- `su` "drinken" — regel 10726: `su lsw| / swi~a / swi / sess / = / na tissi 'to drink'`
  (mogelijk: Aorist=su, Perfectief=swa, Neg.Perfectief=**swi**, Imperfectief=sess,
  Neg.Imperfectief=sess (ongewijzigd))
- `qqim` "zitten" — regel 10397–10398: `qqim 1 = 1 = 1 tyima / tyimi / NA ayimi 'to sit, to remain'`
  (mogelijk: Neg.Perfectief=qqim (ongewijzigd), Neg.Imperfectief=**tɣimi**)
- `ru` "huilen" — regel 10506: `ru 1 = 1 = 1 tm !` (te sterk afgekapt/gecorrumpeerd om iets uit af te leiden)
- Voor `cc` en `ari` heb ik geen appendix-regel gevonden.

De OCR is te onbetrouwbaar (cijfers i.p.v. schuine strepen, ontbrekende diacrieten, `y` i.p.v.
`ɣ`) om dit als "al bestaand op de site" te beschouwen — vandaar dat ik het hier neerleg in
plaats van het over te nemen. Als je toegang hebt tot de originele boek-PDF (`boek.html`) kun
je deze drie regels snel verifiëren; zeg het dan en ik vul de tabellen alsnog in.

---

**Niets in dit bestand is opgelost.** Alle beslissingen wachten op jouw akkoord.
