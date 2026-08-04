"""
Eenvoudige, eigen parser voor de lesbestanden in bron/lessen/ en bron/kaarten/
(zie plan/BOUWPLAN-CURSUS-UITVOERING.md §3). Geen YAML-dependency: alleen `key: value`,
geciteerde strings, flow-lijsten `[a, b]` en bloklijsten met `-`.

Een lesbestand is: `---` frontmatter `---` gevolgd door vrije Markdown-body.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.S)


class ManifestError(Exception):
    """Fout bij het parsen van een lesbestand; message bevat bestand + reden."""


def parse_scalar(val: str):
    val = val.strip()
    if len(val) >= 2 and val[0] == '"' and val[-1] == '"':
        return val[1:-1]
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(x.strip()) for x in inner.split(",")]
    return val


def parse_frontmatter(text: str) -> dict:
    """Parse de key:value / lijst-structuur van de frontmatter (géén algemene YAML)."""
    lines = text.split("\n")
    result: dict = {}
    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i]
        if not raw.strip():
            i += 1
            continue
        if raw.startswith(" ") or raw.startswith("\t"):
            raise ManifestError(f"onverwachte inspringing op regel {i + 1}: {raw!r}")
        if ":" not in raw:
            raise ManifestError(f"regel {i + 1} mist ':': {raw!r}")
        key, _, rest = raw.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest:
            result[key] = parse_scalar(rest)
            i += 1
            continue
        # Bloklijst: opvolgende regels beginnen met minstens twee spaties + "- ".
        items: list = []
        i += 1
        while i < n and re.match(r"^\s+-\s", lines[i]):
            item = re.sub(r"^\s*-\s*", "", lines[i]).strip()
            if ":" in item and not item.startswith('"'):
                ikey, _, ival = item.partition(":")
                items.append({ikey.strip(): parse_scalar(ival.strip())})
            else:
                items.append(parse_scalar(item))
            i += 1
        result[key] = items
    return result


@dataclass
class Manifest:
    path: Path
    id: str
    slug: str
    titel: str
    status: str
    type: str = "les"
    blok: str | None = None
    doel: str | None = None
    grammatica: list[str] = field(default_factory=list)
    zinnen: list[dict] = field(default_factory=list)
    kernwoorden: object = "auto"
    body: str = ""
    body_start_line: int = 0
    raw: dict = field(default_factory=dict)

    @property
    def bestandsnaam(self) -> str:
        return self.path.name


def load_manifest(path: Path) -> Manifest:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise ManifestError(f"{path}: geen geldige frontmatter (verwacht '---' ... '---')")
    fm_text = m.group(1)
    body = text[m.end():]
    body_start_line = text[:m.end()].count("\n") + 1
    try:
        data = parse_frontmatter(fm_text)
    except ManifestError as e:
        raise ManifestError(f"{path}: {e}") from e

    if "id" not in data:
        raise ManifestError(f"{path}: veld 'id' ontbreekt")
    if "slug" not in data:
        raise ManifestError(f"{path}: veld 'slug' ontbreekt")
    if "titel" not in data:
        raise ManifestError(f"{path}: veld 'titel' ontbreekt")

    return Manifest(
        path=path,
        id=str(data["id"]),
        slug=data["slug"],
        titel=data["titel"],
        status=data.get("status", "concept"),
        type=data.get("type", "les"),
        blok=data.get("blok"),
        doel=data.get("doel"),
        grammatica=data.get("grammatica", []) or [],
        zinnen=data.get("zinnen", []) or [],
        kernwoorden=data.get("kernwoorden", "auto"),
        body=body,
        body_start_line=body_start_line,
        raw=data,
    )


def load_lessen(lessen_dir: Path) -> list[Manifest]:
    return [load_manifest(p) for p in sorted(lessen_dir.glob("*.md"))]


def load_kaarten(kaarten_dir: Path) -> list[Manifest]:
    if not kaarten_dir.exists():
        return []
    return [load_manifest(p) for p in sorted(kaarten_dir.glob("*.md"))]
