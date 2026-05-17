import subprocess
from datetime import datetime
import os

class SyftAdapter:

    def generate_sbom(
        self,
        project_path,
        output_file=None
    ):

        sbom_dir = os.path.join(project_path, "sbom")
        os.makedirs(sbom_dir, exist_ok=True)

        if output_file is None:
            today = datetime.now().strftime("%d_%m_%Y")
            output_file = f"SBOM_{today}.json"

        sbom_path = os.path.join(sbom_dir, output_file)


        for file in os.listdir(sbom_dir):
            if file.startswith("SBOM_") and file.endswith(".json"):
                try:
                    os.remove(os.path.join(sbom_dir, file))
                except Exception:
                    pass

        result = subprocess.run(
            [
                "syft",
                project_path,
                "-o",
                f"json={sbom_path}"
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        stderr = (result.stderr or "").strip()

        if result.returncode != 0:
            raise Exception(
                f"Syft failed.\nSTDERR:\n{stderr}"
            )
        
        if not os.path.exists(sbom_path):
            raise Exception("SBOM was not created by Syft")

        return sbom_path