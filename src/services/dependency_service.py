import json
import os

from src.domain.dependency import Dependency


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

 

   