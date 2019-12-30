import os
from typing import Union, List
import logging

from video_file_organizer.settings import VIDEO_EXTENSIONS

logger = logging.getLogger('app.models')


class Folder:
    """A representation of a generic folder"""

    def __init__(self, path: Union[str, List[str]], ignore=[]):
        self.path = path
        # Makes sure path is a list
        if type(self.path) is not list:
            self.path = [self.path]

        self.ignore = ignore
        self.entries = self.scan()

    def scan(self) -> dict:
        """
        Returns a dict with this format
        {
            "name": {
                "_entry": <DirEntry>
                "sub_entries": {
                    "name": {
                        "_entry" : <DirEntry>
                    }
                }
            }
        }
        """
        data = {}
        for path in self.path:
            for entry in os.scandir(path):
                if entry.name in self.ignore:
                    continue
                sub_entries = {}
                if entry.is_dir():
                    for sub_entry in os.scandir(entry.path):
                        sub_entries[sub_entry.name] = {'_entry': sub_entry}
                data[entry.name] = {
                    '_entry': entry, 'sub_entries': sub_entries
                }
        return data

        def iterate_entries(self):
            for name, data in self.entries.items():
                yield name, data


class OutputFolder(Folder):
    def __init__(self, path: Union[str, List[str]], ignore=[]):
        super().__init__(path, ignore)


class InputFolder(Folder):
    def __init__(self, path: str, ignore=[]):
        if type(path) is not str:
            raise TypeError("Input Folder can only be a single folder")
        super().__init__(path, ignore)

        self._vfiles = {}
        self.scan_vfiles()

    def scan_vfiles(self):
        """
        Returns a dict with this format
        {
            "name": <VideoFile>
        }
        """
        data = {}
        for fname, fdata in self.entries.items():
            if fname.rpartition('.')[-1] in VIDEO_EXTENSIONS:
                self.add_vfile(fname, path=fdata['_entry'].path)
            if fdata['_entry'].is_dir():
                for sub_fname, sub_fdata in fdata['sub_entries'].items():
                    if sub_fname.rpartition('.')[-1] in VIDEO_EXTENSIONS:
                        self.add_vfile(
                            sub_fname, path=sub_fdata['_entry'].path)
        return data

    def add_vfile(self, name, **kwargs):
        if name in self._vfiles.keys():
            raise ValueError("This video file already exists in list")
        logger.debug(f"Added vfile {name} with kwargs {kwargs}")
        vfile = VideoFile()
        setattr(vfile, 'name', name)
        for key, value in kwargs.items():
            setattr(vfile, key, value)
        self._vfiles[name] = vfile

    def get_vfile(self, name):
        if name not in self._vfiles.keys():
            raise ValueError("This video file doesn't exists in list")
        return self._vfiles[name]

    def remove_vfile(self, name):
        if name not in self._vfiles.keys():
            raise ValueError("This video file doesn't exists in list")
        logger.debug(f"Removed vfile {name}")
        del self._vfiles[name]

    def edit_vfile(self, name: str, merge: bool = True, **kwargs):
        if name not in self._vfiles.keys():
            raise ValueError("This video file doesn't exist in list")
        logger.debug(f"Edited vfile {name} with kwargs {kwargs}")
        vfile = self._vfiles[name]
        for key, value in kwargs.items():
            setattr(vfile, key, value)

    def iterate_vfiles(self):
        for name, vfile in self._vfiles.copy().items():
            yield name, vfile


class VideoFile:
    pass
