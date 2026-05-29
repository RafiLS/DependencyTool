import argparse
import shutil
import os
import re
import threading
import itertools
import time
from src.controllers.analysis_controller import AnalysisController

from src.services.depcheck_service import DepcheckService
from src.services.snyk_service import SnykService
from src.services.dirty_waters_service import DirtyWatersService
from src.services.dependency_sniffer_service import DependencySnifferService

spinner_running = False


def spinner():

    for char in itertools.cycle(["|", "/", "-", "\\"]):

        if not spinner_running:
            break

        print(f"\rRunning analysis... {char}", end="", flush=True)

        time.sleep(0.1)

    print("\rAnalysis completed.      ")


def validate_repo(repo: str):
    pattern = r"^[a-zA-Z0-9_.-]+\/[a-zA-Z0-9_.-]+$"
    if not re.match(pattern, repo):
        print("[ERROR] Invalid repo format. Use owner/repo (e.g. RafiLS/TaskReact)")
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

    parser = argparse.ArgumentParser(
        description="Dependency Analysis Tool",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Usage:\n"
            "  dependencyTool analyze owner/repo --path \"C:\\path\\to\\project\"\n"
            "Examples:\n"
            "  dependencyTool analyze RafiLS/TaskReact --path \"C:\\Users\\Rafael\\Desktop\\TaskReactVite\"\n\n"
        )
    )

    subparsers = parser.add_subparsers(dest="command")

    analyze_parser = subparsers.add_parser(
        "analyze",
        description="Runs dependency analysis on a local project.",
        help="Analyze dependencies of a project using a GitHub repo + local path"
    )

    analyze_parser.add_argument(
        "repo",
        help="GitHub repository in format owner/repo (e.g. RafiLS/TaskReact)"
    )

    analyze_parser.add_argument(
        "--path",
        required=True,
        help="Path to local project (must contain package.json)"
    )

    analyze_parser.add_argument(
        "--output",
        default="report.md",
        help="Output report file (default: report.md)"
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

        global spinner_running
        spinner_running = True

        spinner_thread = threading.Thread(target=spinner)
        spinner_thread.start()

        start_time = time.time()

        controller.analyze_project(
            project_path=args.path,
            github_repo=args.repo,
            report_path=args.output
        )

        end_time = time.time()

        spinner_running = False
        spinner_thread.join()

        total_time = end_time - start_time

        if os.path.exists("results"):
            shutil.rmtree("results")

        print(f"\nAnalysis completed successfully in {total_time:.2f} seconds.")


if __name__ == "__main__":
    main()