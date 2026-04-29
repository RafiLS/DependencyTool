import subprocess
import json


class DepcheckAdapter:

    def analyze(self, project_path):

        result = subprocess.run(
            "npx depcheck --json",
            cwd=project_path,
            capture_output=True,
            text=True,
            shell=True
        )

        if not result.stdout:
            raise Exception("Depcheck did not return any output")

        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            raise Exception("Invalid Depcheck output")