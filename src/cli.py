import argparse
import shutil
import os

from src.controllers.analysis_controller import AnalysisController


def main():

    parser = argparse.ArgumentParser(
        description="Dependency Tool CLI"
    )

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

        controller = AnalysisController()

        controller.analyze_project(
            project_path=args.path,
            github_repo=args.repo,
            report_path=args.output
        )

        #delete dirty waters report
        results_folder = "results"

        if os.path.exists(results_folder):
          shutil.rmtree(results_folder)
            

        print("\nAnalysis completed!")


if __name__ == "__main__":
    main()