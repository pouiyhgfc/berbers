"""
Restructure the repo into nl/ and en/ language folders.

What this does:
1. Creates nl/ and en/ folders
2. Copies all *.html files to nl/ AND en/
3. In each file:
   - sets <html lang="..."> appropriately
   - rewrites relative paths (styles.css, assets/, tweaks-*.jsx) to root-absolute
   - injects a language-switch into the topnav
4. Leaves a root index.html that redirects based on browser language

After this script runs, en/*.html still contains Dutch content — translation
happens in a separate step.
"""

from __future__ import annotations
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = [
    "index.html",
    "cursus.html",
    "uitleg.html",
    "oefeningen.html",
    "woordenlijst.html",
    "woord-inzenden.html",
    "woord-inzenden-admin.html",
    "boek.html",
]


def fix_paths(html: str) -> str:
    """Rewrite relative paths to root-absolute so files work from /nl/ and /en/."""
    # styles.css (with optional version query)
    html = re.sub(r'href="styles\.css(\?[^"]*)?"', r'href="/styles.css\1"', html)
    # assets/... (in href and src)
    html = re.sub(r'(href|src)="assets/', r'\1="/assets/', html)
    # tweaks-*.jsx
    html = re.sub(r'src="(tweaks-[^"]+\.jsx)"', r'src="/\1"', html)
    return html


def set_lang(html: str, lang: str) -> str:
    return re.sub(r'<html\s+lang="[^"]*"', f'<html lang="{lang}"', html, count=1)


def inject_lang_switch(html: str, current_page: str, current_lang: str) -> str:
    """Add a NL/EN switch inside <nav class="topnav">.

    The switch is appended just before the closing </nav>.
    """
    nl_active = ' class="active"' if current_lang == "nl" else ""
    en_active = ' class="active"' if current_lang == "en" else ""
    switch = (
        '\n        <span class="lang-switch" role="group" aria-label="Language">\n'
        f'          <a href="/nl/{current_page}"{nl_active} hreflang="nl">NL</a>\n'
        '          <span class="lang-sep" aria-hidden="true">/</span>\n'
        f'          <a href="/en/{current_page}"{en_active} hreflang="en">EN</a>\n'
        '        </span>\n      '
    )

    # Find the FIRST </nav> that closes the topnav, and insert before it.
    # topnav structure: <nav class="topnav" ...> ... </nav>
    pattern = re.compile(
        r'(<nav\s+class="topnav"[^>]*>.*?)(</nav>)',
        flags=re.DOTALL,
    )
    new_html, n = pattern.subn(lambda m: m.group(1) + switch + m.group(2), html, count=1)
    if n == 0:
        # Fallback: no topnav found (shouldn't happen, but don't break the file)
        return html
    return new_html


def process_page(src: Path, dest_dir: Path, page: str, lang: str) -> None:
    html = src.read_text(encoding="utf-8")
    html = fix_paths(html)
    html = set_lang(html, lang)
    html = inject_lang_switch(html, page, lang)
    dest = dest_dir / page
    dest.write_text(html, encoding="utf-8")


def main() -> None:
    nl_dir = ROOT / "nl"
    en_dir = ROOT / "en"
    nl_dir.mkdir(exist_ok=True)
    en_dir.mkdir(exist_ok=True)

    for page in PAGES:
        src = ROOT / page
        if not src.exists():
            print(f"  skip (missing): {page}")
            continue
        process_page(src, nl_dir, page, "nl")
        process_page(src, en_dir, page, "en")
        print(f"  wrote: nl/{page}, en/{page}")

    # Now remove the originals at root - they've been moved.
    for page in PAGES:
        src = ROOT / page
        if src.exists():
            src.unlink()

    # Write root index.html that redirects based on browser language.
    root_index = ROOT / "index.html"
    root_index.write_text(
        """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Tarifit</title>
  <script>
    (function () {
      var stored = null;
      try { stored = localStorage.getItem('tarifit-lang'); } catch (e) {}
      var lang = stored;
      if (!lang) {
        var nav = (navigator.language || navigator.userLanguage || 'nl').toLowerCase();
        lang = nav.startsWith('nl') ? 'nl' : 'en';
      }
      location.replace('/' + lang + '/');
    })();
  </script>
  <meta http-equiv="refresh" content="0; url=/nl/">
</head>
<body>
  <p style="font-family: system-ui, sans-serif; padding: 24px;">
    <a href="/nl/">Nederlands</a> &middot; <a href="/en/">English</a>
  </p>
</body>
</html>
""",
        encoding="utf-8",
    )
    print("  wrote: index.html (redirect)")


if __name__ == "__main__":
    main()
