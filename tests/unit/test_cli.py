import os
import shutil
from unittest.mock import patch

from src.cli import validate_repo, validate_path, check_tools

class TestCLI:

    def test_validate_repo_valid(self):
        assert validate_repo("RafiLS/TaskReact") is True

    def test_validate_repo_invalid(self):
        assert validate_repo("invalid_repo") is False

    @patch("os.path.exists")
    @patch("os.path.isdir")
    def test_validate_path_valid(self, mock_isdir, mock_exists):
        mock_exists.return_value = True
        mock_isdir.return_value = True

        with patch("os.path.join", return_value="package.json"):
            assert validate_path("/fake/path") is True

    @patch("os.path.exists")
    def test_validate_path_not_exists(self, mock_exists):
        mock_exists.return_value = False
        assert validate_path("/fake/path") is False

    @patch("os.path.exists")
    @patch("os.path.isdir")
    def test_validate_path_not_dir(self, mock_isdir, mock_exists):
        mock_exists.return_value = True
        mock_isdir.return_value = False
        assert validate_path("/fake/path") is False

    @patch("shutil.which")
    def test_check_tools_valid(self, mock_which):
        mock_which.return_value = "/usr/bin/npx"
        assert check_tools() is True

    @patch("shutil.which")
    def test_check_tools_invalid(self, mock_which):
        mock_which.return_value = None
        assert check_tools() is False