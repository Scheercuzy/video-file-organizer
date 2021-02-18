import os
import abc
import logging
import hashlib

from typing import Union
from video_file_organizer.database.controller import Database

logger = logging.getLogger('vfo.entries')


class ListOfEntries(metaclass=abc.ABCMeta):
    _entries: list = []

    @property
    def entries(self) -> list:
        if not self._entries:
            self._entries = self._scan_entries()
        return self._entries

    @entries.setter
    def entries(self, entries: list):
        self._entries = entries

    @abc.abstractmethod
    def _scan_entries(self) -> list:
        return []

    def __iter__(self):
        for entry in self.entries:
            yield entry

    def __getitem__(self, key: int):
        if not self.entries:
            self.entries = self._scan_entries()
        return self.entries[key]

    def __delitem__(self, key: Union[int, str]):
        pass

    def __setitem__(self, key: Union[int, str]):
        pass

    def __len__(self) -> int:
        return len(self.entries)

    def get_entry_by_name(self, name: str):
        for entry in self.entries:
            if entry.name == name:
                return entry
        raise KeyError(f"Couldn't find an entry with the name '{name}'")

    def list_entries_by_name(self) -> list:
        return [entry.name for entry in self.entries]

    def _map_entry_to_entry_type(
            self,
            entry: os.DirEntry,
            videoextensions: list,
            depth: int,
            database: Database = None):
        # NOTE: Check if its a Directory
        if entry.is_dir():
            return DirectoryEntry(
                entry.name, entry.path, depth + 1, videoextensions, database)
        else:
            ext = entry.name.rpartition('.')[-1]

            # NOTE: Check if its a Video File
            if ext in videoextensions:
                return VideoFileEntry(
                    entry.name, entry.path, ext, depth + 1, database)
            else:
                return FileEntry(entry.name, entry.path, ext, depth + 1)


class InputDirectory(ListOfEntries):
    def __init__(
        self,
        path: str,
        *,
        videoextensions: list = [],
        ignore: list = [],
        whitelist: list = [],
        database: Database
    ):
        self.path = path
        self.videoextensions = videoextensions
        self.depth = 0
        self.ignore = ignore
        self.whitelist = whitelist
        self.videofilelist = []
        self.database = database

        self._scan_entries_for_vfile(self.entries)

    def _scan_entries(self):
        entries: list = []
        for entry in os.scandir(self.path):

            if entry.name in self.ignore:
                continue

            if self.whitelist:
                if entry.name in self.whitelist:
                    entries.append(self._map_entry_to_entry_type(
                        entry,
                        self.videoextensions,
                        self.depth,
                        self.database))
                    continue

            entries.append(self._map_entry_to_entry_type(
                entry,
                self.videoextensions,
                self.depth,
                self.database))
        return entries

    def _scan_entries_for_vfile(self, entries, depth=0, max_depth=2):
        for entry in entries:
            if isinstance(entry, VideoFileEntry):
                self.videofilelist.append(entry)
            if isinstance(entry, DirectoryEntry):
                if depth < max_depth:
                    self._scan_entries_for_vfile(entry.entries, depth+1)

    def __repr__(self):
        return f'<{__class__.__name__} {self.path}>'


class OutputDirectories(ListOfEntries):
    def __init__(self, paths: list, videoextensions: list = []):
        self.paths = paths
        self.depth = 0
        self.videoextensions = videoextensions

    def _scan_entries(self):
        entries: list = []
        for path in self.paths:
            for entry in os.scandir(path):
                entries.append(self._map_entry_to_entry_type(
                    entry, self.videoextensions, self.depth))
        return entries

    def list_entries_by_name(self) -> list:
        return [entry.name for entry in self.entries]

    def get_entry_by_name(self, name: str):
        for entry in self.entries:
            if entry.name == name:
                return entry
        raise KeyError(f"Couldn't find an entry with the name '{name}'")

    def __repr__(self):
        return f'<{__class__.__name__} {self.paths}>'


class DirectoryEntry(ListOfEntries):
    def __init__(
        self,
        name: str,
        path: str,
        depth: int,
        videoextensions: list,
        database: Database
    ):
        self.name = name
        self.path = path
        self.depth = depth
        self.videoextensions = videoextensions
        self.database = database

    def _scan_entries(self):
        entries: list = []
        for entry in os.scandir(self.path):
            entries.append(self._map_entry_to_entry_type(
                entry, self.videoextensions, self.depth, self.database))
        return entries

    def list_entries_by_name(self) -> list:
        return [entry.name for entry in self.entries]

    def get_entry_by_name(self, name: str):
        for entry in self.entries:
            if entry.name == name:
                return entry
        raise KeyError(f"Couldn't find an entry with the name '{name}'")

    def __repr__(self):
        return f'<{__class__.__name__} {self.name}>'


class FileEntry:
    def __init__(self, name: str, path: str, extension: str, depth: int):
        self.name = name
        self.path = path
        self.extension = extension
        self.depth = depth

    def __repr__(self):
        return f'<{__class__.__name__} {self.name}>'


class VideoFileEntry:
    def __init__(
            self,
            name: str,
            path: str,
            extension: str,
            depth: int,
            database: Database):
        self.name = name
        self.path = path
        self.extension = extension
        self.depth = depth
        self.database = database
        self.metadata = {}
        self.foldermatch = None
        self.rules = []
        # self.root_path: str = ''
        self.transfer = {}
        self.valid = True
        self.error_msg = ''
        self.hash = self._create_hash(self.path)
        logger.debug(f'VIDEOFILE created: {self.name}')

        self._validate_videofile()

    def _create_hash(self, path):
        file = path
        BLOCK_SIZE = 65536

        file_hash = hashlib.sha256()
        with open(file, 'rb') as f:
            fb = f.read(BLOCK_SIZE)
            while len(fb) > 0:
                file_hash.update(fb)
                fb = f.read(BLOCK_SIZE)

        return file_hash.hexdigest()

    def _validate_videofile(self):
        if self.database.unsuccessful_vfile_exists(self.name, self.hash):
            self.error(
                f'VIDEOFILE exists in database: {self.name}',
                add_to_database=False)

    def error(self, message, add_to_database=True):
        self.valid = False
        self.error_msg = message
        if add_to_database:
            self.database.add_unsuccessful_vfile(self.name, self.hash, message)
            logger.info(
                f"VIDEOFILE '{self.name}' has error of:\n{self.error_msg}")
        return False

    def update(self, *args, merge: bool = True, **kwargs):
        if args:
            raise ValueError('Update function only takes kwargs')
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise AttributeError(f"Attribute {key} doesn't exist")
            if merge:
                if getattr(self, key) in [list, dict]:
                    orig = getattr(self, key)
                    orig.update(value)
                    value = orig
            setattr(self, key, value)
        logger.debug(
            f"VIDEOFILE '{self.name}' updated with kwargs: \n{kwargs}")

    def __repr__(self):
        return f'<{__class__.__name__} {self.name}>'
