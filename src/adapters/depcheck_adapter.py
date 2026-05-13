import subprocess
import json


class DepcheckAdapter:

    def analyze(self, project_path):

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
            raise Exception(
                f"Depcheck returned empty output.\nSTDERR:\n{stderr}"
            )

        try:
            data = json.loads(stdout)

            return {
                "dependencies": data.get("dependencies", []),
                "devDependencies": data.get("devDependencies", []),
                "missing": data.get("missing", {}),
                "bloated": data.get("bloated", [])
            }

        except json.JSONDecodeError as e:

            print("\ninvalid depcheck json:")
            print(stdout)

            raise Exception(
                f"Invalid Depcheck JSON: {e}"
            )