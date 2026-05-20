from unittest.mock import patch, mock_open

from src.report.report_writer import ReportWriter

class TestReportWriter:

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    @patch("os.path.join", side_effect=lambda *args: "/".join(args))
    @patch("os.path.abspath", return_value="/base")
    @patch("os.path.dirname", return_value="/fake/dir")
    def test_save_with_default_filename(
        self,
        mock_dirname,
        mock_abspath,
        mock_join,
        mock_makedirs,
        mock_file
    ):
        writer = ReportWriter()

        writer.save("content")

        mock_makedirs.assert_called_once()
        mock_file.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    @patch("os.path.join", side_effect=lambda *args: "/".join(args))
    @patch("os.path.abspath", return_value="/base")
    @patch("os.path.dirname", return_value="/fake/dir")
    def test_save_with_custom_filename(
        self,
        mock_dirname,
        mock_abspath,
        mock_join,
        mock_makedirs,
        mock_file
    ):
        writer = ReportWriter()

        writer.save("content", "report.md")

        mock_file.assert_called_once()