import pytest
import os

from .vars import ASSETS_DIR, SERIES_CONFIGPARSE
from .utils import empty_folder

from tests.utils import ConfigFileInjector, RuleBookFileInjector

from video_file_organizer.config import ConfigFile, RuleBookFile


def test_configfile(tmp_dir):
    # ValueError because required fields are not entered
    with pytest.raises(ValueError):
        ConfigFile(os.path.join(tmp_dir, 'config.yaml'))

    # Check if config file was created
    assert os.path.isfile(os.path.join(tmp_dir, 'config.yaml'))

    config_injector = ConfigFileInjector(tmp_dir)
    config_injector.update({
        "series_dirs": [os.path.join(tmp_dir, "series_dirs")],
        "input_dir": os.path.join(tmp_dir, "input_dir")
    })

    # FileNotFoundError because the directory doesn't exist
    with pytest.raises(FileNotFoundError):
        ConfigFile(config_injector.path)

    empty_folder(tmp_dir)

    config_injector = ConfigFileInjector(tmp_dir)
    os.mkdir(os.path.join(tmp_dir, "series_dirs"))
    os.mkdir(os.path.join(tmp_dir, "input_dir"))
    config_injector.update({
        "series_dirs": [os.path.join(tmp_dir, "series_dirs")],
        "input_dir": os.path.join(tmp_dir, "input_dir"),
        "before_scripts": [os.path.join(ASSETS_DIR, "fail_script.sh")]
    })
    # CalledProcessError because the script failed
    with pytest.raises(SystemExit):
        ConfigFile(config_injector.path)

    empty_folder(tmp_dir)

    config_injector = ConfigFileInjector(tmp_dir)
    os.mkdir(os.path.join(tmp_dir, "series_dirs"))
    os.mkdir(os.path.join(tmp_dir, "input_dir"))
    config_injector.update({
        "series_dirs": [os.path.join(tmp_dir, "series_dirs")],
        "input_dir": os.path.join(tmp_dir, "input_dir")
    })
    # Successful ConfigFile exec
    ConfigFile(config_injector.path)


def test_rulebookfile(tmp_dir):
    # Missing Arguments
    with pytest.raises(TypeError):
        RuleBookFile()

    # Check if rulebook file was created
    RuleBookFile(os.path.join(tmp_dir, 'rule_book.ini'))
    assert os.path.isfile(os.path.join(tmp_dir, 'rule_book.ini'))

    rule_book_injector = RuleBookFileInjector(tmp_dir)
    rule_book_injector.update('series', {
        'That 70s Show': 'invalid-rule'
    })
    # Test invalid rule
    with pytest.raises(KeyError):
        RuleBookFile(rule_book_injector.path)

    empty_folder(tmp_dir)

    rule_book_injector = RuleBookFileInjector(tmp_dir)
    rule_book_injector.update('series', {
        'That 70s Show': 'sub-dir'
    })
    # Test secondary rule without value
    RuleBookFile(rule_book_injector.path)

    empty_folder(tmp_dir)

    rule_book_injector = RuleBookFileInjector(tmp_dir)
    rule_book_injector.update('series', SERIES_CONFIGPARSE)
    # Successful RuleBookfile exec
    RuleBookFile(rule_book_injector.path)
