from src.config.config_loader import ConfigLoader
from src.domain.i_analysis_tool import IAnalysisTool
from src.domain.tool_registry import ToolRegistry
from src.adapters.dependency_sniffer_adapter import DependencySnifferAdapter
from src.services.version_classifier import VersionClassifier


@ToolRegistry.register
class DependencySnifferService(IAnalysisTool):

    def __init__(self):
        self._adapter = DependencySnifferAdapter()
        self.classifier = VersionClassifier()

        config = ConfigLoader()
        sniffer_config = config.section("smells").get("sniffer", {})

        self.dangerous_commands = sniffer_config.get("dangerous_commands", [])
        self.constraint_operators = sniffer_config.get("constraint_operators", [])
        self.url_keywords = sniffer_config.get("url_keywords", [])

    def name(self) -> str:
        return "dependency_sniffer"

    def analyze(self, project_path, github_repo, dependencies):

        data = self._adapter.analyze(project_path)

        package = data.get("package_json", {})
        project_meta = data.get("project_meta", {
            "has_package_json": False,
            "has_package_lock": False
        })

        deps = package.get("dependencies", {})
        dev_deps = package.get("devDependencies", {})
        scripts = package.get("scripts", {})

        results = {
            "project_meta": project_meta,
            "pinned": [],
            "url_dependencies": [],
            "restrict_constraints": [],
            "permission_constraints": [],
            "version_risks": []
        }

        all_deps = {**deps, **dev_deps}

        for name, version in all_deps.items():

            if not version:
                continue

            risk = self.classifier.classify(version)

            results["version_risks"].append({
                "dependency": name,
                "version": version,
                "risk": risk
            })
            if not any(op in version for op in self.constraint_operators):
                results["pinned"].append(f"{name}@{version}")

            if any(k in version for k in self.url_keywords):
                results["url_dependencies"].append(f"{name}@{version}")

            if any(op in version for op in self.constraint_operators):
                results["restrict_constraints"].append(f"{name}@{version}")

        risky = [
            name for name, cmd in scripts.items()
            if any(x in cmd for x in self.dangerous_commands)
        ]
        results["permission_constraints"] = risky

        return results