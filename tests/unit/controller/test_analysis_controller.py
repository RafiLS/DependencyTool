from unittest.mock import Mock, patch

from src.controllers.analysis_controller import AnalysisController


class TestAnalysisController:

    @patch("src.controllers.analysis_controller.os.makedirs")
    @patch("src.controllers.analysis_controller.ReportWriter")
    @patch("src.controllers.analysis_controller.ReportGenerator")
    @patch("src.controllers.analysis_controller.SyftService")
    @patch("src.controllers.analysis_controller.SyftAdapter")
    @patch("src.controllers.analysis_controller.DependencyService")
    def test_analyze_project_flow(
        self,
        mock_dependency_service,
        mock_syft_adapter,
        mock_syft_service,
        mock_report_generator,
        mock_report_writer,
        mock_makedirs
    ):

        mock_dependency_service.return_value.extract_from_package_json.return_value = [
            "dep1"
        ]

        mock_syft_adapter.return_value.generate_sbom.return_value = (
            "/fake/sbom.json"
        )

        mock_syft_service.return_value.analyze.return_value = {
            "packages": []
        }

        mock_tool = Mock()
        mock_tool.name.return_value = "FakeTool"
        mock_tool.analyze.return_value = {
            "result": "ok"
        }

        mock_report_generator.return_value.generate_full_report.return_value = (
            "FINAL_REPORT"
        )

        controller = AnalysisController(
            tools=[mock_tool]
        )

        result = controller.analyze_project(
            project_path="/fake/path",
            github_repo="owner/repo",
            report_path="output.md"
        )

        assert result == "FINAL_REPORT"

        mock_tool.analyze.assert_called_once_with(
            "/fake/path",
            "owner/repo",
            ["dep1"]
        )

        mock_report_generator.return_value.generate_full_report.assert_called_once()

        mock_report_writer.return_value.save.assert_called_once_with(
            "FINAL_REPORT",
            "repo",
            filename="output.md"
        )