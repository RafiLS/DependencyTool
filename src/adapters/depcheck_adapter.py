import subprocess
import json
import shutil

from src.config.config_loader import ConfigLoader


class DepcheckAdapter:

    def __init__(self):

        config = ConfigLoader()

        depcheck_config = config.section("tools").get("depcheck", {})

        self.version_command = depcheck_config["version_command"]
        self.analyze_command = depcheck_config["analyze_command"]

    def analyze(self, project_path):

        if shutil.which("npx") is None:
            print("[DEPCHECK] NPX is not installed or not available in PATH.")
            return {
                "dependencies": [],
                "devDependencies": [],
                "missing": {},
                "bloated": []
            }

        check_depcheck = subprocess.run(
            self.version_command,
            capture_output=True,
            text=True,
            shell=True
        )

        if check_depcheck.returncode != 0:
            print("[DEPCHECK] Depcheck is not installed or not working correctly.")
            return {
                "dependencies": [],
                "devDependencies": [],
                "missing": {},
                "bloated": []
            }

        result = subprocess.run(
            self.analyze_command,
            cwd=project_path,
            capture_output=True,
            text=True,
            shell=True,
            encoding="utf-8",
            errors="replace"
        )

        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()

        if not stdout:
            print(f"[DEPCHECK] empty output\n{stderr}")
            return {
                "dependencies": [],
                "devDependencies": [],
                "missing": {},
                "bloated": []
            }

        try:
            data = json.loads(stdout)

            return {
                "dependencies": data.get("dependencies", []),
                "devDependencies": data.get("devDependencies", []),
                "missing": data.get("missing", {}),
                "bloated": data.get("bloated", [])
            }

        except json.JSONDecodeError:

            print("\n[DEPCHECK] invalid JSON output")
            print(stdout)

            return {
                "dependencies": [],
                "devDependencies": [],
                "missing": {},
                "bloated": []
            }