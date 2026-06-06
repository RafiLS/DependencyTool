import subprocess
import os
import shutil
from datetime import datetime


class SyftAdapter:

    def __init__(self, output_dir="save_reports"):
        self.output_dir = output_dir

    def generate_sbom(self, project_path: str):

        if shutil.which("syft") is None:
            print("[SYFT] Syft is not installed or not available in PATH.")
            return None

        os.makedirs(self.output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

        sbom_file = os.path.join(
            self.output_dir,
            f"sbom_{timestamp}.json"
        )
        command = [
            "syft",
            project_path,
            "-o",
            "json"
        ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8"
            )

        except Exception as e:
            print(f"[SYFT] execution error: {e}")
            return None

        if result.returncode != 0:
            print("[SYFT] failed to generate SBOM")
            print(result.stderr)
            return None

        print("\n   [SYFT] tool executed successfully")

        with open(sbom_file, "w", encoding="utf-8") as f:
            f.write(result.stdout)

        return sbom_file