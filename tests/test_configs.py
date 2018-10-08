import pytest
import os
import subprocess

from video_file_organizer.configs.config_handler import ConfigHandler
from tests.fixtures.setup_config import CONFIG_DIR

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")


def test_empty_config_folder(tmp_dir):
    """Test ValueError Exception on new empty config folder which indirectly
    tests:
    - Creation of new configs from templates
    - Opening and reading config.yaml
    - If all required fields are entered"""
    config_dir = os.path.join(tmp_dir, CONFIG_DIR)
    # ValueError because the required fields are not entered
    with pytest.raises(ValueError):
        ConfigHandler(config_dir=config_dir)
    # Checks the files where created by the ConfigHandler
    assert os.path.exists(config_dir)


def test_none_existing_series_and_input_dirs(tmp_config_editor, tmp_dir):
    """Test ValueError on missing series_dirs in config.yaml"""
    editor, config_dir = tmp_config_editor
    editor({
        "series_dirs": [os.path.join(config_dir, "series_dirs")],
        "input_dir": os.path.join(tmp_dir, "input_dir")
    })
    # FileNoteFoundError because the directory doesn't exist
    with pytest.raises(FileNotFoundError):
        ConfigHandler(config_dir=config_dir)


def test_failing_before_script(tmp_config_editor, tmp_dir):
    """Test if there is a fail before script"""
    editor, config_dir = tmp_config_editor
    os.mkdir(os.path.join(tmp_dir, "series_dirs"))
    os.mkdir(os.path.join(tmp_dir, "input_dir"))
    editor({
        "series_dirs": [os.path.join(tmp_dir, "series_dirs")],
        "input_dir": os.path.join(tmp_dir, "input_dir"),
        "before_scripts": [os.path.join(ASSETS_DIR, "fail_script.sh")]
    })
    # CalledProcessError because the script failed
    with pytest.raises(subprocess.CalledProcessError):
        ConfigHandler(config_dir=config_dir)
