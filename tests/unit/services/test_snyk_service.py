from src.services.snyk_service import SnykService

class TestSnykService:

    def test_empty_input_returns_empty_lists(self):

        service = SnykService()

        result = service.analyze({})

        assert result == {
            "install_scripts": [],
            "license_anomalies": [],
            "transitive_dependencies": []
        }


    def test_install_script_detection(self):

        service = SnykService()

        data = {
            "vulnerabilities": [
                {
                    "packageName": "lodash",
                    "title": "Install script vulnerability",
                    "from": ["app", "lodash"]
                }
            ]
        }

        result = service.analyze(data)

        assert len(result["install_scripts"]) == 1
        assert "lodash" in result["install_scripts"][0]
        assert "Install script" in result["install_scripts"][0]


    def test_license_anomaly_detection(self):

        service = SnykService()

        service.problematic_licenses = ["GPL-3.0"]

        data = {
            "vulnerabilities": [
                {
                    "packageName": "react",
                    "license": "GPL-3.0",
                    "from": ["app"]
                }
            ]
        }

        result = service.analyze(data)

        assert len(result["license_anomalies"]) == 1
        assert "react" in result["license_anomalies"][0]
        assert "GPL-3.0" in result["license_anomalies"][0]


    def test_transitive_dependency_detection(self):

        service = SnykService()

        data = {
            "vulnerabilities": [
                {
                    "packageName": "axios",
                    "from": ["app", "lib", "axios"]
                }
            ]
        }

        result = service.analyze(data)

        assert len(result["transitive_dependencies"]) == 1
        assert "axios" in result["transitive_dependencies"][0]
        assert "app > lib > axios" in result["transitive_dependencies"][0]


    def test_deduplication_of_transitives(self):

        service = SnykService()

        data = {
            "vulnerabilities": [
                {
                    "packageName": "axios",
                    "from": ["app", "lib", "axios"]
                },
                {
                    "packageName": "axios",
                    "from": ["app", "lib", "axios"]
                }
            ]
        }

        result = service.analyze(data)

        # deve remover duplicados
        assert len(result["transitive_dependencies"]) == 1


    def test_ignore_invalid_inputs(self):

        service = SnykService()

        data = {
            "vulnerabilities": [
                {
                    "packageName": None,
                    "title": None,
                    "from": None
                }
            ]
        }

        result = service.analyze(data)

        assert result["install_scripts"] == []
        assert result["license_anomalies"] == []
        assert result["transitive_dependencies"] == []