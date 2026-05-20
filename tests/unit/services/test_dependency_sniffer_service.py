from src.services.dependency_sniffer_service import DependencySnifferService

class TestDependencySnifferService:

    def test_detects_url_dependency(self):

        service = DependencySnifferService()

        raw = {
            "package_json": {
                "dependencies": {
                    "lodash": "https://github.com/lodash/lodash"
                },
                "devDependencies": {}
            }
        }

        result = service.analyze_constraints(raw)

        assert any("lodash" in dep for dep in result["url_dependencies"])

    def test_detects_pinned_dependency(self):

        service = DependencySnifferService()

        raw = {
            "package_json": {
                "dependencies": {
                    "react": "18.2.0"
                },
                "devDependencies": {}
            }
        }

        result = service.analyze_constraints(raw)

        assert "react@18.2.0" in result["pinned"]


    def test_detects_restrict_constraint(self):

        service = DependencySnifferService()

        raw = {
            "package_json": {
                "dependencies": {
                    "axios": "^1.6.0"
                },
                "devDependencies": {}
            }
        }

        result = service.analyze_constraints(raw)

        assert "axios@^1.6.0" in result["restrict_constraints"]


    def test_detects_permission_constraint(self):

        service = DependencySnifferService()

        raw = {
            "package_json": {
                "dependencies": {},
                "devDependencies": {},
                "scripts": {
                    "start": "node server.js",
                    "danger": "rm -rf node_modules"
                }
            }
        }

        result = service.analyze_constraints(raw)

        assert "danger" in result["permission_constraints"]


    def test_version_risks_are_generated(self):

        service = DependencySnifferService()

        raw = {
            "package_json": {
                "dependencies": {
                    "lodash": "1.2.3"
                },
                "devDependencies": {}
            }
        }

        result = service.analyze_constraints(raw)

        assert len(result["version_risks"]) == 1
        assert result["version_risks"][0]["dependency"] == "lodash"