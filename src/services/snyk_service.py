class SnykService:

    def analyze(self, snyk_data):

        result = {
            "install_scripts": [],
            "license_anomalies": [],
            "transitive_dependencies": []
        }

        vulnerabilities = snyk_data.get("vulnerabilities", [])

        for v in vulnerabilities:

            title = (v.get("title") or "").lower()
            from_list = v.get("from", [])

            # install scripts
            if from_list and "install" in title:
                result["install_scripts"].append(
                    f"{v.get('packageName')} - {v.get('title')}"
                )

            # license issues
            license_issue = v.get("license")
            if license_issue in {"GPL", "AGPL", "UNKNOWN"}:
                result["license_anomalies"].append(
                    f"{v.get('packageName')} - {license_issue}"
                )

            # transitive dependencies
            if len(from_list) > 2:
                result["transitive_dependencies"].append(
                    f"{v.get('packageName')} (transitive)"
                )

        return result