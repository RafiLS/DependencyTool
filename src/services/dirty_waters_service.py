import re

class DirtyWatersService:

    def analyze(self, report_path):

        if not report_path:
            return self._empty()

        with open(report_path, "r", encoding="utf-8") as f:
            text = f.read()

        def extract_int(pattern):
            m = re.search(pattern, text)
            return int(m.group(1)) if m else 0

        return {

            "source_code": [],
            "repo_404_list": [],
            "source_code_sha": [],
            "deprecated_list": [],
            "forks_list": [],
            "provenance": [],
            "code_signature": [],
            "aliased_packages": [],

            "stats": {

                "total_packages": extract_int(
                    r"Total packages in the supply chain:\s*(\d+)"
                ),

                "missing_source_code": extract_int(
                    r"Packages with no source code URL.*?:\s*(\d+)"
                ),

                "repo_404": extract_int(
                    r"Packages with repo URL that is 404.*?:\s*(\d+)"
                ),

                "inaccessible_sha": extract_int(
                    r"Packages with inaccessible commit SHA/tag.*?:\s*(\d+)"
                ),

                "deprecated": extract_int(
                    r"Packages that are deprecated.*?:\s*(\d+)"
                ),

                "no_code_signature": extract_int(
                    r"Packages without code signature.*?:\s*(\d+)"
                ),

                "invalid_code_signature": extract_int(
                    r"Packages with invalid code signature.*?:\s*(\d+)"
                ),

                "forks": extract_int(
                    r"Packages that are forks.*?:\s*(\d+)"
                ),

                "no_attestation": extract_int(
                    r"Packages without build attestation.*?:\s*(\d+)"
                ),

                "aliased": extract_int(
                    r"Packages that are aliased.*?:\s*(\d+)"
                ),
            }
        }

    def _empty(self):

        return {

            "source_code": [],
            "repo_404_list": [],
            "source_code_sha": [],
            "deprecated_list": [],
            "forks_list": [],
            "provenance": [],
            "code_signature": [],
            "aliased_packages": [],

            "stats": {
                "total_packages": 0,
                "missing_source_code": 0,
                "repo_404": 0,
                "inaccessible_sha": 0,
                "deprecated": 0,
                "no_code_signature": 0,
                "invalid_code_signature": 0,
                "forks": 0,
                "no_attestation": 0,
                "aliased": 0,
            }
        }