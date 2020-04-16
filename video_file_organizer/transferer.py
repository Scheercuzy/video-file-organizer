import shutil
import os
import logging


from video_file_organizer.models import VideoFile

logger = logging.getLogger('vfo.transferer')


class Transferer:
    def __init__(self):
        pass

    def __enter__(self):
        self.delete_list = []
        return self

    def __exit__(self, type, value, traceback):
        # Removes duplicates
        self.delete_list = list(set(self.delete_list))

        for source in self.delete_list:
            try:
                os.remove(source)
            except PermissionError:
                # Getting permission error when its a folder
                shutil.rmtree(source)
            logger.info(f"Deleted {os.path.basename(source)}")
        return True

    def transfer_vfile(self, vfile: VideoFile, **kwargs):
        """A wrapper for the transfer function that uses a VideoFile object

        Args:
            vfile: an instance of VideoFile
            **kwargs:
        """
        if not isinstance(vfile, VideoFile):
            raise TypeError("vfile needs to be an instance of VideoFile")
        if not hasattr(vfile, 'transfer'):
            raise ValueError("vfile needs to have transfer as an attribute")
        if 'transfer_to' not in vfile.transfer:
            raise KeyError("transfer_to key missing in transfer attribute")

        if hasattr(vfile, 'root_path'):
            kwargs.update(root_path=getattr(vfile, 'root_path'))

        source = vfile.path
        destination = vfile.transfer['transfer_to']

        self.transfer(source, destination, **kwargs)

    def transfer(self, source: str, destination: str, **kwargs):
        """A function that transfers and deletes a source file to a destination

        Args:
            source: path to source file
            destination: path to destination
            **kwargs:
        """
        self._copy(source, destination, **kwargs)
        self._delete(source, **kwargs)

    def _copy(self, source: str, destination: str, **kwargs):
        """A function that copies a source file to a destination

        Args:
            source: path to source file
            destination: path to destination
            **kwargs:
        """
        logger.info(f"Transfering {os.path.basename(source)} to {destination}")
        shutil.copy(source, destination)

    def _delete(self, source: str, **kwargs):
        """A function that deletes the source file

        Args:
            source: path to source file
            **kwargs:
                delete (bool): Delete the file or not
                root_path (str): Deletes this path instead of source path
        """
        if 'delete' in kwargs.keys() and not kwargs['delete']:
            return

        if 'root_path' in kwargs.keys():
            self.delete_list.append(kwargs['root_path'])
            return

        self.delete_list.append(source)