#!/usr/bin/env python3
"""
Antigravity to Claude Code (AGY Invariant Injector)
Automated injection engine that embeds deterministic code invariants and swarm governance
directly into Google Antigravity (AGY) system rules, skills, and workspace configurations.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

def print_status(msg: str, success: bool = True):
    symbol = "✓" if success else "✗"
    color = "\033[32m" if success else "\033[31m"
    reset = "\033[0m"
    print(f" {color}{symbol}{reset} {msg}")

def inject(target_workspace: Path, global_mode: bool = True):
    repo_root = Path(__file__).resolve().parent
    home = Path.home()
    
    rules_src = repo_root / "rules" / "antigravity-to-claude-code.md"
    skill_src = repo_root / "skills" / "code-constitution"
    agents_src = repo_root / "AGENTS.md"

    if not rules_src.exists() or not skill_src.exists():
        print(f"Error: Required source files missing in {repo_root}", file=sys.stderr)
        sys.exit(1)

    print("\n\033[1;36m⚡ Injecting Sovereign Invariants into Google Antigravity (AGY)...\033[0m\n")

    # 1. Global Rule Injection (AGY native rules directory)
    if global_mode:
        agy_rules_dir = home / ".gemini" / "antigravity-cli" / "rules"
        agy_rules_dir.mkdir(parents=True, exist_ok=True)
        dest_rule = agy_rules_dir / "antigravity-to-claude-code.md"
        shutil.copy2(rules_src, dest_rule)
        print_status(f"Injected global rule: {dest_rule}")

        # Global Skills Injection
        global_skills_dir = home / ".agents" / "skills" / "code-constitution"
        global_skills_dir.mkdir(parents=True, exist_ok=True)
        for item in skill_src.glob("*"):
            if item.is_file():
                shutil.copy2(item, global_skills_dir / item.name)
        print_status(f"Injected global skill: {global_skills_dir}")

        # Global Invariant Manifest
        dest_global_agents = home / "AGENTS.md"
        shutil.copy2(agents_src, dest_global_agents)
        print_status(f"Injected global manifest: {dest_global_agents}")

        dest_gemini = home / "GEMINI.md"
        if not dest_gemini.exists():
            dest_gemini.symlink_to(dest_global_agents)
            print_status(f"Symlinked manifest to GEMINI.md: {dest_gemini}")

    # 2. Workspace Injection (AGENTS.md)
    if target_workspace:
        target_workspace = target_workspace.resolve()
        target_workspace.mkdir(parents=True, exist_ok=True)
        dest_agents = target_workspace / "AGENTS.md"
        shutil.copy2(agents_src, dest_agents)
        print_status(f"Injected workspace instructions: {dest_agents}")

    print("\n\033[1;32m✓ Injection complete. Antigravity will enforce these invariants on every session.\033[0m\n")

def main():
    parser = argparse.ArgumentParser(description="Inject Sovereign Code Invariants into Antigravity (AGY)")
    parser.add_argument("--workspace", "-w", type=Path, default=Path.cwd(), help="Target workspace directory")
    parser.add_argument("--no-global", action="store_true", help="Skip global ~/.gemini and ~/.agents injection")
    args = parser.parse_args()

    inject(target_workspace=args.workspace, global_mode=not args.no_global)

if __name__ == "__main__":
    main()
