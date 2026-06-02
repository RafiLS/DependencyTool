import os
import shutil
from unittest.mock import patch, mock_open

from src.controllers.analysis_controller import AnalysisController


class TestAnalysisSystem:

    def test_full_analysis_system_runs(self, tmp_path):

        project_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "test_project")
        )

        fake_report_content = """
        Total packages in the supply chain: 10
        Packages with no source code URL: 3
        Packages with repo URL that is 404: 2
        """

        fake_report_file = tmp_path / "dirty_report.md"
        fake_report_file.write_text(fake_report_content, encoding="utf-8")

        with patch("src.adapters.depcheck_adapter.shutil.which", return_value="npx"), \
             patch("src.adapters.snyk_adapter.shutil.which", return_value="npx"), \
             patch("src.adapters.dirty_waters_adapter.shutil.which", return_value="dirty-waters"), \
             patch("src.adapters.dirty_waters_adapter.DirtyWatersAdapter.analyze",
                    return_value=str(fake_report_file)), \
             patch("subprocess.run"), \
             patch("src.report.report_writer.ReportWriter.save") as mock_save:

            controller = AnalysisController()

            report = controller.analyze_project(
                project_path=project_path,
                github_repo="RafiLS/TaskReact",
                report_path="report.md"
            )

        assert "Dependency Analysis Report" in report
        assert "Total Smells" in report
        assert mock_save.called
        if os.path.exists("results"):
            shutil.rmtree("results")