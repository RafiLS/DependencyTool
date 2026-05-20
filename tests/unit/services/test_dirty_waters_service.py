from src.services.dirty_waters_service import DirtyWatersService

class TestDirtyWatersService:

    def test_empty_path_returns_empty(self):

        service = DirtyWatersService()

        result = service.analyze(None)

        assert result["stats"]["total_packages"] == 0


    def test_extracts_missing_source_code(self, tmp_path):

        service = DirtyWatersService()

        content = """
        Total packages in the supply chain: 10
        Packages with no source code URL: 3
        """

        report_file = tmp_path / "report.md"
        report_file.write_text(content, encoding="utf-8")

        result = service.analyze(str(report_file))

        assert result["stats"]["total_packages"] == 10
        assert result["stats"]["missing_source_code"] == 3


    def test_extracts_repo_404(self, tmp_path):

        service = DirtyWatersService()

        content = """
        Packages with repo URL that is 404: 4
        """

        report_file = tmp_path / "report.md"
        report_file.write_text(content, encoding="utf-8")

        result = service.analyze(str(report_file))

        assert result["stats"]["repo_404"] == 4

    def test_disabled_metrics_are_zeroed(self, tmp_path, monkeypatch):

        monkeypatch.setattr(
            "src.services.dirty_waters_service.ConfigLoader",
            lambda: type("C", (), {
                "section": lambda self, x: {
                    "dirty_waters": {
                        "check_source_code": False,
                        "check_source_code_sha": False,
                        "check_deprecated": False,
                        "check_forks": False,
                        "check_provenance": False,
                        "check_code_signature": False,
                        "check_aliased_packages": False
                    }
                }
            })()
        )

        service = DirtyWatersService()

        content = """
        Total packages in the supply chain: 10
        Packages with no source code URL: 3
        Packages that are deprecated: 5
        """

        report_file = tmp_path / "report.md"
        report_file.write_text(content, encoding="utf-8")

        result = service.analyze(str(report_file))

        assert result["stats"]["missing_source_code"] == 0
        assert result["stats"]["deprecated"] == 0
        assert result["stats"]["forks"] == 0