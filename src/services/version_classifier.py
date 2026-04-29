class VersionClassifier:

    def classify(self, version: str):

        if not version:
            return "UNKNOWN"

        # high risk
        if version in ["*", "latest"]:
            return "HIGH"

        # unstable versions
        if version.startswith("^0.") or version.startswith("~0."):
            return "MEDIUM"

        # normal versions
        if version.startswith("^") or version.startswith("~"):
            return "LOW"

        # fixed versions
        if version[0].isdigit():
            return "SAFE"

        return "UNKNOWN"