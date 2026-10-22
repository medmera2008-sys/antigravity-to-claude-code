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

mkdir -p "${AGY_RULES_DIR}"
mkdir -p "${AGY_SKILLS_DIR}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd || echo "")"
LOCAL_MODE=false
if [ -n "${SCRIPT_DIR}" ] && [ -f "${SCRIPT_DIR}/rules/antigravity-to-claude-code.md" ]; then
    LOCAL_MODE=true
fi

if [ "${LOCAL_MODE}" = true ]; then
    echo -e "[*] Local repository detected. Deploying directly from local sources..."
    cp -f "${SCRIPT_DIR}/rules/antigravity-to-claude-code.md" "${AGY_RULES_DIR}/antigravity-to-claude-code.md"
    cp -rf "${SCRIPT_DIR}/skills/code-constitution/"* "${AGY_SKILLS_DIR}/"
    cp -f "${SCRIPT_DIR}/AGENTS.md" "${HOME}/AGENTS.md"
else
    echo -e "[*] Remote installation mode. Fetching from repository..."
    curl -fsSL "${BASE_URL}/rules/antigravity-to-claude-code.md" -o "${AGY_RULES_DIR}/antigravity-to-claude-code.md"
    curl -fsSL "${BASE_URL}/skills/code-constitution/SKILL.md" -o "${AGY_SKILLS_DIR}/SKILL.md"
    curl -fsSL "${BASE_URL}/AGENTS.md" -o "${HOME}/AGENTS.md"
fi

if [ ! -f "${HOME}/GEMINI.md" ]; then
    ln -sf "${HOME}/AGENTS.md" "${HOME}/GEMINI.md"
fi

echo -e "\n${BOLD}${GREEN}✓ Injection Complete!${NC}"
echo -e "Google Antigravity (AGY) now enforces deterministic AST invariants and swarm protocols on all sessions.\n"
