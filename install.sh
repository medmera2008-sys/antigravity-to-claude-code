#!/usr/bin/env bash
set -euo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "\n${BOLD}${CYAN}⚡ Antigravity to Claude Code: Direct Invariant Injector ⚡${NC}\n"

# Target directories
AGY_RULES_DIR="${HOME}/.gemini/antigravity-cli/rules"
AGY_SKILLS_DIR="${HOME}/.agents/skills/code-constitution"
BASE_URL="https://raw.githubusercontent.com/medmera2008-sys/antigravity-to-claude-code/main"

echo -e "[*] Creating configuration directories..."
mkdir -p "${AGY_RULES_DIR}"
mkdir -p "${AGY_SKILLS_DIR}"

echo -e "[*] Injecting native rules into Antigravity system engine..."
curl -fsSL "${BASE_URL}/rules/antigravity-to-claude-code.md" -o "${AGY_RULES_DIR}/antigravity-to-claude-code.md"

echo -e "[*] Injecting sovereign skill into global agents registry..."
curl -fsSL "${BASE_URL}/skills/code-constitution/SKILL.md" -o "${AGY_SKILLS_DIR}/SKILL.md"

echo -e "[*] Injecting workspace invariant manifest into home directory..."
curl -fsSL "${BASE_URL}/AGENTS.md" -o "${HOME}/AGENTS.md"

echo -e "\n${BOLD}${GREEN}✓ Injection Complete!${NC}"
echo -e "Google Antigravity (AGY) now enforces deterministic AST invariants and swarm protocols on all sessions.\n"
