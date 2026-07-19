from pathlib import Path
import re
text = Path('cursus.html').read_text(encoding='utf-8')
text2 = re.sub(
    r'(<p class="lesson-oef-link">[^<]*<a href="oefeningen.html#oef-les-[0-9]{2}">[^<]*</a></p>)\n\s*\n(\s+)<a ',
    r'\1\n\n        <div class="lesson-nav">\n\2<a ',
    text,
)
Path('cursus.html').write_text(text2, encoding='utf-8')
print('lesson-nav count:', text2.count('<div class="lesson-nav">'))
