# Security Policy

## What the Installer Writes
By default, `install.sh` and `inject.py` write exclusively to:
- `~/.gemini/antigravity-cli/rules/antigravity-to-claude-code.md`
- `~/.agents/skills/code-constitution/SKILL.md`
- A targeted project directory via `--workspace` (creating `AGENTS.md` locally).

## Home Directory Policy
Replacing `~/AGENTS.md` is strictly opt-in via `--with-home-agents`. When specified, the installer creates a timestamped backup (`~/AGENTS.md.bak.<UTC>`) prior to modifying the file.

## Remote Fetching
Remote installation modes fetch scripts and markdown files directly from the `main` branch of this repository. They do not pin commit hashes. Inspect script contents prior to piped execution.

## Secrets and Telemetry
This project does not collect telemetry, read credentials, or transmit sensitive environmental data. All operations execute strictly within local system paths.

## Reporting Vulnerabilities
If you discover a security defect, report it privately via GitHub Security Advisories or to [@medismera](https://x.com/medismera).
