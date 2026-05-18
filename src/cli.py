import argparse
import shutil
import os
import re

from src.controllers.analysis_controller import AnalysisController


def validate_repo(repo: str):
    pattern = r"^[a-zA-Z0-9_.-]+\/[a-zA-Z0-9_.-]+$"
    if not re.match(pattern, repo):
        print("[ERROR] Invalid repo format. Expected owner/repo (e.g. RafiLS/TaskReact)")
        return False
    return True


def validate_path(path: str):
    if not os.path.exists(path):
        print("[ERROR] Path does not exist.")
        return False

    if not os.path.isdir(path):
        print("[ERROR] Path is not a directory.")
        return False

    if not os.path.exists(os.path.join(path, "package.json")):
        print("[ERROR] package.json not found in project path.")
        return False

    return True


def check_tools():
    if shutil.which("npx") is None:
        print("[ERROR] npx is not installed or not in PATH.")
        return False
    return True


def main():

    parser = argparse.ArgumentParser(description="Dependency Tool CLI")
    subparsers = parser.add_subparsers(dest="command")

    analyze_parser = subparsers.add_parser("analyze")

    analyze_parser.add_argument(
        "repo",
        help="GitHub repo (e.g. RafiLS/TaskReact)"
    )

    analyze_parser.add_argument(
        "--path",
        required=True,
        help="Local project path"
    )

    analyze_parser.add_argument(
        "--output",
        default="report.md"
    )

    args = parser.parse_args()

    if args.command == "analyze":

        if not check_tools():
            return

        if not validate_repo(args.repo):
            return

        if not validate_path(args.path):
            return

        controller = AnalysisController()

        controller.analyze_project(
            project_path=args.path,
            github_repo=args.repo,
            report_path=args.output
        )

        results_folder = "results"

        if os.path.exists(results_folder):
            shutil.rmtree(results_folder)

        print("\nAnalysis completed!")


if __name__ == "__main__":
    main()