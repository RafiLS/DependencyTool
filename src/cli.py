import argparse
from src.controllers.analysis_controller import AnalysisController


def main():
    parser = argparse.ArgumentParser(description="Dependency Tool CLI")

    subparsers = parser.add_subparsers(dest="command")

    analyze_parser = subparsers.add_parser("analyze")
    analyze_parser.add_argument("path", help="Path to project")
    analyze_parser.add_argument("--output", default="report.md")

    args = parser.parse_args()

    if args.command == "analyze":

        controller = AnalysisController()

        controller.analyze_project(
            args.path,
            args.output
        )

        print("\nAnalysis completed!")

if __name__ == "__main__":
    main()