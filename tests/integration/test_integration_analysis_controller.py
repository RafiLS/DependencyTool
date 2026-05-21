import os
import glob
from unittest.mock import patch

from src.controllers.analysis_controller import AnalysisController


class TestAnalysisControllerIntegration:

    def test_full_analysis_detects_smells(self):

        base_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "test_project")
        )

        with patch("src.report.report_writer.ReportWriter.save") as mock_save:

            controller = AnalysisController()

            report = controller.analyze_project(
                project_path=base_path,
                github_repo="RafiLS/TaskReact",
                report_path="test_report.md"
            )

        assert "# Dependency Analysis Report" in report
        assert "Project Structure" in report

        assert (
            "Unused dependencies" in report
            or "Unused dependencies/Bloated Dependencies" in report
        )

        assert "Missing dependencies" in report
        assert "Version Risk Analysis" in report
        assert "Total Smells" in report
        assert len(report) > 100

        assert "lodash" in report or "react" in report or "axios" in report

        mock_save.assert_called_once()