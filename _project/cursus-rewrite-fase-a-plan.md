# Plan: Cursus lessen 06–36 — les voor les inhoudelijk afstemmen

Doel: elke cursusles heeft dezelfde **pedagogische kwaliteit en toon** als lessen **01–05**, maar blijft een **samenvatting**; diepgaande grammatica blijft in `uitleg.html`. De cursus moet **inhoudelijk overeenkomen** met het gekoppelde hoofdstuk (geen tegenstrijdige uitleg).

---

## 1. Referentiesjabloon (les 01–05)

Per les in `cursus.html` altijd controleren:

| Element | Conventie |
|---------|-----------|
| Koppen | `h2` = les­titel; `h3` = hoofdonderwerp; subkopjes met `h3 class="lesson-sub"` waar nu geneste `h3`‑achtige structuur nodig is (zoals les 06). |
| Inleiding | `p.lead` met één zin doel + waarom het voor de lezer telt. |
| Kerntekst | Korte alinea’s, tabellen waar het helpt, `span.tar` op Tarifit-vormen. |
| Waarschuwing / tip | `div.box.warn` of `div.box.tip` met korte titel. |
| “Uit het boek” | Concrete Tarifit-voorbeelden met vertaling; waar mogelijk pagina­verwijzing in `crosslinks`. |
| Kruislinks | `div.crosslinks`: **Uitleg →** (`uitleg.html#hN`) + **In het boek →** (`boek.html` met pagina’s). |
| Oefeningen | `p.lesson-oef-link` → `oefeningen.html#oef-les-NN`. |
| Navigatie | `div.lesson-nav` vorige/volgende; ids `les-01` … `les-36` ongewijzigd laten. |

**Kwaliteitscriterium:** Iemand die alleen de cursus leest, snapt het hoofdpunt; iemand die doorlinkt naar uitleg, vindt geen tegenstrijdige definities.

---

## 2. Werkwijze per les (checklist)

Voor **één** les tegelijk (bijv. alleen `les-08`):

1. **Open** het blok `<section id="les-NN">` in `cursus.html`.
2. **Lees** het primaire uitleg-hoofdstuk in `uitleg.html` (anker uit de tabel hieronder). Lees **ook** subsecties waar de huidige `crossname` naar verwijst (bijv. “+ 13”, “4.2.2”).
3. **Vergelijk:** Welke definities, termen en voorbeelden *moeten* in de cursus voorkomen om pariteit te hebben? Wat kan korter dan in uitleg?
4. **Herschrijf** de cursustekst: zelfde feiten als uitleg; andere zinsbouw (les ≠ copy-paste).
5. **Woorden:** Tarifit-vormen en lemma’s afstemmen op `woordenlijst.csv` (spelling, `ḥ` / `ɣ` / dubbele medeklinkers, enz.).
6. **Controleer** `oefeningen.html#oef-les-NN` + JSON: oefeningen moeten nog kloppen met de herschreven uitleg (terminologie, voorbeeldzinnen).
7. **Optioneel:** `python _project/_audit-script.py` na een batch (als aanwezig) voor gebroken links / inconsistenties.

Pas daarna **volgende les** pakken.

---

## 3. Koppeling les ↔ uitleg (primaire ankers)

De **eerste** link onder “Uitleg →” in elke sectie is de hoofdleidraad. `crossname` in `cursus.html` kan secundaire verwijzingen noemen — die ook meenemen bij de review.

| Les | Sidebar-titel (kort) | `uitleg.html` anker | Hoofdstuk (kort) |
|-----|----------------------|---------------------|------------------|
| 01 | Klanken & alfabet | `#h3` | H2 Klanken… |
| 02 | Voornaamwoorden | `#h6` | H5 Persoonlijke vw. |
| 03 | "Ik ben..." | `#h14` | H13 Aspect/be (sectie over "be") |
| 04 | Familiewoorden | `#h4` | H3 Znw. |
| 05 | Begroetingen | `#h9` | H8 Pseudo-werkwoorden |
| 06 | Wat is een werkwoord | `#h5` | H4 Werkwoorden |
| 07 | Vervoeging ik/jij/hij/zij | `#h5` | H4 |
| 08 | Vervoeging wij/jullie/zij | `#h5` | H4 |
| 09 | Aspect afgerond vs lopend | `#h5` (+ H13) | H4 + H13 |
| 10 | Toekomst met *ad* | `#h8` | H7 Verbaal complex |
| 11 | Mannelijk vs vrouwelijk | `#h4` | H3 |
| 12 | Enkelvoud vs meervoud | `#h4` | H3 |
| 13 | "Mijn, jouw, zijn..." | `#h6` | H5 |
| 14 | "Deze" en "die" | `#h7` | H6 |
| 15 | Vrije & verbonden staat | `#h4` | H3 |
| 16 | Zinsvolgorde (VSO) | `#h15` | H14 Zinsbouw |
| 17 | Voorzetsels | `#h10` | H9 |
| 18 | Telwoorden 1–10 | `#h11` | H10 Telwoorden |
| 19 | Vraagwoorden | `#h13` | H12 Vragen |
| 20 | Ontkenning | `#h14` | H13 |
| 21 | Willen, kunnen, beginnen | `#h17` | H16 Hulpwerkwoorden |
| 22 | Voornaamwoorden-suffixen | `#h6` | H5 |
| 23 | En, of, maar, als | `#h18` | H17 Voegwoorden |
| 24 | Tijd-uitdrukkingen | `#h14` (+ H10) | H13 + tellen/tijd waar relevant |
| 25 | Bijzondere uitspraak | `#h3` | H2 |
| 26 | Bijvoeglijke naamwoorden | `#h12` | H11 Naamwoordgroep |
| 27 | Collectief vs telbaar | `#h4` | H3 |
| 28 | Tribale namen, *bu-*, *mu-* | `#h4` | H3 |
| 29 | Causatief *ss-* | `#h5` (§ 4.2.2) | H4 |
| 30 | Middel *mm-* & passief *twa-* | `#h5` (§ 4.2.3–4.2.5) | H4 |
| 31 | Pseudo-werkwoorden | `#h9` | H8 |
| 32 | Betrekkelijke bijzinnen | `#h16` | H15 |
| 33 | Cleft-zinnen | `#h16` (§ 15.3) | H15 |
| 34 | Een verhaal lezen | `#h19` | H18 Voorbeeldteksten |
| 35 | Het sprookje | `#h19` | H18 |
| 36 | Dialogen | *(geen `crosslinks`‑blok)* | **Toevoegen:** zelfde als 34/35, `#h19` (H18), eventueel tweede link naar `#h9` voor *qa* e.d. |

**Let op:** `uitleg.html` heeft ook `#h1` (intro) en `#h2` (Wat is Tarifit). Die zijn achtergrond voor de site, niet per se één-op-één met één cursusles.

---

## 4. Batches (review en commits)

Werk in **vijven** om context en review overzichtelijk te houden. Suggestie:

| Batch | Lessen | Focus |
|-------|--------|--------|
| A | 06–10 | Werkwoorden, aspect, verbaal complex |
| B | 11–15 | Naamwoorden, voornaamwoorden, staat |
| C | 16–20 | Zinsbouw, voorzetsels, vragen, ontkenning |
| D | 21–24 | Hulpwerkwoorden, voegwoorden, tijd |
| E | 25–28 | Uitspraak, BNW-groep, znw-verfijning |
| F | 29–33 | Derivaatie, pseudo-werkwoorden, bijzinnen |
| G | 34–36 | Teksten + dialogen; **les 36 crosslinks** afronden |

Na elke batch: korte commit (bijv. `Cursus: inhoud batch B lessen 11–15`) en `git push`.

---

## 5. Locatie in de codebase

- **Te bewerken:** `cursus.html` (alleen binnen de betreffende `<section id="les-NN">`).
- **Afstemmen:** `uitleg.html` (bron van waarheid, alleen aanpassen als er een echte fout in staat — niet “ter plekke” cursus vereenvoudigen door uitleg te verschuiven zonder oordeel).
- **Woorden:** `woordenlijst.csv` (niet spellen tegen de lijst).
- **Oefeningen:** `oefeningen.html`, `assets/cursus/exercises-les-06-36.json`, generatiescripts in `_project/` indien je blokken herbouwt.

---

## 6. Site-copy die buiten Fase A valt maar nuttig is

- Op de cursushoofdpagina staat nog “**25 lessen**” in de lead — feitelijk zijn het **36 lessen**. Dat kan in een aparte mini-commit worden gecorrigeerd (geen onderdeel van de lessen 06–36 herschrijving).

---

## 7. Definitie van “klaar” voor Fase A

Fase A is afgerond wanneer:

- Lessen **06–36** de checklist (sectie 1–2) per les doorlopen hebben.
- Geen bekende inconsistentie meer tussen cursus en het gekoppelde uitleg-hoofdstuk.
- Les **36** een volwaardig `crosslinks`‑blok heeft (minimaal naar `#h19`).
- Oefeningen 06–36 sluiten nog aan op de actualisatie.
