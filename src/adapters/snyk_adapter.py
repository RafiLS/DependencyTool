import subprocess
import json
import shutil

from src.config.config_loader import ConfigLoader


class SnykAdapter:

    def __init__(self):

        config = ConfigLoader()

        snyk_config = config.section("tools").get("snyk", {})

        self.version_command = snyk_config["version_command"]
        self.analyze_command = snyk_config["analyze_command"]

    def analyze(self, project_path: str):

        if shutil.which("npx") is None:
            print("[SNYK] npx is not installed or not available in PATH.")
            return {
                "status": "error",
                "tool": "snyk",
                "message": "npx is not installed or not available in PATH.",
                "vulnerabilities": []
            }

        try:
            check = subprocess.run(
                self.version_command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                shell=True
            )

            if check.returncode != 0:
                print("[SNYK] snyk is not installed or not accessible via npx.")
                return {
                    "status": "error",
                    "tool": "snyk",
                    "message": "snyk is not available",
                    "vulnerabilities": []
                }

        except Exception:
            print("[SNYK] error checking snyk installation.")
            return {
                "status": "error",
                "tool": "snyk",
                "message": "snyk check failed",
                "vulnerabilities": []
            }

        result = subprocess.run(
            self.analyze_command,
            cwd=project_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=True
        )

        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()

        output = stdout or stderr

        if not output:
            print("[SNYK] empty output")
            return {
                "status": "error",
                "tool": "snyk",
                "message": "Snyk returned empty output.",
                "vulnerabilities": []
            }

        try:
            data = json.loads(output)
            print("\n   [SNYK] tool executed successfully")
            return {
                "status": "success",
                "tool": "snyk",
                "vulnerabilities": data.get("vulnerabilities", [])
            }

        except json.JSONDecodeError:
            print("[SNYK] invalid JSON output")
            return {
                "status": "error",
                "tool": "snyk",
                "message": "Snyk output is not valid JSON. Tool may not be installed correctly.",
                "raw_output": output,
                "vulnerabilities": []
            }