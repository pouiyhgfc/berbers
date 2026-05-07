"""One-off: sync assets/cursus/exercises-les-06-36.json from oefeningen.html inline JSON."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
text = (ROOT / "oefeningen.html").read_text(encoding="utf-8")
out = {}
for m in re.finditer(
    r'<div class="exercises" data-lesson="(les-[0-9]{2})">\s*'
    r'<script type="application/json">\s*',
    text,
):
    lid = m.group(1)
    num = int(lid.split("-")[1])
    if num < 6:
        continue
    start = m.end()
    end = text.find("</script>", start)
    raw = text[start:end].strip()
    out[lid] = json.loads(raw)

dest = ROOT / "assets" / "cursus" / "exercises-les-06-36.json"
dest.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Wrote", dest, "keys:", len(out))
