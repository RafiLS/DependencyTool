import pytest

from src.report.report_generator import ReportGenerator

class DummyDep:
    def __init__(self, name, is_used=True, smells=None):
        self.name = name
        self.is_used = is_used
        self.smell_indicators = smells or []

class DummySmell:
    def __init__(self, description):
        self.description = description

@pytest.fixture
def generator():
    return ReportGenerator()

def test_empty_report(generator):
    result = generator.generate_full_report(
        depcheck_output={},
        sniffer_output={},
        snyk_output={},
        dirty_waters_output={},
        dependencies=[]
    )

    assert "# Dependency Analysis Report" in result
    assert "Total Smells: 0" in result


def test_unused_and_missing_dependencies(generator):
    deps = [
        DummyDep("a", is_used=False),
        DummyDep("b", is_used=True),
        DummyDep("c", smells=[DummySmell("Undeclared dependency")])
    ]

    result = generator.generate_full_report(
        depcheck_output={},
        sniffer_output={},
        snyk_output={},
        dirty_waters_output={},
        dependencies=deps
    )

    assert "Unused dependencies/Bloated Dependencies (1)" in result
    assert "- a" in result

    assert "Missing dependencies (1)" in result
    assert "- c" in result


def test_sniffer_sections(generator):
    result = generator.generate_full_report(
        depcheck_output={},
        sniffer_output={
            "pinned": ["pkg@1.0"],
            "url_dependencies": ["pkg@http://repo"],
            "restrict_constraints": ["pkg@^1.0"],
            "permission_constraints": ["danger-script"],
            "version_risks": [
                {"dependency": "pkg", "risk": "LOW"}
            ]
        },
        snyk_output={},
        dirty_waters_output={},
        dependencies=[]
    )

    assert "Pinned dependencies (1)" in result
    assert "URL dependencies (1)" in result
    assert "Restrict constraints (1)" in result
    assert "Permission constraints (1)" in result
    assert "Version Risk Analysis (1)" in result
    assert "pkg → LOW" in result

def test_version_risk_filter(generator):
    result = generator.generate_full_report(
        depcheck_output={},
        sniffer_output={
            "version_risks": [
                {"dependency": "a", "risk": "SAFE"},
                {"dependency": "b", "risk": "UNKNOWN"},
                {"dependency": "c", "risk": "HIGH"},
            ]
        },
        snyk_output={},
        dirty_waters_output={},
        dependencies=[]
    )

    assert "c → HIGH" in result
    assert "a → SAFE" not in result
    assert "b → UNKNOWN" not in result

def test_snyk_sections(generator):
    result = generator.generate_full_report(
        depcheck_output={},
        sniffer_output={},
        snyk_output={
            "install_scripts": ["pkg - install issue"],
            "license_anomalies": ["pkg - GPL"],
            "transitive_dependencies": ["pkg (via a > b)"]
        },
        dirty_waters_output={},
        dependencies=[]
    )

    assert "Install scripts (1)" in result
    assert "Problematic licenses (1)" in result
    assert "Transitive dependencies (1)" in result


def test_dirty_waters(generator):
    result = generator.generate_full_report(
        depcheck_output={},
        sniffer_output={},
        snyk_output={},
        dirty_waters_output={
            "stats": {
                "missing_source_code": 1,
                "repo_404": 2,
                "inaccessible_sha": 3,
                "deprecated": 0,
                "no_code_signature": 0,
                "invalid_code_signature": 0,
                "forks": 0,
                "aliased": 0
            }
        },
        dependencies=[]
    )

    assert "Missing source code: 1" in result
    assert "Repo 404: 2" in result
    assert "Inaccessible SHA: 3" in result


def test_project_meta_flags(generator):
    result = generator.generate_full_report(
        depcheck_output={},
        sniffer_output={},
        snyk_output={},
        dirty_waters_output={},
        dependencies=[],
        project_meta={
            "has_package_json": True,
            "has_package_lock": False
        }
    )

    assert "package.json: Yes" in result
    assert "package-lock.json: No" in result

def test_total_smells_accumulation(generator):
    deps = [DummyDep("a", is_used=False)]

    result = generator.generate_full_report(
        depcheck_output={},
        sniffer_output={
            "pinned": ["a@1.0"]
        },
        snyk_output={
            "install_scripts": ["x"]
        },
        dirty_waters_output={
            "stats": {"missing_source_code": 1}
        },
        dependencies=deps
    )

    assert "Total Smells:" in result