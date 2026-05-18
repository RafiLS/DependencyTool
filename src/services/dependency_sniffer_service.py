from src.config.config_loader import ConfigLoader
from src.services.version_classifier import VersionClassifier


class DependencySnifferService:

    def __init__(self):

        config = ConfigLoader()
        sniffer_config = config.section("smells").get("sniffer", {})

        self.classifier = VersionClassifier()

        self.dangerous_commands = sniffer_config["dangerous_commands"]
        self.constraint_operators = sniffer_config["constraint_operators"]
        self.url_keywords = sniffer_config["url_keywords"]

    def analyze_constraints(self, data):

        package = data["package_json"]

        deps = package.get("dependencies", {})
        dev_deps = package.get("devDependencies", {})

        results = {
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

            # risk classification
            risk = self.classifier.classify(version)

            results["version_risks"].append({
                "dependency": name,
                "version": version,
                "risk": risk
            })

            # pinned
            if not any(op in version for op in self.constraint_operators):
                results["pinned"].append(f"{name}@{version}")

            # url dependencies
            if any(k in version for k in self.url_keywords):
                results["url_dependencies"].append(f"{name}@{version}")

            # restrict constraints
            if any(op in version for op in self.constraint_operators):
                results["restrict_constraints"].append(f"{name}@{version}")

        scripts = package.get("scripts", {})
        risky = []

        for name, cmd in scripts.items():
            if any(x in cmd for x in self.dangerous_commands):
                risky.append(name)

        results["permission_constraints"] = risky

        return results