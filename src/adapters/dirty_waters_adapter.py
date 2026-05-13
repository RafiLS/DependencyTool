import subprocess
import os
import glob


class DirtyWatersAdapter:

    def analyze(self, project_repo, version="main", is_local=False):

        command = [
            "dirty-waters",
            "-p", project_repo,
            "-pm", "npm",

            "--check-source-code",
            "--check-source-code-sha",
            "--check-deprecated",
            "--check-forks",
            "--check-provenance",
            "--check-code-signature",
            "--check-aliased-packages"
        ]

        if not is_local:
            command += ["-v", version]

        subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=os.environ.copy()
        )

        reports = glob.glob(
            "results/**/*_static_summary.md",
            recursive=True
        )

        if not reports:
            return None

        latest_report = max(
            reports,
            key=os.path.getctime
        )

        return latest_report