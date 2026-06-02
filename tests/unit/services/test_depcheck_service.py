from src.services.depcheck_service import DepcheckService


class FakeDependency:
    def __init__(self, name):
        self.name = name
        self.is_used = True
        self.smell_indicators = []

    def add_smell_indicator(self, smell):
        self.smell_indicators.append(smell)


class TestDepcheckService:

    def test_marks_unused_dependency(self):

        service = DepcheckService()

        deps = [FakeDependency("lodash")]

        service._adapter.analyze = lambda _: {
            "dependencies": ["lodash"],
            "missing": []
        }
        result = service.analyze("/fake", "repo", deps)

        dep = result[0]
        assert dep.is_used is False
        assert len(dep.smell_indicators) == 1
        assert dep.smell_indicators[0].description == service.unused_description

    def test_detects_missing_dependency(self):

        service = DepcheckService()

        deps = [FakeDependency("react")]

        service._adapter.analyze = lambda _: {
            "dependencies": [],
            "missing": ["react"]
        }
        result = service.analyze("/fake", "repo", deps)

        dep = result[0]
        assert len(dep.smell_indicators) == 1
        assert dep.smell_indicators[0].description == service.missing_description

    def test_unused_and_missing_at_same_time(self):

        service = DepcheckService()

        deps = [FakeDependency("axios")]

        service._adapter.analyze = lambda _: {
            "dependencies": ["axios"],
            "missing": ["axios"]
        }
        result = service.analyze("/fake", "repo", deps)

        dep = result[0]
        assert len(dep.smell_indicators) == 2

        severities = {s.severity for s in dep.smell_indicators}
        assert service.unused_severity in severities
        assert service.missing_severity in severities

    def test_no_matches_keeps_dependency_clean(self):

        service = DepcheckService()

        deps = [FakeDependency("express")]

        service._adapter.analyze = lambda _: {
            "dependencies": [],
            "missing": []
        }
        result = service.analyze("/fake", "repo", deps)

        dep = result[0]
        assert dep.is_used is True
        assert dep.smell_indicators == []

    def test_multiple_dependencies_mixed_cases(self):

        service = DepcheckService()

        deps = [
            FakeDependency("a"),
            FakeDependency("b"),
            FakeDependency("c")
        ]

        service._adapter.analyze = lambda _: {
            "dependencies": ["a", "c"],
            "missing": ["b"]
        }

        result = service.analyze("/fake", "repo", deps)
        a, b, c = result

        assert a.is_used is False
        assert c.is_used is False

        assert len(b.smell_indicators) == 1
        assert b.smell_indicators[0].description == service.missing_description