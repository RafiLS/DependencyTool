import json
import os

from src.domain.dependency import Dependency
from src.repositories.sqlite_dependency_repository import SQLiteDependencyRepository


class DependencyService:

    def __init__(self, dependency_repository=None):
        self.dependency_repository = dependency_repository

    def extract_from_package_json(self, path):

        dependencies = []

        with open(f"{path}/package.json", encoding="utf-8") as f:
            data = json.load(f)

        deps = data.get("dependencies", {})

        for name, version in deps.items():

            dep = Dependency(
                name=name,
                version=version,
                dep_type="npm",
                source="package.json"
            )

            dependencies.append(dep)

        return dependencies

    def extract_from_sbom(self, sbom_path):

        dependencies = []

        with open(sbom_path, encoding="utf-8") as f:
            data = json.load(f)

        artifacts = data.get("artifacts", [])

        for artifact in artifacts:

            dep = Dependency(
                name=artifact.get("name"),
                version=artifact.get("version"),
                dep_type=artifact.get("type") or artifact.get("language") or "unknown",
                source="SBOM",
                purl=artifact.get("purl")
            )

            dependencies.append(dep)

        return dependencies

    def extract_and_store_from_sbom(self, sbom_adapter, project_path):

        sbom_path = sbom_adapter.generate_sbom(project_path)

        sbom_dir = os.path.dirname(sbom_path)

        self.dependency_repository = SQLiteDependencyRepository(sbom_dir)

        dependencies = self.extract_from_sbom(sbom_path)

        for dep in dependencies:
            self.dependency_repository.save(dep)

        return sbom_path