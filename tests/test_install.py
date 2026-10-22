#!/usr/bin/env python3
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent
INSTALL_SH = REPO_ROOT / "install.sh"
INJECT_PY = REPO_ROOT / "inject.py"

class TestInstallerAndInjector(unittest.TestCase):
    def setUp(self):
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.temp_dir = Path(self.temp_dir_obj.name)
        self.temp_home = self.temp_dir / "home"
        self.temp_home.mkdir(parents=True, exist_ok=True)
        self.env = {**os.environ, "HOME": str(self.temp_home)}

    def tearDown(self):
        self.temp_dir_obj.cleanup()

    def test_01_install_default_keeps_home_agents(self):
        home_agents = self.temp_home / "AGENTS.md"
        home_agents.write_text("KEEP", encoding="utf-8")

        res = subprocess.run([str(INSTALL_SH)], env=self.env, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)

        self.assertEqual(home_agents.read_text(encoding="utf-8"), "KEEP")
        self.assertFalse((self.temp_home / "GEMINI.md").exists())
        self.assertTrue((self.temp_home / ".gemini" / "antigravity-cli" / "rules" / "antigravity-to-claude-code.md").is_file())
        self.assertTrue((self.temp_home / ".agents" / "skills" / "code-constitution" / "SKILL.md").is_file())

    def test_02_install_dry_run(self):
        home_agents = self.temp_home / "AGENTS.md"
        home_agents.write_text("KEEP", encoding="utf-8")

        res = subprocess.run([str(INSTALL_SH), "--dry-run"], env=self.env, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)

        self.assertEqual(home_agents.read_text(encoding="utf-8"), "KEEP")
        self.assertFalse((self.temp_home / ".gemini" / "antigravity-cli" / "rules" / "antigravity-to-claude-code.md").exists())
        self.assertFalse((self.temp_home / ".agents" / "skills" / "code-constitution" / "SKILL.md").exists())

    def test_03_install_with_home_agents_backup_and_symlink(self):
        home_agents = self.temp_home / "AGENTS.md"
        home_agents.write_text("KEEP", encoding="utf-8")

        res = subprocess.run([str(INSTALL_SH), "--with-home-agents"], env=self.env, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)

        self.assertNotEqual(home_agents.read_text(encoding="utf-8"), "KEEP")
        backups = list(self.temp_home.glob("AGENTS.md.bak.*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(encoding="utf-8"), "KEEP")

        gemini_md = self.temp_home / "GEMINI.md"
        self.assertTrue(gemini_md.is_symlink())
        self.assertEqual(os.readlink(gemini_md), str(home_agents))

    def test_04_install_second_run_with_existing_gemini(self):
        home_agents = self.temp_home / "AGENTS.md"
        home_agents.write_text("KEEP", encoding="utf-8")
        gemini_md = self.temp_home / "GEMINI.md"
        gemini_md.write_text("EXISTING_GEMINI", encoding="utf-8")

        res = subprocess.run([str(INSTALL_SH), "--with-home-agents"], env=self.env, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)

        self.assertFalse(gemini_md.is_symlink())
        self.assertEqual(gemini_md.read_text(encoding="utf-8"), "EXISTING_GEMINI")

    def test_05_inject_nonexistent_workspace_exits_2(self):
        non_existent = self.temp_dir / "non_existent_dir"
        res = subprocess.run(
            [sys.executable, str(INJECT_PY), "--workspace", str(non_existent)],
            env=self.env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 2)
        self.assertFalse(non_existent.exists())

    def test_06_inject_workspace_existing_dir(self):
        workspace = self.temp_dir / "project"
        workspace.mkdir(parents=True, exist_ok=True)
        home_agents = self.temp_home / "AGENTS.md"
        home_agents.write_text("KEEP", encoding="utf-8")

        res = subprocess.run(
            [sys.executable, str(INJECT_PY), "--workspace", str(workspace)],
            env=self.env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0)
        self.assertTrue((workspace / "AGENTS.md").is_file())
        self.assertEqual(home_agents.read_text(encoding="utf-8"), "KEEP")
        self.assertFalse((self.temp_home / ".gemini" / "antigravity-cli" / "rules" / "antigravity-to-claude-code.md").exists())

    def test_07_inject_global_mode_keeps_home_agents(self):
        home_agents = self.temp_home / "AGENTS.md"
        home_agents.write_text("KEEP", encoding="utf-8")
        workspace = self.temp_dir / "dummy_ws"
        workspace.mkdir(parents=True, exist_ok=True)

        res = subprocess.run(
            [sys.executable, str(INJECT_PY), "--global", "--workspace", str(workspace)],
            env=self.env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0)
        self.assertTrue((self.temp_home / ".gemini" / "antigravity-cli" / "rules" / "antigravity-to-claude-code.md").is_file())
        self.assertTrue((self.temp_home / ".agents" / "skills" / "code-constitution" / "SKILL.md").is_file())
        self.assertEqual(home_agents.read_text(encoding="utf-8"), "KEEP")

    def test_08_inject_dry_run_workspace(self):
        workspace = self.temp_dir / "project_dry"
        workspace.mkdir(parents=True, exist_ok=True)

        res = subprocess.run(
            [sys.executable, str(INJECT_PY), "--dry-run", "--workspace", str(workspace)],
            env=self.env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0)
        self.assertFalse((workspace / "AGENTS.md").exists())

if __name__ == "__main__":
    unittest.main()
