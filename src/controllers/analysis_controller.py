from src.services.dependency_service import DependencyService
from src.adapters.depcheck_adapter import DepcheckAdapter
from src.services.depcheck_mapper import DepcheckMapper
from src.report.report_generator import ReportGenerator
from src.report.report_writer import ReportWriter


class AnalysisController:

    def __init__(self):
        self.dependency_service = DependencyService()
        self.depcheck_adapter = DepcheckAdapter()
        self.mapper = DepcheckMapper()
        self.report_generator = ReportGenerator()
        self.report_writer = ReportWriter()

    def analyze_project(self, project_path: str, report_path="report.md"):

        # extract from json
        dependencies = self.dependency_service.extract_from_package_json(project_path)

        # run depcheck
        depcheck_output = self.depcheck_adapter.analyze(project_path)

        self.mapper.map(depcheck_output, dependencies)

        # report generator
        report = self.report_generator.generate_depcheck_report(
            depcheck_output,
            dependencies
        )

        # 5. save report
        self.report_writer.save(report, report_path)

        return report