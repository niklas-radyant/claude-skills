#!/usr/bin/env python3
"""Validate the marketplace, its plugins, and every skill in them.

Run before pushing:  python3 scripts/validate.py

A broken manifest here breaks `/plugin install` for everyone who has added
this marketplace, so this runs in CI on every PR. No dependencies beyond
the standard library — the frontmatter parse is deliberately hand-rolled so
CI needs nothing installed.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
PLUGINS_DIR = ROOT / "plugins"

# A description is the whole trigger surface: too short and the skill never
# fires, too long and every invocation pays for it. Bounds are advisory.
DESC_MIN = 40
DESC_MAX = 600

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


def load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        err(f"{rel(path)}: missing")
    except json.JSONDecodeError as e:
        err(f"{rel(path)}: invalid JSON — {e}")
    return None


def parse_frontmatter(path: Path) -> dict[str, str] | None:
    """Read the leading `---` block as flat key: value pairs."""
    text = path.read_text()
    if not text.startswith("---"):
        err(f"{rel(path)}: no YAML frontmatter (must start with '---')")
        return None
    end = text.find("\n---", 3)
    if end == -1:
        err(f"{rel(path)}: frontmatter is never closed with '---'")
        return None
    fields: dict[str, str] = {}
    for line in text[3:end].strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            err(f"{rel(path)}: frontmatter line is not 'key: value' — {line!r}")
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def check_skill(skill_dir: Path, plugin_name: str) -> str | None:
    """Validate one skills/<name>/ directory. Returns the skill name."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        err(f"{rel(skill_dir)}: no SKILL.md")
        return None

    fm = parse_frontmatter(skill_md)
    if fm is None:
        return None

    name = fm.get("name")
    desc = fm.get("description")

    if not name:
        err(f"{rel(skill_md)}: frontmatter has no 'name'")
    elif name != skill_dir.name:
        err(
            f"{rel(skill_md)}: frontmatter name {name!r} does not match "
            f"its directory {skill_dir.name!r} — Claude Code addresses the "
            f"skill by directory, so these must agree"
        )

    if not desc:
        err(f"{rel(skill_md)}: frontmatter has no 'description'")
    else:
        if len(desc) < DESC_MIN:
            warn(
                f"{rel(skill_md)}: description is {len(desc)} chars — too "
                f"thin to trigger reliably. Say when to use it, not just "
                f"what it is."
            )
        if len(desc) > DESC_MAX:
            warn(
                f"{rel(skill_md)}: description is {len(desc)} chars "
                f"(soft cap {DESC_MAX}). It is read on every invocation; "
                f"move detail into the body."
            )

    # Every reference/... path mentioned in the body must resolve. A dangling
    # pointer sends the model looking for a file that is not there.
    body = skill_md.read_text()
    for match in sorted(set(re.findall(r"(reference/[\w./-]+\.md)", body))):
        if not (skill_dir / match).is_file():
            err(f"{rel(skill_md)}: references {match}, which does not exist")

    # And every reference file should be reachable from the body, or it is
    # dead weight nobody will ever load.
    ref_dir = skill_dir / "reference"
    if ref_dir.is_dir():
        for ref in sorted(ref_dir.rglob("*.md")):
            token = str(ref.relative_to(skill_dir))
            if token not in body:
                warn(
                    f"{rel(ref)}: never mentioned in SKILL.md, so it will "
                    f"never be loaded"
                )

    return name


def check_plugin(plugin_dir: Path) -> tuple[str, str] | None:
    """Validate one plugins/<name>/ directory. Returns (name, version)."""
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    manifest = load_json(manifest_path)
    if manifest is None:
        return None

    name = manifest.get("name")
    version = manifest.get("version")

    for field in ("name", "version", "description", "author", "license"):
        if not manifest.get(field):
            err(f"{rel(manifest_path)}: missing '{field}'")

    if name and name != plugin_dir.name:
        err(
            f"{rel(manifest_path)}: name {name!r} does not match its "
            f"directory {plugin_dir.name!r}"
        )

    skills_dir = plugin_dir / "skills"
    skill_names: list[str] = []
    if skills_dir.is_dir():
        for child in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
            got = check_skill(child, plugin_dir.name)
            if got:
                skill_names.append(got)

    if not skill_names:
        err(
            f"{rel(plugin_dir)}: contains no valid skills — a plugin with "
            f"nothing in it installs as a no-op"
        )
    else:
        print(f"  {plugin_dir.name} v{version}: {', '.join(skill_names)}")

    return (name or plugin_dir.name, version or "")


def main() -> int:
    marketplace = load_json(MARKETPLACE)
    if marketplace is None:
        print("\n".join(errors), file=sys.stderr)
        return 1

    for field in ("name", "description", "owner", "plugins"):
        if not marketplace.get(field):
            err(f"{rel(MARKETPLACE)}: missing '{field}'")

    listed = marketplace.get("plugins") or []
    if not isinstance(listed, list):
        err(f"{rel(MARKETPLACE)}: 'plugins' must be a list")
        listed = []

    print(f"marketplace: {marketplace.get('name')}")

    on_disk = (
        sorted(p.name for p in PLUGINS_DIR.iterdir() if p.is_dir())
        if PLUGINS_DIR.is_dir()
        else []
    )

    versions: dict[str, str] = {}
    for plugin_name in on_disk:
        got = check_plugin(PLUGINS_DIR / plugin_name)
        if got:
            versions[got[0]] = got[1]

    listed_names = []
    for entry in listed:
        if not isinstance(entry, dict):
            err(f"{rel(MARKETPLACE)}: plugin entries must be objects")
            continue
        name = entry.get("name")
        listed_names.append(name)

        source = entry.get("source")
        if not source:
            err(f"{rel(MARKETPLACE)}: plugin {name!r} has no 'source'")
        elif isinstance(source, str) and source.startswith("./"):
            if not (ROOT / source).is_dir():
                err(
                    f"{rel(MARKETPLACE)}: plugin {name!r} points at "
                    f"{source}, which is not a directory"
                )

        # Version drift between the two manifests is silent and confusing:
        # the marketplace listing is what users see before installing.
        entry_version = entry.get("version")
        if name in versions and entry_version != versions[name]:
            err(
                f"{rel(MARKETPLACE)}: plugin {name!r} is listed as "
                f"v{entry_version} but its plugin.json says "
                f"v{versions[name]}"
            )

    for name in on_disk:
        if name not in listed_names:
            err(
                f"plugins/{name} exists but is not listed in "
                f"{rel(MARKETPLACE)} — it will not be installable"
            )
    for name in listed_names:
        if name and name not in on_disk:
            err(
                f"{rel(MARKETPLACE)} lists {name!r}, but plugins/{name} "
                f"does not exist"
            )

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}", file=sys.stderr)

    if errors:
        print(
            f"\n{len(errors)} error(s), {len(warnings)} warning(s)",
            file=sys.stderr,
        )
        return 1

    print(f"\nOK — {len(on_disk)} plugin(s), {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
