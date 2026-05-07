"""Build oefeningen.html from extracted blocks + lesson metadata."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LESSONS = [
    ("01", "Klanken & alfabet"),
    ("02", "Voornaamwoorden"),
    ("03", '"Ik ben..."'),
    ("04", "Familiewoorden"),
    ("05", "Begroetingen"),
    ("06", "Wat is een werkwoord"),
    ("07", "Vervoeging ik/jij/hij/zij"),
    ("08", "Vervoeging wij/jullie/zij"),
    ("09", "Aspect: afgerond vs lopend"),
    ("10", 'Toekomst met ad'),
    ("11", "Mannelijk vs vrouwelijk"),
    ("12", "Enkelvoud vs meervoud"),
    ("13", '"Mijn, jouw, zijn..."'),
    ("14", '"Deze" en "die"'),
    ("15", "Vrije & verbonden staat"),
    ("16", "Zinsvolgorde (VSO)"),
    ("17", "Voorzetsels"),
    ("18", "Telwoorden 1–10"),
    ("19", "Vraagwoorden"),
    ("20", "Ontkenning"),
    ("21", "Willen, kunnen, beginnen"),
    ("22", "Voornaamwoorden-suffixen"),
    ("23", "En, of, maar, als"),
    ("24", "Tijd-uitdrukkingen"),
    ("25", "Bijzondere uitspraak"),
    ("26", "Bijvoeglijke naamwoorden"),
    ("27", "Collectief vs telbaar"),
    ("28", "Tribale namen, bu-, mu-"),
    ("29", "Causatief ss-"),
    ("30", "Middel mm- & passief twa-"),
    ("31", "Pseudo-werkwoorden"),
    ("32", "Betrekkelijke bijzinnen"),
    ("33", "Cleft-zinnen"),
    ("34", "Een verhaal lezen"),
    ("35", "Het sprookje"),
    ("36", "Dialogen"),
]

# Load JSON blocks (les 01–05)
raw = (ROOT / "_project" / "_oefeningen-blocks.txt").read_text(encoding="utf-8")
chunks = {}
for part in raw.split("\n---\n"):
    part = part.strip()
    if not part:
        continue
    first_nl = part.find("\n")
    lid = part[:first_nl].strip()  # les-01
    js = part[first_nl + 1 :].strip()
    chunks[lid] = js

extra_path = ROOT / "assets" / "cursus" / "exercises-les-06-36.json"
extra_obj = {}
if extra_path.exists():
    extra_obj = json.loads(extra_path.read_text(encoding="utf-8"))

nav_links = "".join(
    f'<a href="#oef-les-{num}">{num}</a>' for num, _ in LESSONS
)

sections = []
for num, title in LESSONS:
    lid = f"les-{num}"
    back = f'cursus.html#les-{num}'
    h = f"Les {int(num):02d} — {title}"
    if lid in chunks:
        js = chunks[lid]
    elif lid in extra_obj:
        js = json.dumps(extra_obj[lid], ensure_ascii=False, indent=2)
    else:
        js = None
    if js is not None:
        sections.append(
            f'''      <section class="oef-lesson" id="oef-{lid}">
        <h2>{h}</h2>
        <p class="oef-back"><a href="{back}">Lees eerst de les in de cursus</a></p>
        <div class="exercises" data-lesson="{lid}">
          <script type="application/json">
{js}
          </script>
        </div>
      </section>'''
        )
    else:
        sections.append(
            f'''      <section class="oef-lesson" id="oef-{lid}">
        <h2>{h}</h2>
        <p class="oef-back"><a href="{back}">Terug naar de les</a></p>
        <div class="oef-placeholder box">
          <p style="margin:0">Voor deze les zijn de oefeningen nog in voorbereiding. De inhoud van de cursus is leidend; oefen met de voorbeelden en de woordenlijst.</p>
        </div>
      </section>'''
        )

body = "\n\n".join(sections)

html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>Oefeningen · Tarifit</title>
  <link rel="stylesheet" href="styles.css?v=4">
</head>
<body>
  <header class="topbar">
    <div class="topbar-inner">
      <a href="index.html" class="brand"><span class="brand-mark" aria-hidden="true"></span>arifit</a>
      <nav class="topnav">
        <a href="cursus.html">Cursus</a>
        <a href="oefeningen.html" class="active">Oefeningen</a>
        <a href="uitleg.html">Uitleg</a>
        <a href="woordenlijst.html">Woordenlijst</a>
        <a href="woord-inzenden.html" class="nav-quiet">Woord voorstellen</a>
        <a href="boek.html">Het boek</a>
      </nav>
    </div>
  </header>

  <main class="boek-container" style="max-width: 900px;">
    <div class="eyebrow">oefenen</div>
    <h1>Oefeningen</h1>
    <p class="lead">Alle interactieve opdrachten per les. Je voortgang wordt in deze browser bewaard. Ga naar een les via het raster hieronder of via de link <strong>Oefeningen bij deze les</strong> op de cursuspagina.</p>

    <nav class="oef-quick-nav" aria-label="Spring naar les">
      {nav_links}
    </nav>

{body}
  </main>

  <footer>
    <p>Gebaseerd op Mourigh &amp; Kossmann (2019).</p>
  </footer>
  <script src="assets/cursus/cursus.js"></script>
</body>
</html>
"""

(ROOT / "oefeningen.html").write_text(html, encoding="utf-8")
print("Wrote oefeningen.html")
