import subprocess
import os
import sys
import glob


class TestE2ECLI:

    def test_cli_runs_full_pipeline(self):

        project_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "test_project")
        )

        cmd = [
            sys.executable,
            "-m",
            "src.cli",
            "analyze",
            "RafiLS/TaskReact",
            "--path",
            project_path
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        output = (result.stdout or "") + (result.stderr or "")

        assert result.returncode == 0, output

        reports = glob.glob("save_reports/*.md")

        assert len(reports) > 0, "Nenhum relatório foi gerado"

        latest = max(reports, key=os.path.getctime)

        with open(latest, "r", encoding="utf-8") as f:
            content = f.read()

        assert "Dependency Analysis Report" in content
        assert "Total Smells" in content