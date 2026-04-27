import os
from datetime import datetime


class ReportWriter:

    def save(self, content, filename=None):

        # time stamp for the file name
        now = datetime.now()
        timestamp = now.strftime("%d-%m-%Y_%H-%M-%S")
        if filename is None:
            filename = f"Report_{timestamp}.md"
        else:
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{timestamp}{ext}"

        # path to the reports folder
        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )

        folder = os.path.join(base_dir, "save_reports")

        os.makedirs(folder, exist_ok=True)

        path = os.path.join(folder, filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"\nReport guardado em: {path}")