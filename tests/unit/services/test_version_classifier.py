from src.services.version_classifier import VersionClassifier

class TestVersionClassifier:

    def setup_method(self):
        self.classifier = VersionClassifier()

    def test_high_risk_version(self):
        assert self.classifier.classify("*") == "HIGH"

    def test_medium_risk_version(self):
        assert self.classifier.classify("^0.1.0") == "MEDIUM"

    def test_low_risk_version(self):
        assert self.classifier.classify("^1.2.3") == "LOW"

    def test_safe_version(self):
        assert self.classifier.classify("1.2.3") == "SAFE"

    def test_unknown_version(self):
        assert self.classifier.classify("") == "UNKNOWN"