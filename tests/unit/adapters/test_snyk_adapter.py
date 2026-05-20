from unittest.mock import patch, Mock

from src.adapters.snyk_adapter import SnykAdapter

class TestSnykAdapter:

    def test_npx_not_found(self):

        with patch("shutil.which", return_value=None):
            adapter = SnykAdapter()

            result = adapter.analyze("/fake/path")

            assert result["status"] == "error"
            assert result["tool"] == "snyk"
            assert result["vulnerabilities"] == []


    def test_snyk_version_command_fails(self):

        with patch("shutil.which", return_value="npx"), \
             patch("subprocess.run") as mock_run:

            mock_run.return_value = Mock(returncode=1)

            adapter = SnykAdapter()
            result = adapter.analyze("/fake/path")

            assert result["status"] == "error"
            assert result["tool"] == "snyk"
            assert result["vulnerabilities"] == []


    def test_exception_during_version_check(self):

        with patch("shutil.which", return_value="npx"), \
             patch("subprocess.run", side_effect=Exception("fail")):

            adapter = SnykAdapter()
            result = adapter.analyze("/fake/path")

            assert result["status"] == "error"
            assert result["tool"] == "snyk"
            assert result["message"] == "snyk check failed"


    def test_empty_output(self):

        with patch("shutil.which", return_value="npx"), \
             patch("subprocess.run") as mock_run:

            mock_run.side_effect = [
                Mock(returncode=0),
                Mock(stdout="", stderr="")
            ]

            adapter = SnykAdapter()
            result = adapter.analyze("/fake/path")

            assert result["status"] == "error"
            assert result["tool"] == "snyk"
            assert result["message"] == "Snyk returned empty output."
            assert result["vulnerabilities"] == []


    def test_valid_json_output(self):

        with patch("shutil.which", return_value="npx"), \
             patch("subprocess.run") as mock_run:

            mock_run.side_effect = [
                Mock(returncode=0),
                Mock(stdout='{"vulnerabilities":[{"id":"1"},{"id":"2"}]}', stderr="")
            ]

            adapter = SnykAdapter()
            result = adapter.analyze("/fake/path")

            assert result["status"] == "success"
            assert result["tool"] == "snyk"
            assert len(result["vulnerabilities"]) == 2


    def test_invalid_json_output(self):

        with patch("shutil.which", return_value="npx"), \
             patch("subprocess.run") as mock_run:

            mock_run.side_effect = [
                Mock(returncode=0),
                Mock(stdout="INVALID JSON", stderr="")
            ]

            adapter = SnykAdapter()
            result = adapter.analyze("/fake/path")

            assert result["status"] == "error"
            assert result["tool"] == "snyk"
            assert "raw_output" in result
            assert result["vulnerabilities"] == []