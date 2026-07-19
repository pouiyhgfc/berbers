# Eenmalig: haal oefeningen uit cursus.html, voeg links toe, schrijf snippets.
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CURSUS = ROOT / 'cursus.html'
OUT_SNIP = ROOT / '_project' / '_oefeningen-blocks.txt'

html = CURSUS.read_text(encoding='utf-8')

pat = re.compile(
    r'\n        <div class="exercises" data-lesson="(les-[0-9]{2})">\s*'
    r'<script type="application/json">\s*(\[[\s\S]*?\])\s*</script>\s*</div>',
    re.MULTILINE,
)
extracted = pat.findall(html)
OUT_SNIP.write_text('\n---\n'.join(f'{lid}\n{js}' for lid, js in extracted), encoding='utf-8')
print('extracted', len(extracted), 'blocks to', OUT_SNIP)

html2 = pat.sub('', html)


def ins_link(m):
    sid = m.group(1)
    mid = m.group(2)
    return (
        f'<section id="{sid}">{mid}\n'
        f'        <p class="lesson-oef-link"><a href="oefeningen.html#oef-{sid}">'
        f'Oefeningen bij deze les</a></p>\n        '
    )


html3 = re.sub(
    r'<section id="(les-[0-9]{2})">([\s\S]*?)\n        <div class="lesson-nav">',
    ins_link,
    html2,
)

html3 = html3.replace(
    '<script src="assets/cursus/cursus.js"></script>\n',
    '',
)

CURSUS.write_text(html3, encoding='utf-8')
print('cursus.html: exercises removed, links inserted, cursus.js removed')
