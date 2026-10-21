#!/usr/bin/env python3
"""Build one upload-ready zip per skill into dist/.

Run after changing a skill:  python3 scripts/package.py

claude.ai and ChatGPT take a skill as a zip of its folder, with SKILL.md
inside the top-level folder. People who aren't on Claude Code download these
from dist/ instead of cloning the repo. The zips are committed, so
validate.py checks they match the source; a stale zip is the version
everyone outside Claude Code actually runs.

Timestamps and permissions are fixed so the same source always produces the
same bytes, and an unchanged skill doesn't show up in the diff.
"""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = ROOT / "plugins"
DIST = ROOT / "dist"
FIXED_TIME = (2026, 1, 1, 0, 0, 0)


def skill_dirs() -> list[Path]:
    return sorted(p.parent for p in PLUGINS_DIR.glob("*/skills/*/SKILL.md"))


def expected_entries(skill_dir: Path) -> dict[str, bytes]:
    """Archive name -> contents, for one skill folder."""
    out: dict[str, bytes] = {}
    for f in sorted(skill_dir.rglob("*")):
        if f.is_file() and f.name != ".DS_Store" and "__pycache__" not in f.parts:
            name = f"{skill_dir.name}/{f.relative_to(skill_dir).as_posix()}"
            out[name] = f.read_bytes()
    return out


def build(skill_dir: Path) -> Path:
    DIST.mkdir(exist_ok=True)
    target = DIST / f"{skill_dir.name}.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in expected_entries(skill_dir).items():
            info = zipfile.ZipInfo(name, FIXED_TIME)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    return target


def main() -> int:
    built = [build(d) for d in skill_dirs()]
    keep = {p.name for p in built}
    for stale in DIST.glob("*.zip"):
        if stale.name not in keep:
            stale.unlink()
            print(f"removed {stale.relative_to(ROOT)}")
    for p in built:
        print(f"built {p.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
