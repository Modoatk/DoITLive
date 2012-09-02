import calendar
import os

from errno import ENOENT
from fuse import Operations, LoggingMixIn, FuseOSError

import dropbox_adapter
import dto

def catch_not_found(f):
    """Decorator to deal with dropbox_adapter.FileNotFoundException."""

    def decorated_func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except dropbox_adapter.FileNotFoundException:
            raise FuseOSError(ENOENT)

    return decorated_func

class FuseAdapter(Operations, LoggingMixIn):
    """Adapter to register through FUSE for creating file system."""

    def __init__(self, dropbox_adapter):
        """Create a new FUSE adapter.

        @param dropbox_adapter: Adapter for dropbox to operate on.
        @type dropbox_adapter: dropbox_adapter.DropboxAdapter
        """
        # TODO(apottinger): Cache
        self.__dropbox_adapter = dropbox_adapter

    def create(self, path, unused_mode):
        """FUSE hook for creating a new empty file.

        @param path: The absolute path of the file to create.
        @type path: String
        @return: OS native status code
        @rtype: int
        """
        self.__dropbox_adapter.save_file(path, "")
        return 0 # TODO(apottinger): Proper error reporting from dropbox adapter

    @catch_not_found
    def getattr(self, path, unused_fh=None):
        """Get the metadata for a file.

        @param path: The absolute path of the file to get metadata for.
        @type path: String
        @return: Metadata for file.
        @rtype: dict
        """
        raw_metadata = self.__dropbox_adapter.get_metadata(path)
        metadata = dto.FileInfoDecorator(raw_metadata)

        attrs = {
            'st_gid': os.getegid(),
            'st_mode': metadata.get_mode(),
            'st_size': metadata.get_size(),
            'st_uid': os.getuid()
        }

        if not metadata.is_directory():
            mtime = calendar.timegm(metadata.get_modified())
            attrs['st_atime'] = mtime # TODO: Created?
            attrs['st_mtime'] = mtime

        return attrs

    @catch_not_found
    def mkdir(self, path, unused_mode):
        """Make a new directory.

        @param path: The absolute path of the directory to create.
        @type path: String
        @return: OS native status code
        @rtype: int
        """
        self.__dropbox_adapter.make_directory(path)
        return 0 # TODO(apottinger): Proper error reporting from dropbox adapter

    @catch_not_found
    def read(self, path, size, offset, unused_fh):
        """Read the contents of a file.

        @param path: The absolute path of the file to read.
        @type path: String
        @param size: The number of bytes to read from the file.
        @type size: int
        @param offset: The number of bytes to skip at the beginning of the file.
        @type offset: int
        @return: Contents of the file.
        @rtype: String
        """
        contents = self.__dropbox_adapter.read_file(path)
        return contents[offset:size]

    @catch_not_found
    def readdir(self, path, unused_fh):
        """Get the contents of a directory.

        @param path: The absolute path of the directory to read.
        @type path: String
        @return: List of items in the given directory.
        @rtype: Iterable over string.
        """
        names = self.__dropbox_adapter.list_directory_contents(path)
        return ['.', '..'] + names

    @catch_not_found
    def rename(self, old, new):
        """Rename a file.

        @param old: The old absolute path of the file.
        @type old: String
        @param new: The new absolute path for the file.
        @type new: String
        @return: System status code.
        @rtype: int
        """
        # TODO(apottinger): Check to make sure new is in app dir
        # TODO(apottinger): Handle moving outside of dropbox
        # TODO(apottinger): Check for errors
        self.__dropbox_adapter.move(old, new)
        return 0

    @catch_not_found
    def rmdir(self, path):
        """Remove a directory.

        @param path: The old absolute path of the directory to remove.
        @type path: String
        @return: System status code.
        @rtype: int
        """
        self.__dropbox_adapter.remove(path)
        return 0 # TODO(apottinger): Proper error reporting from dropbox adapter

    @catch_not_found
    def truncate(self, path, length, fh=None):
        """Reduce the size of a file by removing the later part of the file.

        @param path: The absolute path of the file to truncate.
        @type path: String
        @param length: The number of bytes to make the file.
        @type length: int
        @return: System status code.
        @rtype: int
        """
        new_contents = self.read(path, length, 0, None)
        self.write(path, new_contents, 0, None)
        return 0 # TODO(apottinger): Proper error reporting from dropbox adapter

    @catch_not_found
    def unlink(self, path):
        """Remove a file.

        @param path: The absolute path of the file to delete.
        @type path: String
        @return: System status code.
        @rtype: int
        """
        self.__dropbox_adapter.remove(path)
        return 0 # TODO(apottinger): Proper error reporting from dropbox adapter

    @catch_not_found
    def write(self, path, data, offset, fh):
        """Write data to a file.

        @param path: The absolute path of the file to write to.
        @type path: String
        @return: Number of bytes written.
        @rtype: Int
        """
        if offset > 0:
            orig = self.__dropbox_adapter.read_file(path)[:offset]
        else:
            orig = ""
        data = orig + data
        self.__dropbox_adapter.save_file(path, data)
        return len(data)
