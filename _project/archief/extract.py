"""
extract.py - Tarifit HTML → Markdown extractor
Extracts:
  - nl/cursus.html  → _ai/cursus/les-XX.md (36 lessons)
  - nl/uitleg.html  → _ai/grammatica/hXX.md (20 chapters)
  - woordenlijst.csv → _ai/woordenlijst.md
  - _ai/index.md    (AI instruction header)
"""

import csv
import os
import re
import sys
from pathlib import Path
from html import unescape

# Try to import BeautifulSoup
try:
    from bs4 import BeautifulSoup, NavigableString, Tag
except ImportError:
    print("Installing beautifulsoup4...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4", "lxml"], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    from bs4 import BeautifulSoup, NavigableString, Tag

BASE = Path(r"c:\Users\Idrie\Downloads\berbers-main\berbers-main")
OUT  = BASE / "_ai"

CURSUS_HTML    = BASE / "nl" / "cursus.html"
UITLEG_HTML    = BASE / "nl" / "uitleg.html"
WOORDENLIJST   = BASE / "assets" / "woordenlijst" / "woordenlijst.csv"

# ─── Helpers ─────────────────────────────────────────────────────────────────

def clean(text: str) -> str:
    """Collapse whitespace and clean up text."""
    return re.sub(r"\s+", " ", text).strip()

def element_to_md(el) -> str:
    """Convert a single HTML element to Markdown text."""
    if isinstance(el, NavigableString):
        return clean(str(el))
    
    tag = el.name
    text = el.get_text(" ", strip=True)
    text = clean(text)
    
    if tag in ("h1", "h2", "h3", "h4"):
        level = int(tag[1]) + 1  # bump by 1 since section title takes ##
        return f"\n{'#' * level} {text}\n"
    elif tag == "p":
        return f"\n{text}\n"
    elif tag == "strong":
        return f"**{text}**"
    elif tag in ("em", "span"):
        return text
    elif tag == "ul":
        items = []
        for li in el.find_all("li", recursive=False):
            items.append(f"- {clean(li.get_text(' ', strip=True))}")
        return "\n" + "\n".join(items) + "\n"
    elif tag == "ol":
        items = []
        for i, li in enumerate(el.find_all("li", recursive=False), 1):
            items.append(f"{i}. {clean(li.get_text(' ', strip=True))}")
        return "\n" + "\n".join(items) + "\n"
    elif tag == "table":
        return table_to_md(el)
    elif tag == "hr":
        return "\n---\n"
    elif tag == "div":
        # Handle tip/warn boxes
        box_title = el.find(class_="box-title")
        if box_title:
            title = clean(box_title.get_text())
            body_parts = []
            for child in el.children:
                if hasattr(child, "get_text") and "box-title" not in child.get("class", []):
                    body_parts.append(clean(child.get_text(" ", strip=True)))
            body = " ".join(filter(None, body_parts))
            return f"\n> **{title}:** {body}\n"
        return ""
    return ""

def table_to_md(table_el) -> str:
    """Convert an HTML table to a Markdown table."""
    rows = []
    
    # Headers
    thead = table_el.find("thead")
    if thead:
        header_cells = [clean(th.get_text(" ", strip=True)) for th in thead.find_all(["th", "td"])]
        if header_cells:
            rows.append("| " + " | ".join(header_cells) + " |")
            rows.append("| " + " | ".join(["---"] * len(header_cells)) + " |")
    
    # Body
    tbody = table_el.find("tbody") or table_el
    for tr in tbody.find_all("tr"):
        cells = [clean(td.get_text(" ", strip=True)) for td in tr.find_all(["td", "th"])]
        if cells and not all(c == "" for c in cells):
            # Escape pipe chars in cells
            cells = [c.replace("|", "\\|") for c in cells]
            rows.append("| " + " | ".join(cells) + " |")
    
    return "\n" + "\n".join(rows) + "\n"

def section_to_md(section, title_prefix="") -> str:
    """Convert a section element to Markdown."""
    parts = []
    
    # Skip sidebar, nav, crosslinks, lesson-nav, lesson-oef-link
    SKIP_CLASSES = {"crosslinks", "lesson-nav", "lesson-oef-link", "sidebar", "topbar", "source"}
    
    for child in section.children:
        if not isinstance(child, Tag):
            continue
        
        child_classes = set(child.get("class") or [])
        if child_classes & SKIP_CLASSES:
            continue
        
        tag = child.name
        
        if tag == "div" and "eyebrow" in child_classes:
            continue  # Skip eyebrow labels (les 01 · niveau 1)
        
        if tag in ("h1", "h2"):
            text = clean(child.get_text(" ", strip=True))
            parts.append(f"\n### {text}\n")
        elif tag == "h3":
            text = clean(child.get_text(" ", strip=True))
            parts.append(f"\n#### {text}\n")
        elif tag == "p":
            cls = set(child.get("class") or [])
            if "lead" in cls:
                text = clean(child.get_text(" ", strip=True))
                parts.append(f"\n*{text}*\n")
            elif "source" in cls:
                continue  # Skip book page refs in section body (captured at top)
            else:
                text = clean(child.get_text(" ", strip=True))
                if text:
                    parts.append(f"\n{text}\n")
        elif tag == "ul":
            items = []
            for li in child.find_all("li", recursive=False):
                items.append(f"- {clean(li.get_text(' ', strip=True))}")
            parts.append("\n" + "\n".join(items) + "\n")
        elif tag == "ol":
            items = []
            for i, li in enumerate(child.find_all("li", recursive=False), 1):
                items.append(f"{i}. {clean(li.get_text(' ', strip=True))}")
            parts.append("\n" + "\n".join(items) + "\n")
        elif tag == "table":
            parts.append(table_to_md(child))
        elif tag == "div":
            cls = set(child.get("class") or [])
            if cls & SKIP_CLASSES:
                continue
            if "box" in cls:
                box_title_el = child.find(class_="box-title")
                box_title = clean(box_title_el.get_text()) if box_title_el else "Tip"
                # Get the paragraph(s) in the box
                box_body = []
                for p in child.find_all("p"):
                    box_body.append(clean(p.get_text(" ", strip=True)))
                box_text = " ".join(filter(None, box_body))
                parts.append(f"\n> **{box_title}:** {box_text}\n")
            elif "style" in child.attrs and "overflow" in child.get("style", ""):
                # Scrollable table wrapper
                tbl = child.find("table")
                if tbl:
                    parts.append(table_to_md(tbl))
            else:
                # Recurse into generic div
                inner = section_to_md(child)
                if inner.strip():
                    parts.append(inner)
        elif tag == "hr":
            pass  # Skip horizontal rules within sections
    
    return "".join(parts)


# ─── Phase 1a: Extract Cursus Lessons ────────────────────────────────────────

def extract_cursus(html_path: Path) -> list[dict]:
    print(f"Extracting lessons from {html_path.name}...")
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "lxml")
    
    lessons = []
    for section in soup.find_all("section", id=re.compile(r"^les-\d+")):
        les_id = section["id"]  # e.g. "les-04"
        num = les_id.split("-")[1]  # "04"
        
        eyebrow = section.find(class_="eyebrow")
        niveau = clean(eyebrow.get_text()) if eyebrow else ""
        
        h2 = section.find("h2")
        title = clean(h2.get_text()) if h2 else f"Les {num}"
        
        lead = section.find(class_="lead")
        lead_text = clean(lead.get_text()) if lead else ""
        
        # Book/uitleg links
        crosslinks = section.find(class_="crosslinks")
        refs = []
        if crosslinks:
            for a in crosslinks.find_all("a"):
                href = a.get("href", "")
                label_el = a.find(class_="crosslabel")
                name_el = a.find(class_="crossname")
                label = clean(label_el.get_text()) if label_el else ""
                name = clean(name_el.get_text()) if name_el else ""
                refs.append(f"{label} {name} ({href})")
        
        body_md = section_to_md(section)
        
        lessons.append({
            "id": les_id,
            "num": num,
            "niveau": niveau,
            "title": title,
            "lead": lead_text,
            "refs": refs,
            "body_md": body_md,
        })
    
    print(f"  Found {len(lessons)} lessons.")
    return lessons


# ─── Phase 1b: Extract Uitleg Chapters ───────────────────────────────────────

def extract_uitleg(html_path: Path) -> list[dict]:
    print(f"Extracting chapters from {html_path.name}...")
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "lxml")
    
    chapters = []
    for section in soup.find_all("section", id=re.compile(r"^h\d+")):
        ch_id = section["id"]  # e.g. "h4"
        num = int(ch_id[1:])  # 4
        
        h1 = section.find("h1")
        title = clean(h1.get_text()) if h1 else f"Hoofdstuk {num}"
        
        source = section.find(class_="source")
        book_ref = clean(source.get_text()) if source else ""
        
        lead = section.find(class_="lead")
        lead_text = clean(lead.get_text()) if lead else ""
        
        body_md = section_to_md(section)
        
        chapters.append({
            "id": ch_id,
            "num": num,
            "title": title,
            "book_ref": book_ref,
            "lead": lead_text,
            "body_md": body_md,
        })
    
    print(f"  Found {len(chapters)} chapters.")
    return chapters


# ─── Phase 1c: Load Wordlist ──────────────────────────────────────────────────

def load_wordlist(csv_path: Path) -> dict[str, list]:
    print(f"Loading wordlist from {csv_path.name}...")
    words_by_level = {}
    total = 0
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 5:
                continue
            tarifit, nl, en, level, pos = row[0], row[1], row[2], row[3], row[4]
            tarifit = tarifit.strip()
            nl = nl.strip().strip('"')
            en = en.strip().strip('"')
            level = level.strip()
            pos = pos.strip()
            
            if not tarifit or not level:
                continue
            
            if level not in words_by_level:
                words_by_level[level] = []
            words_by_level[level].append((tarifit, nl, en, pos))
            total += 1
    
    print(f"  Loaded {total} words across levels: {sorted(words_by_level.keys())}")
    return words_by_level


# ─── Phase 3a: Write Wordlist ─────────────────────────────────────────────────

def write_wordlist(words_by_level: dict, out_dir: Path):
    path = out_dir / "woordenlijst.md"
    level_order = ["A1", "A2", "B1", "B2", "C1", "C2"]
    
    lines = [
        "# Tarifit Woordenlijst\n",
        "> **REGEL:** Gebruik ALLEEN woorden die letterlijk in deze lijst staan.\n",
        f"> Totaal: {sum(len(v) for v in words_by_level.values())} woorden.\n\n",
        "**Afkortingen woordsoort:** ww = werkwoord · znw = zelfstandig naamwoord · "
        "vnw = voornaamwoord · voegw = voegwoord · bvnw = bijvoeglijk naamwoord · "
        "byw = bijwoord\n\n",
    ]
    
    for level in level_order:
        if level not in words_by_level:
            continue
        words = sorted(words_by_level[level], key=lambda x: x[0].lower())
        lines.append(f"## Niveau {level}\n\n")
        lines.append("| Tarifit | Nederlands | Engels | Soort |\n")
        lines.append("|---------|------------|--------|-------|\n")
        for tarifit, nl, en, pos in words:
            # Escape pipe chars
            tarifit = tarifit.replace("|", "\\|")
            nl = nl.replace("|", "\\|")
            en = en.replace("|", "\\|")
            pos_short = pos.split("::")[0] if "::" in pos else pos
            lines.append(f"| {tarifit} | {nl} | {en} | {pos_short} |\n")
        lines.append("\n")
    
    path.write_text("".join(lines), encoding="utf-8")
    print(f"  Written: {path.relative_to(BASE)}")


# ─── Phase 3b: Write Lessons ──────────────────────────────────────────────────

def write_lessons(lessons: list[dict], out_dir: Path):
    cursus_dir = out_dir / "cursus"
    cursus_dir.mkdir(exist_ok=True)
    
    for les in lessons:
        filename = f"les-{les['num']}.md"
        path = cursus_dir / filename
        
        refs_md = ""
        if les["refs"]:
            refs_md = "\n**Links:** " + " · ".join(les["refs"]) + "\n"
        
        content = f"""## Les {les['num']} — {les['title']}

*{les['niveau']}*

{les['lead']}
{refs_md}
---
{les['body_md']}
"""
        path.write_text(content, encoding="utf-8")
    
    print(f"  Written {len(lessons)} lesson files to _ai/cursus/")


# ─── Phase 3c: Write Grammar Chapters ────────────────────────────────────────

def write_chapters(chapters: list[dict], out_dir: Path):
    gram_dir = out_dir / "grammatica"
    gram_dir.mkdir(exist_ok=True)
    
    for ch in chapters:
        filename = f"h{ch['num']:02d}.md"
        path = gram_dir / filename
        
        book_ref_md = f"\n{ch['book_ref']}\n" if ch["book_ref"] else ""
        lead_md = f"\n*{ch['lead']}*\n" if ch["lead"] else ""
        
        content = f"""## {ch['title']}
{book_ref_md}{lead_md}
---
{ch['body_md']}
"""
        path.write_text(content, encoding="utf-8")
    
    print(f"  Written {len(chapters)} grammar files to _ai/grammatica/")


# ─── Phase 5: Write Index ─────────────────────────────────────────────────────

def write_index(lessons: list[dict], chapters: list[dict], words_by_level: dict, out_dir: Path):
    total_words = sum(len(v) for v in words_by_level.values())
    
    les_index = "\n".join(
        f"- [Les {l['num']}: {l['title']}](cursus/les-{l['num']}.md)" for l in lessons
    )
    ch_index = "\n".join(
        f"- [H{c['num']}: {c['title']}](grammatica/h{c['num']:02d}.md)" for c in chapters
    )
    
    content = f"""# Tarifit Kennisbank — Instructies voor AI

## Wat is dit?
Een gestructureerde kennisbank voor de Tarifit (Riffijnse Berber) taal,
gebaseerd op Mourigh & Kossmann (2019), *An Introduction to Tarifiyt Berber*.

Schrijfwijze: Latijns-Berber alfabet (learntarifit-conventie).

## ⚠️ HARDE REGEL — VERPLICHT NALEVEN
**Verzin NOOIT Tarifit-woorden.** Gebruik uitsluitend woorden die letterlijk
in `woordenlijst.md` staan. Als een woord er niet in staat, zeg dat dan
expliciet. Gok nooit op een Tarifit-spelling.

## Hoe te gebruiken
- **Woordvertaling** → `woordenlijst.md`
- **Lesuitleg + voorbeeldzinnen** → `cursus/les-XX.md`
- **Grammaticaregels** → `grammatica/hXX.md`

Laad selectief: laad alleen de bestanden die relevant zijn voor de vraag.

## Afkortingen

| Code | Betekenis |
|------|-----------|
| ww | werkwoord |
| znw | zelfstandig naamwoord |
| vnw | voornaamwoord |
| bvnw | bijvoeglijk naamwoord |
| byw | bijwoord |
| voegw | voegwoord |
| A1–C2 | CEFR-niveau |
| M/V | mannelijk/vrouwelijk |
| ev/mv | enkelvoud/meervoud |
| FS | vrije staat (Free State) |
| AS | verbonden staat (Annexed State) |
| P | Perfectief (afgeronde actie) |
| I | Imperfectief (lopende actie) |

## Schrijfwijze — bijzondere letters

| Letter | Klank | Internet |
|--------|-------|---------|
| ṯ / ḏ | th in think / this | th |
| ḥ | harde h (Arabisch ح) | 7 |
| ɛ | ayn (Arabisch ع) | 3 |
| ɣ | zachte g (Arabisch غ) | gh |
| q | diepe k (Arabisch ق) | 9 |
| c | sj (sjaal) | ch/sh |
| ǧ | j in joke | dj |
| ř | rollende r (was l) | r |
| ṛ / ṣ / ṭ / ẓ | donkere variant | — |

## Inhoud

### Woordenlijst
{total_words} woorden → [woordenlijst.md](woordenlijst.md)

### Cursus ({len(lessons)} lessen)
{les_index}

### Grammatica ({len(chapters)} hoofdstukken)
{ch_index}
"""
    
    path = out_dir / "index.md"
    path.write_text(content, encoding="utf-8")
    print(f"  Written: {path.relative_to(BASE)}")


# ─── Phase 6: Validation ─────────────────────────────────────────────────────

def validate(lessons, chapters, words_by_level):
    print("\n=== Validatie ===")
    print(f"  Lessen:      {len(lessons)} (verwacht: 36)")
    print(f"  Hoofdstukken:{len(chapters)} (verwacht: 20)")
    total = sum(len(v) for v in words_by_level.values())
    print(f"  Woorden:     {total}")
    
    # Spot check
    ids = [l["id"] for l in lessons]
    for expected in ["les-01", "les-04", "les-20", "les-36"]:
        status = "OK" if expected in ids else "MISSING"
        print(f"  {expected}: {status}")
    
    ch_ids = [f"h{c['num']}" for c in chapters]
    for expected in ["h1", "h4", "h10", "h20"]:
        status = "OK" if expected in ch_ids else "MISSING"
        print(f"  {expected}: {status}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    # Create output dirs
    OUT.mkdir(exist_ok=True)
    (OUT / "cursus").mkdir(exist_ok=True)
    (OUT / "grammatica").mkdir(exist_ok=True)
    
    # Fase 1: Extract
    lessons      = extract_cursus(CURSUS_HTML)
    chapters     = extract_uitleg(UITLEG_HTML)
    words        = load_wordlist(WOORDENLIJST)
    
    # Fase 6 (pre): Validate counts
    validate(lessons, chapters, words)
    
    # Fase 3: Write markdown
    print("\n=== Schrijven ===")
    write_wordlist(words, OUT)
    write_lessons(lessons, OUT)
    write_chapters(chapters, OUT)
    write_index(lessons, chapters, words, OUT)
    
    print("\nKlaar! Bestanden staan in _ai/")


if __name__ == "__main__":
    main()
