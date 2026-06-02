import json
import pytest

from src.adapters.dependency_sniffer_adapter import DependencySnifferAdapter


class TestDependencySnifferAdapter:

    def test_no_files_exist(self, tmp_path):
        adapter = DependencySnifferAdapter()

        result = adapter.analyze(str(tmp_path))

        assert result["package_json"] == {}
        assert result["lock_file"] == {}
        assert result["project_meta"] == {
            "has_package_json": False,
            "has_package_lock": False
        }

    def test_only_package_json(self, tmp_path):
        adapter = DependencySnifferAdapter()

        package_data = {"name": "test-project"}

        pkg_path = tmp_path / "package.json"
        pkg_path.write_text(json.dumps(package_data), encoding="utf-8")

        result = adapter.analyze(str(tmp_path))

        assert result["package_json"] == package_data
        assert result["lock_file"] == {}
        assert result["project_meta"]["has_package_json"] is True
        assert result["project_meta"]["has_package_lock"] is False

    def test_only_package_lock(self, tmp_path):
        adapter = DependencySnifferAdapter()

        lock_data = {"lockfileVersion": 2}

        lock_path = tmp_path / "package-lock.json"
        lock_path.write_text(json.dumps(lock_data), encoding="utf-8")

        result = adapter.analyze(str(tmp_path))

        assert result["package_json"] == {}
        assert result["lock_file"] == lock_data
        assert result["project_meta"]["has_package_json"] is False
        assert result["project_meta"]["has_package_lock"] is True

    def test_both_files_exist(self, tmp_path):
        adapter = DependencySnifferAdapter()

        package_data = {"name": "app"}
        lock_data = {"lockfileVersion": 2}

        (tmp_path / "package.json").write_text(
            json.dumps(package_data),
            encoding="utf-8"
        )

        (tmp_path / "package-lock.json").write_text(
            json.dumps(lock_data),
            encoding="utf-8"
        )

        result = adapter.analyze(str(tmp_path))

        assert result["package_json"] == package_data
        assert result["lock_file"] == lock_data

        assert result["project_meta"] == {
            "has_package_json": True,
            "has_package_lock": True
        }

    def test_invalid_json_handling_not_crashing(self, tmp_path):
        adapter = DependencySnifferAdapter()

        (tmp_path / "package.json").write_text(
            "{invalid json",
            encoding="utf-8"
        )

        with pytest.raises(json.JSONDecodeError):
            adapter.analyze(str(tmp_path))