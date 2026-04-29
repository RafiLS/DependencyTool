from src.services.dependency_service import DependencyService

from src.adapters.depcheck_adapter import DepcheckAdapter
from src.adapters.dependency_sniffer_adapter import DependencySnifferAdapter
from src.adapters.snyk_adapter import SnykAdapter

from src.services.depcheck_service import DepcheckService
from src.services.dependency_sniffer_service import DependencySnifferService
from src.services.snyk_service import SnykService

from src.report.report_generator import ReportGenerator
from src.report.report_writer import ReportWriter


class AnalysisController:

    def __init__(self):

        self.dependency_service = DependencyService()

        self.depcheck_adapter = DepcheckAdapter()
        self.sniffer_adapter = DependencySnifferAdapter()
        self.snyk_adapter = SnykAdapter()

        self.depcheck_service = DepcheckService()
        self.sniffer_service = DependencySnifferService()
        self.snyk_service = SnykService()

        self.report_generator = ReportGenerator()
        self.report_writer = ReportWriter()

    def analyze_project(self, project_path: str, report_path="report.md"):

        dependencies = self.dependency_service.extract_from_package_json(project_path)

        # DEPCHECK
        depcheck_output = self.depcheck_adapter.analyze(project_path)
        self.depcheck_service.map_results(depcheck_output, dependencies)

        # SNIFFER
        sniffer_raw = self.sniffer_adapter.analyze(project_path)
        sniffer_results = self.sniffer_service.analyze_constraints(sniffer_raw)

        # SNYK
        snyk_raw = self.snyk_adapter.analyze(project_path)
        snyk_results = self.snyk_service.analyze(snyk_raw)

        # REPORT
        report = self.report_generator.generate_full_report(
            depcheck_output,
            sniffer_results,
            snyk_results,
            dependencies
        )

        self.report_writer.save(report, report_path)

        return report