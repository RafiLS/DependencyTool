from src.config.config_loader import ConfigLoader
from src.domain.i_analysis_tool import IAnalysisTool
from src.domain.tool_registry import ToolRegistry
from src.domain.smell_indicator import SmellIndicator
from src.adapters.depcheck_adapter import DepcheckAdapter


@ToolRegistry.register
class DepcheckService(IAnalysisTool):

    def __init__(self):

        self._adapter = DepcheckAdapter()

        config = ConfigLoader()
        depcheck_config = config.section("smells").get("depcheck", {})

        self.unused_severity = depcheck_config.get("unused_severity", "medium")
        self.unused_description = depcheck_config.get("unused_description", "Unused dependency")

        self.missing_severity = depcheck_config.get("missing_severity", "high")
        self.missing_description = depcheck_config.get("missing_description", "Undeclared dependency")

    def name(self) -> str:
        return "depcheck"

    def analyze(self, project_path, github_repo, dependencies):

        depcheck_output = self._adapter.analyze(project_path)

        unused = (
            depcheck_output.get("dependencies", []) +
            depcheck_output.get("devDependencies", [])
        ) or []

        missing = depcheck_output.get("missing", {}) or {}

        for dep in dependencies:

            dep.is_used = True

            if dep.name in unused:
                dep.is_used = False
                dep.add_smell_indicator(
                    SmellIndicator(
                        severity=self.unused_severity,
                        description=self.unused_description
                    )
                )

            if dep.name in missing:
                dep.add_smell_indicator(
                    SmellIndicator(
                        severity=self.missing_severity,
                        description=self.missing_description
                    )
                )

        return dependencies