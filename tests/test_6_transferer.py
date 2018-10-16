import os
import pytest
import tempfile
import yg.lockfile

from tests.utils.injectors import setup_app_with_injectors

from tests.fixtures.setup_assets import SERIES_CONFIGPARSE


def test_lockfile(tmp_config_dir, tmp_dir):
    app, config_injector, rule_book_injector = setup_app_with_injectors(
        tmp_config_dir)
    rule_book_injector.configparse['series'] = SERIES_CONFIGPARSE
    rule_book_injector.save()
    config_injector.append({
        "input_dir": tmp_dir,
        "series_dirs": [tmp_dir]
    })
    app.setup()
    with yg.lockfile.FileLock(
            os.path.join(tempfile.gettempdir(), 'vfo_lock'), timeout=10):
        with pytest.raises(yg.lockfile.FileLockTimeout):
            app.run()


def test_success_transferer(tmp_config_dir,
                            extract_input_dir,
                            extract_series_dirs):
    app, config_injector, rule_book_injector = setup_app_with_injectors(
        tmp_config_dir)
    rule_book_injector.configparse['series'] = SERIES_CONFIGPARSE
    rule_book_injector.save()
    config_injector.append({
        "input_dir": extract_input_dir,
        "series_dirs": extract_series_dirs
    })
    app.setup()
    app.run()
