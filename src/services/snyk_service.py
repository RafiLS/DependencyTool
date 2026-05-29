from src.config.config_loader import ConfigLoader
from src.domain.i_analysis_tool import IAnalysisTool
from src.domain.tool_registry import ToolRegistry
from src.adapters.snyk_adapter import SnykAdapter


@ToolRegistry.register
class SnykService(IAnalysisTool):

    def __init__(self):

        self._adapter = SnykAdapter()

        config = ConfigLoader()
        smells_config = config.section("licenses")

        self.problematic_licenses = smells_config["problematic_licenses"]

    def name(self) -> str:
        return "snyk"

    def analyze(self, project_path, github_repo, dependencies):

        snyk_data = self._adapter.analyze(project_path)

        result = {
            "install_scripts": [],
            "license_anomalies": [],
            "transitive_dependencies": []
        }

        vulnerabilities = snyk_data.get("vulnerabilities", []) or []

        seen_transitives = set()

        for v in vulnerabilities:

            title = (v.get("title") or "").lower()
            from_list = v.get("from", []) or []
            package = v.get("packageName")

            # install scripts
            if from_list and "install" in title:
                item = f"{package} - {v.get('title')}"
                if item not in result["install_scripts"]:
                    result["install_scripts"].append(item)

            # license issues
            license_issue = v.get("license")
            if license_issue in self.problematic_licenses:
                item = f"{package} - {license_issue}"
                if item not in result["license_anomalies"]:
                    result["license_anomalies"].append(item)

            # transitive dependencies
            if from_list and len(from_list) >= 3:

                chain = " > ".join(from_list)
                key = f"{package}|{chain}"

                if key not in seen_transitives:
                    seen_transitives.add(key)

                    result["transitive_dependencies"].append(
                        f"{package} (via {chain})"
                    )

        return result