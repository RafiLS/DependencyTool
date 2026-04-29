import subprocess
import json


class SnykAdapter:

    def analyze(self, project_path: str):

        result = subprocess.run(
            ["npx", "snyk", "test", "--json"],
            cwd=project_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=True
        )

        stdout = result.stdout or ""
        stderr = result.stderr or ""

        output = stdout.strip()

        if not output:
            output = stderr.strip()

        if not output:
            return {
                "vulnerabilities": []
            }

        try:
            return json.loads(output)
        except Exception:
            return {
                "vulnerabilities": []
            }