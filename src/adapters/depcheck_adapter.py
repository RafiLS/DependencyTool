import subprocess
import json
import shutil


class DepcheckAdapter:

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
            "npx depcheck --version",
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
            "npx depcheck --json",
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

        except json.JSONDecodeError as e:

            print("\n[DEPCHECK] invalid JSON output")
            print(stdout)

            return {
                "dependencies": [],
                "devDependencies": [],
                "missing": {},
                "bloated": []
            }