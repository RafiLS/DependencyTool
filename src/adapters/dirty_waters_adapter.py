import subprocess
import os
import glob
import shutil


class DirtyWatersAdapter:

    def analyze(self, project_repo, version="main", is_local=False):

        if shutil.which("dirty-waters") is None:
            print("[DIRTY WATERS] tool is not installed or not in PATH")
            return None

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

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=os.environ.copy()
        )

        if result.returncode != 0:
            print("[DIRTY WATERS] tool failed to execute")
            print(result.stderr)
            return None

        reports = glob.glob(
            "results/**/*_static_summary.md",
            recursive=True
        )

        if not reports:
            print("[DIRTY WATERS] no report generated")
            return None

        latest_report = max(
            reports,
            key=os.path.getctime
        )

        return latest_report