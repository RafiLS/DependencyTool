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

        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()

        output = stdout or stderr

        if not output:
            return {
                "vulnerabilities": []
            }

        try:
            return json.loads(output)
        except Exception as e:
            print("\n===== JSON PARSE ERROR =====\n")
            print(e)

            return {
                "vulnerabilities": [],
                "raw_output": output
            }