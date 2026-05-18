import subprocess
import json
import shutil


class SnykAdapter:

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
                ["npx", "snyk", "--version"],
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
            ["npx", "snyk", "test", "--json"],
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