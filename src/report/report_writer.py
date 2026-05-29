import os
from datetime import datetime


class ReportWriter:

    def save(self, content, project_name, filename=None, base_dir_name="save_reports"):

        now = datetime.now()
        timestamp = now.strftime("%d-%m-%Y_%H-%M-%S")

        project_name = project_name.replace("/", "_")

        if filename is None:
            filename = f"report_{timestamp}.md"
        else:
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{timestamp}{ext}"

        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )

        project_folder = os.path.join(
            base_dir,
            base_dir_name,
            project_name
        )

        os.makedirs(project_folder, exist_ok=True)

        path = os.path.join(project_folder, filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"\nReport saved in: {path}")

        return path