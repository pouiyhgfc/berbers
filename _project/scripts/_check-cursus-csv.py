"""Quick check: span.tar tokens in cursus.html vs woordenlijst.csv (exact / lower)."""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
csv_path = ROOT / "assets" / "woordenlijst" / "woordenlijst.csv"
variants = set()
with open(csv_path, encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) < 2:
            continue
        for v in row[0].strip().split("/"):
            v = v.strip()
            if v:
                variants.add(v)
                variants.add(v.lower())

html = (ROOT / "cursus.html").read_text(encoding="utf-8")
tokens = re.findall(r'<span class="tar">([^<]+)</span>', html)
missing = []
for t in sorted(set(tokens)):
    raw = t.strip()
    if not raw or "..." in raw:
        continue
    if raw in variants or raw.lower() in variants:
        continue
    missing.append(raw)
print("unique tar tokens:", len(set(tokens)))
print("not matched to csv variants:", len(missing))
for m in missing[:50]:
    print(" ", repr(m))
if len(missing) > 50:
    print(" ...")
