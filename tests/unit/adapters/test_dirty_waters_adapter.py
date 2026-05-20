from unittest.mock import patch, Mock

from src.adapters.dirty_waters_adapter import DirtyWatersAdapter

class TestDirtyWatersAdapter:

    def test_tool_not_installed(self):

        with patch("shutil.which", return_value=None):
            adapter = DirtyWatersAdapter()

            result = adapter.analyze("repo/test")

            assert result is None


    def test_tool_execution_fails(self):

        with patch("shutil.which", return_value="dirty-waters"), \
             patch("subprocess.run") as mock_run:

            mock_run.return_value = Mock(returncode=1, stderr="error")

            adapter = DirtyWatersAdapter()
            result = adapter.analyze("repo/test")

            assert result is None


    def test_no_report_generated(self):

        with patch("shutil.which", return_value="dirty-waters"), \
             patch("subprocess.run") as mock_run, \
             patch("glob.glob", return_value=[]):

            mock_run.return_value = Mock(returncode=0)

            adapter = DirtyWatersAdapter()
            result = adapter.analyze("repo/test")

            assert result is None


    def test_latest_report_selected(self):

        with patch("shutil.which", return_value="dirty-waters"), \
             patch("subprocess.run") as mock_run, \
             patch("glob.glob") as mock_glob, \
             patch("os.path.getctime") as mock_ctime:

            mock_run.return_value = Mock(returncode=0)

            mock_glob.return_value = [
                "results/report1_static_summary.md",
                "results/report2_static_summary.md"
            ]

            mock_ctime.side_effect = [100, 200]

            adapter = DirtyWatersAdapter()
            result = adapter.analyze("repo/test")

            assert result == "results/report2_static_summary.md"


    def test_local_mode_skips_version_flag(self):

        with patch("shutil.which", return_value="dirty-waters"), \
             patch("subprocess.run") as mock_run, \
             patch("glob.glob", return_value=["results/x.md"]), \
             patch("os.path.getctime", return_value=100):

            mock_run.return_value = Mock(returncode=0)

            adapter = DirtyWatersAdapter()
            result = adapter.analyze("repo/test", is_local=True)

            assert result == "results/x.md"

            args = mock_run.call_args[0][0]
            assert "-v" not in args