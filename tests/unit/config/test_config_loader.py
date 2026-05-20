import os
import tempfile

from src.config.config_loader import ConfigLoader

class TestConfigLoader:

    def test_config_loader_missing_file(self):
        loader = ConfigLoader(path="non_existing.toml")

        assert loader.config == {}

    def test_config_loader_loads_toml(self):
        toml_content = """
            [smells.depcheck]
            unused_severity = "medium"
            missing_severity = "high"
            """

        with tempfile.NamedTemporaryFile(delete=False, suffix=".toml") as f:
            f.write(toml_content.encode("utf-8"))
            temp_path = f.name

        loader = ConfigLoader(path=temp_path)

        assert "smells" in loader.config
        assert loader.config["smells"]["depcheck"]["unused_severity"] == "medium"

        os.remove(temp_path)

    def test_section_returns_correct_data(self):
        toml_content = """
            [tools.depcheck]
            version = "1.0"
            """

        with tempfile.NamedTemporaryFile(delete=False, suffix=".toml") as f:
            f.write(toml_content.encode("utf-8"))
            temp_path = f.name

        loader = ConfigLoader(path=temp_path)

        section = loader.section("tools")

        assert "depcheck" in section
        assert section["depcheck"]["version"] == "1.0"

        os.remove(temp_path)

    def test_section_returns_empty_dict(self):
        loader = ConfigLoader(path="non_existing.toml")

        assert loader.section("anything") == {}