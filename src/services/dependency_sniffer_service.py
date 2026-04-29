from src.services.version_classifier import VersionClassifier


class DependencySnifferService:

    def __init__(self):
        self.classifier = VersionClassifier()

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
            if not any(op in version for op in ["^", "~", ">", "<"]):
                results["pinned"].append(f"{name}@{version}")

            # url dependencies
            if "http" in version or "git+" in version:
                results["url_dependencies"].append(f"{name}@{version}")

            # restrict constraints
            if any(op in version for op in [">", "<", "^", "~"]):
                results["restrict_constraints"].append(f"{name}@{version}")

        # scripts risk
        scripts = package.get("scripts", {})
        risky = []

        dangerous_cmds = ["rm ", "sudo ", "chmod ", "del "]

        for name, cmd in scripts.items():
            if any(x in cmd for x in dangerous_cmds):
                risky.append(name)

        results["permission_constraints"] = risky

        return results