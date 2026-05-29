import json
import os
from collections import Counter


class SyftService:

    def analyze(self, sbom_path):

        if not sbom_path or not os.path.exists(sbom_path):
            return {}

        with open(sbom_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        artifacts = data.get("artifacts", [])

        licenses = []
        no_license = []

        for artifact in artifacts:

            artifact_licenses = artifact.get("licenses", [])

            if not artifact_licenses:
                no_license.append(artifact.get("name"))
                continue

            for lic in artifact_licenses:
                value = lic.get("value")

                if value:
                    licenses.append(value)

        distribution = dict(Counter(licenses))

        return {
            "sbom_file": sbom_path,
            "total_components": len(artifacts),
            "license_distribution": distribution,
            "no_license": no_license
        }