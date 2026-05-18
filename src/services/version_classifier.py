from src.config.config_loader import ConfigLoader


class VersionClassifier:

    def __init__(self):

        config = ConfigLoader()

        smells_config = config.section("version_smells")

        self.dangerous_versions = smells_config["dangerous_versions"]

        self.unstable_prefixes = smells_config["unstable_prefixes"]

        self.normal_prefixes = smells_config["normal_prefixes"]

        self.high_risk_label = smells_config["high_risk_label"]
        self.medium_risk_label = smells_config["medium_risk_label"]
        self.low_risk_label = smells_config["low_risk_label"]
        self.safe_label = smells_config["safe_label"]
        self.unknown_label = smells_config["unknown_label"]

    def classify(self, version: str):

        if not version:
            return self.unknown_label

        # high risk
        if version in self.dangerous_versions:
            return self.high_risk_label

        # unstable versions
        if any(version.startswith(prefix)
               for prefix in self.unstable_prefixes):
            return self.medium_risk_label

        # normal versions
        if any(version.startswith(prefix)
               for prefix in self.normal_prefixes):
            return self.low_risk_label

        # fixed versions
        if version[0].isdigit():
            return self.safe_label

        return self.unknown_label