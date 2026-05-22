from src.config.config_loader import ConfigLoader
from src.domain.smell_indicator import SmellIndicator


class DepcheckService:

    def __init__(self):

        config = ConfigLoader()
        depcheck_config = config.section("smells").get("depcheck", {})

        self.unused_severity = depcheck_config.get("unused_severity", "medium")
        self.unused_description = depcheck_config.get("unused_description", "Unused dependency")

        self.missing_severity = depcheck_config.get("missing_severity", "high")
        self.missing_description = depcheck_config.get("missing_description", "Undeclared dependency")

    def map_results(self, depcheck_output, dependencies):

        unused = (
            depcheck_output.get("dependencies", []) +
            depcheck_output.get("devDependencies", [])
        ) or []

        missing = depcheck_output.get("missing", {}) or {}

        unused_found = []

        for dep in dependencies:

            dep.is_used = True

            # unused dependency
            if dep.name in unused:
                dep.is_used = False
                unused_found.append(dep.name)

                dep.add_smell_indicator(
                    SmellIndicator(
                        severity=self.unused_severity,
                        description=self.unused_description
                    )
                )

            # missing dependency
            if dep.name in missing:
                dep.add_smell_indicator(
                    SmellIndicator(
                        severity=self.missing_severity,
                        description=self.missing_description
                    )
                )

        return dependencies