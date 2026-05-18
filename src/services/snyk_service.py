from src.config.config_loader import ConfigLoader


class SnykService:

    def __init__(self):

        config = ConfigLoader()
        smells_config = config.section("licenses")

        self.problematic_licenses = smells_config["problematic_licenses"]

    def analyze(self, snyk_data):

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
            if from_list and len(from_list) >= 2:

                chain = " > ".join(from_list)
                key = f"{package}|{chain}"

                if key not in seen_transitives:
                    seen_transitives.add(key)

                    result["transitive_dependencies"].append(
                        f"{package} (via {chain})"
                    )

        return result