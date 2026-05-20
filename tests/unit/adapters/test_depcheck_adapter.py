from unittest.mock import patch, Mock

from src.adapters.depcheck_adapter import DepcheckAdapter

class TestDepcheckAdapter:

    def test_analyze_npx_not_found(self):

        adapter = DepcheckAdapter()

        with patch("shutil.which", return_value=None):

            result = adapter.analyze("/fake/path")

            assert result == {
                "dependencies": [],
                "devDependencies": [],
                "missing": {},
                "bloated": []
            }


    def test_analyze_version_command_fails(self):

        adapter = DepcheckAdapter()

        with patch("shutil.which", return_value="npx"), \
             patch("subprocess.run") as mock_run:

            mock_run.return_value = Mock(returncode=1)

            result = adapter.analyze("/fake/path")

            assert result == {
                "dependencies": [],
                "devDependencies": [],
                "missing": {},
                "bloated": []
            }


    def test_analyze_empty_stdout(self):

        adapter = DepcheckAdapter()

        with patch("shutil.which", return_value="npx"), \
             patch("subprocess.run") as mock_run:

            first_call = Mock(returncode=0)
            second_call = Mock(stdout="", stderr="error")

            mock_run.side_effect = [first_call, second_call]

            result = adapter.analyze("/fake/path")

            assert result == {
                "dependencies": [],
                "devDependencies": [],
                "missing": {},
                "bloated": []
            }


    def test_analyze_valid_json(self):

        adapter = DepcheckAdapter()

        with patch("shutil.which", return_value="npx"), \
             patch("subprocess.run") as mock_run:

            first_call = Mock(returncode=0)
            second_call = Mock(
                stdout='{"dependencies":["a","b"],"devDependencies":["c"],"missing":{"d":true},"bloated":["e"]}',
                stderr=""
            )

            mock_run.side_effect = [first_call, second_call]

            result = adapter.analyze("/fake/path")

            assert result["dependencies"] == ["a", "b"]
            assert result["devDependencies"] == ["c"]
            assert "d" in result["missing"]
            assert result["bloated"] == ["e"]


    def test_analyze_invalid_json(self):

        adapter = DepcheckAdapter()

        with patch("shutil.which", return_value="npx"), \
             patch("subprocess.run") as mock_run:

            first_call = Mock(returncode=0)
            second_call = Mock(stdout="INVALID JSON", stderr="")

            mock_run.side_effect = [first_call, second_call]

            result = adapter.analyze("/fake/path")

            assert result == {
                "dependencies": [],
                "devDependencies": [],
                "missing": {},
                "bloated": []
            }