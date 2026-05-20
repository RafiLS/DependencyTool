from src.domain.smell_indicator import SmellIndicator

class TestSmellIndicator:

    def test_creation(self):
        indicator = SmellIndicator("HIGH", "Unused dependency")

        assert indicator.severity == "HIGH"
        assert indicator.description == "Unused dependency"
        assert indicator.smells == []

    def test_add_smell(self):
        indicator = SmellIndicator("MEDIUM", "Bloated dependency")

        indicator.add_smell("example-smell")

        assert len(indicator.smells) == 1
        assert indicator.smells[0] == "example-smell"

    def test_str_representation(self):
        indicator = SmellIndicator("LOW", "Test smell")

        assert str(indicator) == "[LOW] Test smell"