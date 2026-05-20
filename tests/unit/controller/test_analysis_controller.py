from unittest.mock import patch, Mock

from src.controllers.analysis_controller import AnalysisController

class TestAnalysisController:

    @patch("src.controllers.analysis_controller.ReportWriter")
    @patch("src.controllers.analysis_controller.ReportGenerator")
    @patch("src.controllers.analysis_controller.DirtyWatersService")
    @patch("src.controllers.analysis_controller.SnykService")
    @patch("src.controllers.analysis_controller.DependencySnifferService")
    @patch("src.controllers.analysis_controller.DepcheckService")
    @patch("src.controllers.analysis_controller.DirtyWatersAdapter")
    @patch("src.controllers.analysis_controller.SnykAdapter")
    @patch("src.controllers.analysis_controller.DependencySnifferAdapter")
    @patch("src.controllers.analysis_controller.DepcheckAdapter")
    @patch("src.controllers.analysis_controller.DependencyService")
    def test_analyze_project_flow(
        self,
        mock_dep_service,
        mock_depcheck_adapter,
        mock_sniffer_adapter,
        mock_snyk_adapter,
        mock_dirty_adapter,
        mock_depcheck_service,
        mock_sniffer_service,
        mock_snyk_service,
        mock_dirty_service,
        mock_report_generator,
        mock_report_writer
    ):

        mock_dep_service.return_value.extract_from_package_json.return_value = ["dep1"]

        mock_depcheck_adapter.return_value.analyze.return_value = {"raw": "depcheck"}
        mock_depcheck_service.return_value.map_results.return_value = {"depcheck": "ok"}

        mock_sniffer_adapter.return_value.analyze.return_value = {
            "project_meta": {}
        }
        mock_sniffer_service.return_value.analyze_constraints.return_value = {"sniffer": "ok"}

        mock_snyk_adapter.return_value.analyze.return_value = {"raw": "snyk"}
        mock_snyk_service.return_value.analyze.return_value = {"snyk": "ok"}

        mock_dirty_adapter.return_value.analyze.return_value = "report.md"
        mock_dirty_service.return_value.analyze.return_value = {"dirty": "ok"}

        mock_report_generator.return_value.generate_full_report.return_value = "FINAL_REPORT"

        mock_writer_instance = Mock()
        mock_report_writer.return_value = mock_writer_instance

        controller = AnalysisController()

        result = controller.analyze_project(
            project_path="/fake/path",
            github_repo="owner/repo",
            report_path="output.md"
        )

        assert result == "FINAL_REPORT"

        mock_writer_instance.save.assert_called_once_with(
            "FINAL_REPORT",
            "output.md"
        )