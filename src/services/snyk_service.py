class SnykService:

    def analyze(self, snyk_data):

        result = {
            "install_scripts": [],
            "license_anomalies": [],
            "transitive_dependencies": []
        }

        vulnerabilities = snyk_data.get("vulnerabilities", []) or []

        for v in vulnerabilities:

            title = (v.get("title") or "").lower()
            from_list = v.get("from", []) or []
            package = v.get("packageName")

            # install scripts
            if from_list and "install" in title:
                result["install_scripts"].append(
                    f"{package} - {v.get('title')}"
                )

            # license issues
            license_issue = v.get("license")
            if license_issue in {"GPL", "AGPL", "UNKNOWN"}:
                result["license_anomalies"].append(
                    f"{package} - {license_issue}"
                )

            # transitive dependencies
            if from_list and len(from_list) >= 2:
                chain = " > ".join(from_list)
                result["transitive_dependencies"].append(
                f"{package} (via {chain})"
            )
        return result