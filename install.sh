#!/usr/bin/env bash
set -euo pipefail

WITH_HOME_AGENTS=false
DRY_RUN=false

for arg in "$@"; do
  case "$arg" in
    --with-home-agents)
      WITH_HOME_AGENTS=true
      ;;
    --dry-run)
      DRY_RUN=true
      ;;
    -h|--help)
      echo "Usage: $0 [--with-home-agents] [--dry-run]"
      exit 0
      ;;
    *)
      echo "Unknown option: $arg" >&2
      exit 1
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd || echo "")"
LOCAL_MODE=false
if [ -n "${SCRIPT_DIR}" ] && [ -f "${SCRIPT_DIR}/rules/antigravity-to-claude-code.md" ]; then
  LOCAL_MODE=true
fi

AGY_RULES_DIR="${HOME}/.gemini/antigravity-cli/rules"
AGY_SKILLS_DIR="${HOME}/.agents/skills/code-constitution"
BASE_URL="https://raw.githubusercontent.com/medmera2008-sys/antigravity-to-claude-code/main"

RULE_SRC="${SCRIPT_DIR}/rules/antigravity-to-claude-code.md"
SKILL_SRC="${SCRIPT_DIR}/skills/code-constitution/SKILL.md"
AGENTS_SRC="${SCRIPT_DIR}/AGENTS.md"

DEST_RULE="${AGY_RULES_DIR}/antigravity-to-claude-code.md"
DEST_SKILL="${AGY_SKILLS_DIR}/SKILL.md"
DEST_HOME_AGENTS="${HOME}/AGENTS.md"
DEST_HOME_GEMINI="${HOME}/GEMINI.md"

if [ "${DRY_RUN}" = true ]; then
  echo "[dry-run] mkdir -p ${AGY_RULES_DIR}"
  echo "[dry-run] mkdir -p ${AGY_SKILLS_DIR}"
  if [ "${LOCAL_MODE}" = true ]; then
    echo "[dry-run] cp ${RULE_SRC} ${DEST_RULE}"
    echo "[dry-run] cp ${SKILL_SRC} ${DEST_SKILL}"
  else
    echo "[dry-run] fetch ${BASE_URL}/rules/antigravity-to-claude-code.md -> ${DEST_RULE}"
    echo "[dry-run] fetch ${BASE_URL}/skills/code-constitution/SKILL.md -> ${DEST_SKILL}"
  fi
  if [ "${WITH_HOME_AGENTS}" = true ]; then
    TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
    if [ -e "${DEST_HOME_AGENTS}" ] || [ -L "${DEST_HOME_AGENTS}" ]; then
      echo "[dry-run] cp ${DEST_HOME_AGENTS} ${DEST_HOME_AGENTS}.bak.${TIMESTAMP}"
    fi
    if [ "${LOCAL_MODE}" = true ]; then
      echo "[dry-run] cp ${AGENTS_SRC} ${DEST_HOME_AGENTS}"
    else
      echo "[dry-run] fetch ${BASE_URL}/AGENTS.md -> ${DEST_HOME_AGENTS}"
    fi
    if [ ! -e "${DEST_HOME_GEMINI}" ] && [ ! -L "${DEST_HOME_GEMINI}" ]; then
      echo "[dry-run] ln -s ${DEST_HOME_AGENTS} ${DEST_HOME_GEMINI}"
    fi
  fi
  exit 0
fi

mkdir -p "${AGY_RULES_DIR}"
mkdir -p "${AGY_SKILLS_DIR}"

if [ "${LOCAL_MODE}" = true ]; then
  cp -f "${RULE_SRC}" "${DEST_RULE}"
  cp -f "${SKILL_SRC}" "${DEST_SKILL}"
else
  curl -fsSL "${BASE_URL}/rules/antigravity-to-claude-code.md" -o "${DEST_RULE}"
  curl -fsSL "${BASE_URL}/skills/code-constitution/SKILL.md" -o "${DEST_SKILL}"
fi

if [ "${WITH_HOME_AGENTS}" = true ]; then
  TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
  if [ -e "${DEST_HOME_AGENTS}" ] || [ -L "${DEST_HOME_AGENTS}" ]; then
    cp "${DEST_HOME_AGENTS}" "${DEST_HOME_AGENTS}.bak.${TIMESTAMP}"
  fi
  if [ "${LOCAL_MODE}" = true ]; then
    cp -f "${AGENTS_SRC}" "${DEST_HOME_AGENTS}"
  else
    curl -fsSL "${BASE_URL}/AGENTS.md" -o "${DEST_HOME_AGENTS}"
  fi
  if [ ! -e "${DEST_HOME_GEMINI}" ] && [ ! -L "${DEST_HOME_GEMINI}" ]; then
    ln -s "${DEST_HOME_AGENTS}" "${DEST_HOME_GEMINI}"
  fi
fi
