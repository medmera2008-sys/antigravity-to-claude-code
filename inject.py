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

    if not rule_src.is_file() or not skill_src.is_dir() or not agents_src.is_file():
        print(f"Error: Missing source specification files in {repo_root}", file=sys.stderr)
        sys.exit(1)

    if not global_mode and target is None:
        print("Notice: No actions specified (--no-global without --workspace). Exiting.", file=sys.stderr)
        sys.exit(0)

    if global_mode:
        rules_dir = home / ".gemini" / "antigravity-cli" / "rules"
        skills_dir = home / ".agents" / "skills" / "code-constitution"
        rules_dir.mkdir(parents=True, exist_ok=True)
        skills_dir.mkdir(parents=True, exist_ok=True)

        shutil.copy2(rule_src, rules_dir / "antigravity-to-claude-code.md")
        shutil.copytree(skill_src, skills_dir, dirs_exist_ok=True)

        dest_home_agents = home / "AGENTS.md"
        if dest_home_agents.exists() and not dest_home_agents.is_symlink():
            shutil.copy2(dest_home_agents, home / "AGENTS.md.bak")
        shutil.copy2(agents_src, dest_home_agents)

        gemini_md = home / "GEMINI.md"
        if not gemini_md.exists() and not gemini_md.is_symlink():
            gemini_md.symlink_to(dest_home_agents)
        print("✓ Injected global Antigravity engine rules & skills.")

    if target:
        target = target.resolve()
        if target.is_file():
            print(f"Error: Target path is a file, expected a directory: {target}", file=sys.stderr)
            sys.exit(2)
        target.mkdir(parents=True, exist_ok=True)
        dest_target_agents = target / "AGENTS.md"
        if dest_target_agents.exists() and not dest_target_agents.is_symlink():
            shutil.copy2(dest_target_agents, target / "AGENTS.md.bak")
        shutil.copy2(agents_src, dest_target_agents)
        print(f"✓ Injected workspace manifest into {target}")

def main():
    parser = argparse.ArgumentParser(description="Antigravity Invariant Injector (by @medismera)")
    parser.add_argument("--workspace", "-w", type=Path, default=None, help="Target workspace directory")
    parser.add_argument("--no-global", action="store_true", help="Skip global injection")
    args = parser.parse_args()

    inject(target=args.workspace, global_mode=not args.no_global)

if __name__ == "__main__":
    main()
