from src.domain.dependency import Dependency
from src.domain.smell_indicator import SmellIndicator

class TestDependency:

    def test_creation(self):
        dep = Dependency(
            name="react",
            version="18.2.0",
            dep_type="prod",
            source="package.json"
        )

        assert dep.name == "react"
        assert dep.version == "18.2.0"
        assert dep.dep_type == "prod"
        assert dep.source == "package.json"
        assert dep.purl is None
        assert dep.smell_indicators == []

    def test_add_smell_indicator(self):
        dep = Dependency(
            name="react",
            version="18.2.0",
            dep_type="prod",
            source="package.json"
        )

        smell = SmellIndicator("HIGH", "Unused dependency")

        dep.add_smell_indicator(smell)

        assert len(dep.smell_indicators) == 1
        assert dep.smell_indicators[0] == smell

    def test_has_smells_false(self):
        dep = Dependency(
            name="react",
            version="18.2.0",
            dep_type="prod",
            source="package.json"
        )

        assert dep.has_smells() is False

    def test_has_smells_true(self):
        dep = Dependency(
            name="react",
            version="18.2.0",
            dep_type="prod",
            source="package.json"
        )

        dep.add_smell_indicator(
            SmellIndicator("MEDIUM", "Bloated dependency")
        )

        assert dep.has_smells() is True