import json
from src.domain.dependency import Dependency


class DependencyService:
    def extract_from_package_json(self, path):
        dependencies = []

        with open(f"{path}/package.json") as f:
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