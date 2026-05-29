import os

from src.config.config_loader import ConfigLoader
from src.services.dependency_service import DependencyService
from src.adapters.syft_adapter import SyftAdapter
from src.services.syft_service import SyftService
from src.domain.tool_registry import ToolRegistry
from src.report.report_generator import ReportGenerator
from src.report.report_writer import ReportWriter


class AnalysisController:

    def __init__(self, tools=None):
        self.config = ConfigLoader()
        self.dependency_service = DependencyService()

        self.tools = tools if tools is not None else ToolRegistry.get_all()

        self.syft_service = SyftService()

        self.report_generator = ReportGenerator()
        self.report_writer = ReportWriter()

    def analyze_project(
        self,
        project_path: str,
        github_repo: str,
        report_path: str = "report.md"
    ):

        project_name = github_repo.split("/")[-1]

        output_dir = os.path.join(
            "save_reports",
            project_name
        )

        os.makedirs(output_dir, exist_ok=True)

        syft_adapter = SyftAdapter(output_dir=output_dir)

        sbom_path = syft_adapter.generate_sbom(project_path)
        sbom_data = self.syft_service.analyze(sbom_path)

        dependencies = self.dependency_service.extract_from_package_json(
            project_path
        )

        results = {
            tool.name(): tool.analyze(
                project_path,
                github_repo,
                dependencies
            )
            for tool in self.tools
        }

        report = self.report_generator.generate_full_report(
            results=results,
            dependencies=dependencies,
            project_repo=github_repo,
            sbom=sbom_data,
            sbom_path=sbom_path
        )

        self.report_writer.save(
            report,
            project_name,
            filename=report_path
        )

        return report