import os
import logging
import tempfile
import yg.lockfile

from typing import Union

from video_file_organizer.config import ConfigDirectory
from video_file_organizer.models import VideoCollection, FolderCollection
from video_file_organizer.matchers import OutputFolderMatcher, \
    RuleBookMatcher, MetadataMatcher
from video_file_organizer.transferer import Transferer
from video_file_organizer.rules import rules_before_matching_vfile, \
    rules_before_transfering_vfile

logger = logging.getLogger('vfo.app')


class App:
    def setup(
            self,
            config_dir: Union[str, None] = None,
            create: bool = False
    ) -> None:

        logger.debug("Setting up app")

        self.configdir = ConfigDirectory(config_dir, create)
        self.config = self.configdir.configfile
        self.rulebook = self.configdir.rulebookfile

    def run(self, **kwargs) -> None:

        logger.debug("Running app")

        try:
            with yg.lockfile.FileLock(
                    os.path.join(tempfile.gettempdir(), 'vfolock'),
                    timeout=10):

                output_folder = FolderCollection(self.config.series_dirs)
                input_folder = VideoCollection(
                    self.config.input_dir,
                    videoextensions=self.config.videoextensions)

                metadata_matcher = MetadataMatcher()
                rulebook_matcher = RuleBookMatcher(self.rulebook)
                folder_matcher = OutputFolderMatcher(output_folder)

                operations = [
                    metadata_matcher,
                    rulebook_matcher,
                    rules_before_matching_vfile,
                    folder_matcher,
                    rules_before_transfering_vfile,
                ]

                with input_folder as ifolder:
                    for vfile in ifolder:
                        for operation in operations:
                            operation(vfile=vfile) or \
                                vfile.edit(valid=False)
                        if not vfile.valid:
                            continue

                # Transfer
                with Transferer() as transferer:
                    for vfile in input_folder:
                        transferer.transfer_vfile(vfile)

        except yg.lockfile.FileLockTimeout:
            logger.warning(
                "Lockfile FAILED: The program must already be running")
