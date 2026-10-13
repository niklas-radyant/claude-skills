#!/usr/bin/env python3
"""Extract what the human actually typed from Claude Code transcripts.

Claude Code stores every session as JSONL under ~/.claude/projects/<dir>/.
This pulls the human's own messages (not tool results, not system reminders,
not skill bodies) together with a short excerpt of the assistant turn before
each one, so corrections can be read in context.

    python3 extract-messages.py --match <project-name-substring> [--days 120] \
        [--out messages.jsonl] [--max-chars 3000]

--match selects transcript directories whose name contains the substring
(worktree sessions of the same repo usually share it). Output: one JSON
object per message, oldest first: {ts, session, text, before, long}.

Everything stays local. Transcripts can contain secrets and personal data;
the script masks common token shapes, but read the output before sharing it.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path.home() / ".claude" / "projects"

# Text that is boilerplate injected into the user role, not typed by a human.
NOISE = re.compile(
    r"^\s*(<(system-reminder|command-name|command-message|command-args|local-command|task-notification|"
    r"cross-session-message|agent-message)|Base directory for this skill:|Caveat: The messages below|"
    r"\[Request interrupted|This session is being continued from a previous conversation)",
)
SECRET = re.compile(
    r"(sk-[A-Za-z0-9_-]{16,}|ops_[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|xox[abp]-[A-Za-z0-9-]{10,}|"
    r"AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}|npg_[A-Za-z0-9]{8,}|"
    r"postgres(ql)?://[^\s\"']+)"
)


def text_of(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"
        )
    return ""


def human_texts(rec: dict) -> list[str]:
    """Typed text in a record: plain user messages, and messages queued mid-turn."""
    out = []
    if rec.get("type") == "user" and not rec.get("isMeta") and not rec.get("isSidechain"):
        msg = rec.get("message") or {}
        content = msg.get("content")
        # Tool results are user-role records too; skip them.
        if isinstance(content, list) and any(
            isinstance(b, dict) and b.get("type") == "tool_result" for b in content
        ):
            return []
        out.append(text_of(content))
    # Messages typed while the agent was working arrive as queued attachments.
    att = rec.get("attachment") or {}
    if rec.get("type") == "attachment" and att.get("type") in ("queued_command", "queued_message"):
        out.append(text_of(att.get("prompt") or att.get("content") or ""))
    return [t for t in out if t and t.strip() and not NOISE.match(t)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--match", required=True)
    ap.add_argument("--days", type=int, default=120)
    ap.add_argument("--out", default="-")
    ap.add_argument("--max-chars", type=int, default=3000)
    a = ap.parse_args()

    cutoff = time.time() - a.days * 86400
    files = [
        f
        for d in ROOT.iterdir()
        if d.is_dir() and a.match in d.name
        for f in d.glob("*.jsonl")
        if f.stat().st_mtime >= cutoff
    ]
    if not files:
        print(f"no transcripts under {ROOT} matching '{a.match}' in the last {a.days} days", file=sys.stderr)
        return 1

    rows, seen = [], set()
    for f in files:
        last_assistant = ""
        with f.open(errors="ignore") as fh:
            for line in fh:
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("type") == "assistant" and not rec.get("isSidechain"):
                    t = text_of((rec.get("message") or {}).get("content"))
                    if t.strip():
                        last_assistant = t
                    continue
                for t in human_texts(rec):
                    key = t.strip()[:200]
                    if key in seen:  # the same message pasted into several sessions
                        continue
                    seen.add(key)
                    rows.append(
                        {
                            "ts": rec.get("timestamp", ""),
                            "session": f"{f.parent.name}/{f.stem[:8]}",
                            "text": SECRET.sub("«masked»", t[: a.max_chars]),
                            "long": len(t) > a.max_chars,
                            "before": SECRET.sub("«masked»", last_assistant[-600:]),
                        }
                    )
    rows.sort(key=lambda r: r["ts"])
    out = sys.stdout if a.out == "-" else open(a.out, "w")
    for r in rows:
        out.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{len(rows)} messages from {len(files)} transcripts", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
