from src.domain.smell_indicator import SmellIndicator


class DepcheckService:

    def map_results(self, depcheck_output, dependencies):

        unused = depcheck_output.get("dependencies", []) or []
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
                        severity="medium",
                        description="Unused dependency"
                    )
                )

            # missing dependency
            if dep.name in missing:
                dep.add_smell_indicator(
                    SmellIndicator(
                        severity="high",
                        description="Undeclared dependency"
                    )
                )
        return dependencies