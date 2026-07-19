# Conventies — HTML-structuur van de bron-pagina's

Vastgelegd in stap 3.2 (deel 1) van `plan/fase-3-generatoren-en-borging.md`. Doel: het patroon
documenteren dat de extractors (`gen_cursus_md.py`, `gen_grammatica_md.py`) straks verliesloos uit de
NL-HTML moeten lezen. **Hier wordt nog geen generator beschreven** — alleen wat de HTML draagt.

Bronbestanden (NL is leidend, want `_ai/` is Nederlandstalig):

| Afgeleide          | Bron-HTML        | EN-tegenhanger (pariteit) |
| ------------------ | ---------------- | ------------------------- |
| `_ai/cursus.md`    | `nl/cursus.html` | `en/course.html`          |
| `_ai/grammatica.md`| `nl/uitleg.html` | `en/grammar.html`         |

---

## 1. De Tarifit-drager: `<span class="tar">`

**Alle** Tarifit in de body-tekst staat in `<span class="tar">…</span>`. Dit is de enige autoritatieve
drager en de basis van de round-trip-check (deel 3): de tokenverzameling van álle `class="tar"`-spans
in de bron moet exact gelijk zijn aan die in de gegenereerde markdown.

- In `nl/cursus.html`: 957 voorkomens van de gemarkeerde classes; in `nl/uitleg.html`: 964.
- Een `tar`-span kan meerdere woorden bevatten: `<span class="tar">necc ḏ Mimun</span>`,
  `<span class="tar">aqq-ec mliḥ?</span>`. Voor de tokenverzameling moet je dus binnen de span op
  whitespace splitsen (en leestekens als `?`, `.`, `~` aan de rand normaliseren), niet de hele span
  als één token nemen — anders mist de check echte verschillen.
- Varianten worden gescheiden door een losse `~` tussen twee spans:
  `<span class="tar">niṯni</span> ~ <span class="tar">nihni</span>`.

### Wat NIET als Tarifit-body telt

- **Navigatie-chrome.** Tarifit in `<em>` binnen de sidebar en `lesson-nav` is navigatietekst, geen
  inhoud: `Toekomst met <em>ad</em>`, `Causatief <em>ss-</em>`, `<em>bu-, mu-</em>`. Deze `<em>`-vormen
  staan in `.sidebar-section` (regels rond 50–121 in cursus.html) en in `.lesson-nav`-titels. De
  extractor verwerkt alleen `<main class="content">` en negeert sidebar + nav; daarmee vallen deze
  buiten de Tarifit-tokenverzameling vanzelf weg.
- **`<em>`/`<code>` met niet-Tarifit.** `<em>bad</em>`, `<em>vader</em>` (NL/EN uitspraakhulp),
  `<code>9</code>`, `<code>3</code>` (internet-spelling-cijfers), `<em>banco</em>`, `<em>queso</em>`
  (Spaanse etymons) — dit is géén Tarifit. Alleen `class="tar"` telt; vertrouw niet op `<em>`/`<code>`.
- **`<em class="source">`** draagt een Nederlandse glos tussen haakjes, geen Tarifit:
  `<em class="source">(letterlijk: "ben jij goed?")</em>`, `<em class="source">(Imperfectief)</em>`.

> **Harde regel (uit het plan):** de extractor is een verliesloze herformatteerder. Hij neemt elke
> `tar`-vorm **letterlijk** over uit kolom/span; hij synthetiseert nooit Tarifit. Mist een verwachte
> token in de output, dan moet hij falen.

---

## 2. `nl/cursus.html` — lesstructuur

Eén `<main class="content">` met een inleidend blok, daarna 36 lessen. Elke les is een eigen
`<section>`, netjes ingesprongen, met een vaste kop:

```html
<section id="les-01">
  <div class="eyebrow">les 01 · niveau 1</div>   <!-- lesnummer + niveau -->
  <h2>Klanken &amp; alfabet</h2>                  <!-- lestitel -->
  <p class="lead">…intro…</p>                      <!-- één lead-alinea -->
  …body…
  <div class="crosslinks">…</div>                  <!-- 0–1× links naar uitleg + boek -->
  <p class="lesson-oef-link">…</p>                 <!-- link naar oefeningen -->
  <div class="lesson-nav">…</div>                  <!-- vorige/volgende -->
</section>
```

Vaste feiten:

- **Secties:** `<section id="les-01">` t/m `<section id="les-36">`, in volgorde. Begin/eind herkenbaar
  aan `<section id="les-NN">` … `</section>` (beide op eigen regel, ingesprongen).
- **Lesnummer + niveau:** `<div class="eyebrow">les NN · niveau N</div>`.
- **Titel:** de eerste `<h2>` in de sectie.
- **Intro:** de eerste `<p class="lead">`.
- **Niveau-scheidingen** zitten als HTML-commentaarblokken tussen secties
  (`<!-- ===== NIVEAU 1 · DE BASIS ===== -->`) en als `<div class="sidebar-section-label">` in de
  sidebar — beide zijn navigatie/structuur, geen body.

Body-elementen binnen een les (dit is wat naar markdown moet):

| HTML                                   | Betekenis / markdown-doel                                  |
| -------------------------------------- | ---------------------------------------------------------- |
| `<h3>…</h3>`                           | subkop                                                     |
| `<h3 class="lesson-sub">…</h3>`        | genummerde subkop binnen een les (bv. "1. …")              |
| `<p>…</p>`                             | alinea (kan `tar`-spans + `<strong>`/`<em>`/`<u>` bevatten)|
| `<ul>` / `<ol>` met `<li>`             | opsomming (geordend/ongeordend)                            |
| `<table><thead><tr><th>…<tbody><tr><td>` | tabel; cellen bevatten vaak `tar`-spans                  |
| `<div class="box [tip\|warn]">`        | aandachtsblok; `<div class="box-title">` = titel, dan `<p>`|
| `<div class="crosslinks"><a>…`         | per link: `<div class="crosslabel">` + `<div class="crossname">` |
| `<p class="lesson-oef-link">`          | oefeningen-link (verschijnt niet in de huidige `_ai`-output)|
| `<div class="lesson-nav">`             | vorige/volgende-navigatie (chrome, géén body)              |

Crosslinks-vorm (label → naam, + href):
```html
<div class="crosslinks">
  <a href="uitleg.html#h3"><div class="crosslabel">Uitleg →</div><div class="crossname">Hoofdstuk 2: …</div></a>
  <a href="boek.html"><div class="crosslabel">In het boek →</div><div class="crossname">Pagina 21–33</div></a>
</div>
```

---

## 3. `nl/uitleg.html` — hoofdstukstructuur

Eén `<main class="content">` met een inleidend blok, daarna 20 secties. Anders dan cursus.html staan
de secties **aaneengesloten** (`</section><section id="hN">` op één regel, niet ingesprongen) en begint
elke sectie met een `<h1>` i.p.v. `<h2>`:

```html
<section id="h2">
  <h1>Hoofdstuk 1 — Wat is Tarifit?</h1>     <!-- chapter-titel als h1 -->
  <p class="source">📖 Boek p. 9–19</p>      <!-- bron-paginareferentie (optioneel) -->
  <p class="lead">…intro…</p>                 <!-- intro-alinea (optioneel) -->
  …body…
  <hr />                                       <!-- sectie-afsluiter -->
</section>
```

Vaste feiten:

- **Secties:** `<section id="h1">` t/m `<section id="h20">`, in volgorde.
  - `#h1` = "Cursus-aantekeningen" (voorwoord, géén hoofdstuknummer).
  - `#h2`–`#h19` = "Hoofdstuk 1" t/m "Hoofdstuk 18" (let op: id-nummer = hoofdstuknummer + 1).
  - `#h20` = "EINDSAMENVATTING".
- **Titel:** de `<h1>` aan het begin van de sectie.
- **Paginareferentie:** `<p class="source">📖 Boek p. X–Y</p>` (niet in elke (sub)sectie aanwezig).
- **Intro:** een `<p class="lead">` (niet overal aanwezig).
- **Afsluiter:** elke sectie eindigt op `<hr />`.

Body-elementen binnen een hoofdstuk:

| HTML                                   | Betekenis / markdown-doel                                  |
| -------------------------------------- | ---------------------------------------------------------- |
| `<h2>…</h2>`                           | subhoofdstuk (bv. "2.1 Waarom deze letters?")              |
| `<h3>…</h3>`                           | sub-subkop                                                 |
| `<p>…</p>` / `<p class="source">…</p>` | alinea / paginareferentie                                  |
| `<ul>` / `<ol>` met `<li>`             | opsomming                                                  |
| `<table>` (soms in `<div style="overflow-x:auto;">`) | tabel; cellen bevatten `tar`-spans + `<code>`/`<em>` |
| `<div class="box [tip\|warn]">`        | aandachtsblok (zelfde vorm als cursus.html)                |
| `<hr />`                               | sectie-/blokscheiding                                      |

---

## 4. Gedeelde, niet-relevante chrome (door beide extractors te negeren)

Alles buiten `<main class="content">` is layout en hoeft niet naar markdown:

- `<header class="topbar">` met merk, `<nav class="topnav">` en `<span class="lang-switch">` (NL/EN).
- `<aside class="sidebar">` met `sidebar-toggle`, `sidebar-title`, `sidebar-section` +
  `sidebar-section-label` en de `#…`-ankerlinks. Hierin staat de enige Tarifit-in-`<em>` (zie §1).
- `<!-- … -->`-commentaarblokken die niveaus markeren.

---

## 5. Samengevat patroon voor de extractors (deel 2)

1. Parse alleen `<main class="content">`; negeer header, sidebar, nav, commentaar.
2. Loop over de `<section id>`-blokken in documentvolgorde.
   - cursus.html: `les-NN`, titel uit `<h2>`, label uit `.eyebrow`, intro uit eerste `.lead`.
   - uitleg.html: `hN`, titel uit `<h1>`, paginaref uit `.source`, intro uit `.lead`.
3. Reproduceer de body (koppen, alinea's, lijsten, tabellen, box-blokken, crosslinks) in de bestaande
   markdown-kopstructuur van `_ai/cursus.md` / `_ai/grammatica.md`.
4. Behoud elke `<span class="tar">`-inhoud **letterlijk**.
5. Round-trip-check (deel 3): `set(tarifit_tokens_uit_html) == set(tarifit_tokens_uit_md)`, anders falen.

> ⚠️ Let op bij deel 2: de huidige `_ai/cursus.md` en `_ai/grammatica.md` lopen op enkele plekken
> inhoudelijk uit de pas met de NL-HTML (o.a. de klinkertabel in les 01 en de emfatische-medeklinker-
> opsomming verschillen). De extractor moet de **HTML** als bron nemen; verwacht dus dat de eerste
> generator-run die bestaande markdown wijzigt. Dat is correct — de HTML is leidend.
