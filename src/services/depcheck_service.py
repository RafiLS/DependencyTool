from src.domain.smell_indicator import SmellIndicator


class DepcheckService:

    def map_results(self, depcheck_output, dependencies):

        unused = depcheck_output.get("dependencies", [])
        missing = depcheck_output.get("missing", {})

        for dep in dependencies:

            dep.is_used = True

            if dep.name in unused:
                dep.is_used = False
                dep.add_smell_indicator(
                    SmellIndicator(
                        severity="medium",
                        description="Unused dependency"
                    )
                )

            if dep.name in missing:
                dep.add_smell_indicator(
                    SmellIndicator(
                        severity="high",
                        description="Undeclared dependency"
                    )
                )