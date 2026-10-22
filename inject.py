#!/usr/bin/env python3
"""
Antigravity to Claude Code (AGY Sovereign Invariant Injector)
Author: @medismera (https://x.com/medismera)
"""

import argparse
from pathlib import Path
import shutil
import sys

def inject(target: Path, global_mode: bool = True):
    repo_root = Path(__file__).resolve().parent
    home = Path.home()

    rule_src = repo_root / "rules" / "antigravity-to-claude-code.md"
    skill_src = repo_root / "skills" / "code-constitution"
    agents_src = repo_root / "AGENTS.md"

    if global_mode:
        rules_dir = home / ".gemini" / "antigravity-cli" / "rules"
        skills_dir = home / ".agents" / "skills" / "code-constitution"
        rules_dir.mkdir(parents=True, exist_ok=True)
        skills_dir.mkdir(parents=True, exist_ok=True)

        shutil.copy2(rule_src, rules_dir / "antigravity-to-claude-code.md")
        for item in skill_src.glob("*"):
            if item.is_file():
                shutil.copy2(item, skills_dir / item.name)

        shutil.copy2(agents_src, home / "AGENTS.md")
        gemini_md = home / "GEMINI.md"
        if not gemini_md.exists():
            gemini_md.symlink_to(home / "AGENTS.md")
        print("✓ Injected global Antigravity engine rules & skills.")

    if target:
        target = target.resolve()
        target.mkdir(parents=True, exist_ok=True)
        shutil.copy2(agents_src, target / "AGENTS.md")
        print(f"✓ Injected workspace manifest into {target}")

def main():
    parser = argparse.ArgumentParser(description="Antigravity Invariant Injector (by @medismera)")
    parser.add_argument("--workspace", "-w", type=Path, default=None, help="Target workspace directory")
    parser.add_argument("--no-global", action="store_true", help="Skip global injection")
    args = parser.parse_args()

    inject(target=args.workspace, global_mode=not args.no_global)

if __name__ == "__main__":
    main()
