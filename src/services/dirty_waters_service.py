from src.config.config_loader import ConfigLoader
from src.domain.i_analysis_tool import IAnalysisTool
from src.domain.tool_registry import ToolRegistry
from src.adapters.dirty_waters_adapter import DirtyWatersAdapter
import re
import os


@ToolRegistry.register
class DirtyWatersService(IAnalysisTool):

    def __init__(self):
        self._adapter = DirtyWatersAdapter()

        config = ConfigLoader()
        dirty = config.section("tools").get("dirty_waters", {})

        self.enabled = {
            "missing_source_code": dirty.get("check_source_code", True),
            "repo_404": dirty.get("check_source_code", True),
            "inaccessible_sha": dirty.get("check_source_code_sha", True),
            "deprecated": dirty.get("check_deprecated", True),
            "forks": dirty.get("check_forks", True),
            "no_code_signature": dirty.get("check_code_signature", True),
            "invalid_code_signature": dirty.get("check_code_signature", True),
            "aliased": dirty.get("check_aliased_packages", True),
        }

    def name(self) -> str:
        return "dirty_waters"

    def analyze(self, project_path, github_repo, dependencies):

        report_file = self._adapter.analyze(
            project_repo=github_repo,
            is_local=False
        )

        if not report_file or not os.path.exists(report_file):
            return self._empty()

        with open(report_file, "r", encoding="utf-8") as f:
            text = f.read()

        def extract_int(pattern):
            m = re.search(pattern, text)
            return int(m.group(1)) if m else 0

        stats = {
            "missing_source_code": extract_int(r"Packages with no source code URL.*?:\s*(\d+)"),
            "repo_404": extract_int(r"Packages with repo URL that is 404.*?:\s*(\d+)"),
            "inaccessible_sha": extract_int(r"Packages with inaccessible commit SHA/tag.*?:\s*(\d+)"),
            "deprecated": extract_int(r"Packages that are deprecated.*?:\s*(\d+)"),
            "no_code_signature": extract_int(r"Packages without code signature.*?:\s*(\d+)"),
            "invalid_code_signature": extract_int(r"Packages with invalid code signature.*?:\s*(\d+)"),
            "forks": extract_int(r"Packages that are forks.*?:\s*(\d+)"),
            "aliased": extract_int(r"Packages that are aliased.*?:\s*(\d+)"),
        }

        for key, enabled in self.enabled.items():
            if not enabled:
                stats[key] = 0

        return {
            "source_code": [],
            "repo_404_list": [],
            "source_code_sha": [],
            "deprecated_list": [],
            "forks_list": [],
            "provenance": [],
            "code_signature": [],
            "aliased_packages": [],
            "stats": stats
        }