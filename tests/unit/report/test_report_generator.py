from unittest.mock import Mock

from src.report.report_generator import ReportGenerator


class TestReportGenerator:

    def test_empty_report(self):

        # Arrange
        generator = ReportGenerator()

        # Act
        report = generator.generate_full_report(
            results={},
            dependencies=[]
        )

        # Assert
        assert "# Dependency Analysis Report" in report
        assert "Total Smells: 0" in report

    def test_unused_and_missing_dependencies(self):

        # Arrange
        generator = ReportGenerator()

        dep1 = Mock()
        dep1.name = "a"
        dep1.is_used = False
        dep1.smell_indicators = []

        smell = Mock()
        smell.description = "Undeclared dependency"

        dep2 = Mock()
        dep2.name = "c"
        dep2.is_used = True
        dep2.smell_indicators = [smell]

        # Act
        report = generator.generate_full_report(
            results={},
            dependencies=[dep1, dep2]
        )

        # Assert
        assert "Unused dependencies (1)" in report
        assert "- a" in report

        assert "Missing dependencies (1)" in report
        assert "- c" in report

    def test_sniffer_sections(self):

        # Arrange
        generator = ReportGenerator()

        results = {
            "dependency_sniffer": {
                "pinned": ["pkg@1.0"],
                "url_dependencies": ["pkg@http://repo"],
                "restrict_constraints": ["pkg@^1.0"],
                "permission_constraints": ["danger-script"],
                "version_risks": [
                    {
                        "dependency": "pkg",
                        "risk": "LOW"
                    }
                ]
            }
        }

        # Act
        report = generator.generate_full_report(
            results=results,
            dependencies=[]
        )

        # Assert
        assert "Pinned dependencies (1)" in report
        assert "URL dependencies (1)" in report
        assert "Restrict constraints (1)" in report
        assert "Permission constraints (1)" in report
        assert "Version Risk Analysis (1)" in report
        assert "pkg → LOW" in report

    def test_version_risk_filter(self):

        # Arrange
        generator = ReportGenerator()

        results = {
            "dependency_sniffer": {
                "version_risks": [
                    {"dependency": "a", "risk": "SAFE"},
                    {"dependency": "b", "risk": "UNKNOWN"},
                    {"dependency": "c", "risk": "HIGH"}
                ]
            }
        }

        # Act
        report = generator.generate_full_report(
            results=results,
            dependencies=[]
        )

        # Assert
        assert "c → HIGH" in report
        assert "a → SAFE" not in report
        assert "b → UNKNOWN" not in report

    def test_snyk_sections(self):

        # Arrange
        generator = ReportGenerator()

        results = {
            "snyk": {
                "install_scripts": [
                    "pkg - install issue"
                ],
                "license_anomalies": [
                    "pkg - GPL"
                ],
                "transitive_dependencies": [
                    "pkg (via a > b)"
                ]
            }
        }

        # Act
        report = generator.generate_full_report(
            results=results,
            dependencies=[]
        )

        # Assert
        assert "Install scripts (1)" in report
        assert "Problematic licenses (1)" in report
        assert "Transitive dependencies (1)" in report

    def test_dirty_waters_section(self):

        # Arrange
        generator = ReportGenerator()

        results = {
            "dirty_waters": {
                "stats": {
                    "missing_source_code": 1,
                    "repo_404": 2,
                    "inaccessible_sha": 3
                }
            }
        }

        # Act
        report = generator.generate_full_report(
            results=results,
            dependencies=[]
        )

        # Assert
        assert "- missing_source_code: 1" in report
        assert "- repo_404: 2" in report
        assert "- inaccessible_sha: 3" in report

    def test_project_structure_section(self):

        # Arrange
        generator = ReportGenerator()

        results = {
            "dependency_sniffer": {
                "project_meta": {
                    "has_package_json": True,
                    "has_package_lock": False
                }
            }
        }

        # Act
        report = generator.generate_full_report(
            results=results,
            dependencies=[],
            project_repo="owner/repo"
        )

        # Assert
        assert "Project: owner/repo" in report
        assert "package.json: Yes" in report
        assert "package-lock.json: No" in report

    def test_sbom_section(self):

        # Arrange
        generator = ReportGenerator()

        sbom = {
            "total_components": 5,
            "license_distribution": {
                "MIT": 3,
                "Apache-2.0": 2
            },
            "no_license": ["pkg1"]
        }

        # Act
        report = generator.generate_full_report(
            results={},
            dependencies=[],
            sbom=sbom,
            sbom_path="sbom.json"
        )

        # Assert
        assert "SBOM Summary" in report
        assert "SBOM file: sbom.json" in report
        assert "Total components: 5" in report
        assert "MIT (3)" in report
        assert "Apache-2.0 (2)" in report
        assert "Components with no license: 1" in report

    def test_total_smells_accumulation(self):

        # Arrange
        generator = ReportGenerator()

        dep = Mock()
        dep.name = "a"
        dep.is_used = False
        dep.smell_indicators = []

        results = {
            "dependency_sniffer": {
                "version_risks": [
                    {
                        "dependency": "pkg",
                        "risk": "HIGH"
                    }
                ]
            },
            "snyk": {
                "install_scripts": ["script"]
            },
            "dirty_waters": {
                "stats": {
                    "missing_source_code": 1
                }
            }
        }

        # Act
        report = generator.generate_full_report(
            results=results,
            dependencies=[dep]
        )

        # Assert
        assert "Total Smells: 4" in report