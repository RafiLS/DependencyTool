import json
from src.services.dependency_service import DependencyService
from src.domain.dependency import Dependency

class TestDependencyService:

    def test_extracts_dependencies_from_package_json(self, tmp_path):

        package_data = {
            "dependencies": {
                "lodash": "^4.0.0",
                "react": "^18.0.0"
            }
        }

        pkg_file = tmp_path / "package.json"
        pkg_file.write_text(json.dumps(package_data), encoding="utf-8")

        service = DependencyService()

        result = service.extract_from_package_json(str(tmp_path))

        assert len(result) == 2

        names = [d.name for d in result]

        assert "lodash" in names
        assert "react" in names


    def test_dependency_object_structure(self, tmp_path):

        package_data = {
            "dependencies": {
                "axios": "1.0.0"
            }
        }

        (tmp_path / "package.json").write_text(
            json.dumps(package_data),
            encoding="utf-8"
        )

        service = DependencyService()

        result = service.extract_from_package_json(str(tmp_path))

        dep = result[0]

        assert isinstance(dep, Dependency)
        assert dep.name == "axios"
        assert dep.version == "1.0.0"
        assert dep.dep_type == "npm"
        assert dep.source == "package.json"


    def test_empty_dependencies_returns_empty_list(self, tmp_path):

        package_data = {
            "dependencies": {}
        }

        (tmp_path / "package.json").write_text(
            json.dumps(package_data),
            encoding="utf-8"
        )

        service = DependencyService()

        result = service.extract_from_package_json(str(tmp_path))

        assert result == []


    def test_missing_dependencies_key(self, tmp_path):

        package_data = {
            "name": "test-project"
        }

        (tmp_path / "package.json").write_text(
            json.dumps(package_data),
            encoding="utf-8"
        )

        service = DependencyService()

        result = service.extract_from_package_json(str(tmp_path))

        assert result == []