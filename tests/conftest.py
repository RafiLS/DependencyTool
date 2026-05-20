import pytest

from src.domain.dependency import Dependency

@pytest.fixture
def sample_dependencies():

    return [
        Dependency("axios", "^1.6.0"),
        Dependency("request", "2.88.2"),
        Dependency("uuid", "^9.0.0")
    ]


@pytest.fixture
def sample_depcheck_output():

    return {
        "dependencies": ["request"],
        "missing": {}
    }


@pytest.fixture
def sample_snyk_output():

    return {
        "vulnerabilities": [
            {
                "packageName": "request",
                "title": "install script execution",
                "from": [
                    "project",
                    "request@2.88.2"
                ]
            }
        ]
    }