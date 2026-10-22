#!/usr/bin/env python3
"""
Antigravity to Claude Code (AGY Invariant Injector)
Automated injection engine that embeds code-constitution rules and swarm constraints
into Google Antigravity (AGY) system rules, skills, and workspace configurations.
"""

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import sys

def inject(workspace: Path, global_mode: bool, with_home_agents: bool, dry_run: bool):
    repo_root = Path(__file__).resolve().parent
    home = Path.home()

    rule_src = repo_root / "rules" / "antigravity-to-claude-code.md"
    skill_src = repo_root / "skills" / "code-constitution" / "SKILL.md"
    agents_src = repo_root / "AGENTS.md"

    if not rule_src.is_file() or not skill_src.is_file() or not agents_src.is_file():
        print(f"Error: Required source files missing in {repo_root}", file=sys.stderr)
        sys.exit(1)

    if workspace is not None:
        if not workspace.is_dir():
            print(f"Error: Workspace path does not exist or is not a directory: {workspace}", file=sys.stderr)
            sys.exit(2)

    agy_rules_dir = home / ".gemini" / "antigravity-cli" / "rules"
    agy_skills_dir = home / ".agents" / "skills" / "code-constitution"
    dest_rule = agy_rules_dir / "antigravity-to-claude-code.md"
    dest_skill = agy_skills_dir / "SKILL.md"

    dest_home_agents = home / "AGENTS.md"
    dest_home_gemini = home / "GEMINI.md"

    if dry_run:
        if global_mode:
            print(f"[dry-run] mkdir -p {agy_rules_dir}")
            print(f"[dry-run] cp {rule_src} {dest_rule}")
            print(f"[dry-run] mkdir -p {agy_skills_dir}")
            print(f"[dry-run] cp {skill_src} {dest_skill}")
        if with_home_agents:
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            if dest_home_agents.exists() or dest_home_agents.is_symlink():
                print(f"[dry-run] cp {dest_home_agents} {dest_home_agents}.bak.{timestamp}")
            print(f"[dry-run] cp {agents_src} {dest_home_agents}")
            if not dest_home_gemini.exists() and not dest_home_gemini.is_symlink():
                print(f"[dry-run] ln -s {dest_home_agents} {dest_home_gemini}")
        if workspace is not None:
            dest_workspace_agents = workspace / "AGENTS.md"
            print(f"[dry-run] cp {agents_src} {dest_workspace_agents}")
        return

    if global_mode:
        agy_rules_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(rule_src, dest_rule)
        agy_skills_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(skill_src, dest_skill)

    if with_home_agents:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        if dest_home_agents.exists() or dest_home_agents.is_symlink():
            shutil.copy2(dest_home_agents, dest_home_agents.with_name(f"AGENTS.md.bak.{timestamp}"))
        shutil.copy2(agents_src, dest_home_agents)
        if not dest_home_gemini.exists() and not dest_home_gemini.is_symlink():
            dest_home_gemini.symlink_to(dest_home_agents)

    if workspace is not None:
        dest_workspace_agents = workspace / "AGENTS.md"
        shutil.copy2(agents_src, dest_workspace_agents)

def main():
    parser = argparse.ArgumentParser(description="Inject code-constitution rules and swarm constraints into Google Antigravity")
    parser.add_argument("--workspace", "-w", type=Path, default=Path.cwd(), help="Target workspace directory (default: current directory)")
    parser.add_argument("--global", dest="global_mode", action="store_true", help="Inject rule and skill into global Antigravity directories")
    parser.add_argument("--with-home-agents", action="store_true", help="Replace ~/AGENTS.md with backup and maintain ~/GEMINI.md symlink")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without modifying files")
    args = parser.parse_args()

    inject(
        workspace=args.workspace,
        global_mode=args.global_mode,
        with_home_agents=args.with_home_agents,
        dry_run=args.dry_run,
    )

if __name__ == "__main__":
    main()
