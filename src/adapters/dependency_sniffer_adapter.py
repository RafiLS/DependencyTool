import json
import os

class DependencySnifferAdapter:

    def analyze(self, project_path: str):

        package_json_path = os.path.join(project_path, "package.json")
        lock_path = os.path.join(project_path, "package-lock.json")

        has_package_json = os.path.exists(package_json_path)
        has_package_lock = os.path.exists(lock_path)

        package_json = {}

        if has_package_json:
            with open(package_json_path, "r", encoding="utf-8") as f:
                package_json = json.load(f)

        lock_data = {}

        if has_package_lock:
            with open(lock_path, "r", encoding="utf-8") as f:
                lock_data = json.load(f)

        return {
            "package_json": package_json,
            "lock_file": lock_data,
            "project_meta": {
                "has_package_json": has_package_json,
                "has_package_lock": has_package_lock
            }
        }