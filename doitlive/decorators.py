import datetime
import os
from dropbox import client, rest, session

class DropboxAdapterPathDecorator:
    """Decorator around a dropbox adapter that adjusts paths."""

    def __init__(self, adapter, base_path):
        self.__adapter = adapter
        self.__base_path = base_path

    def login(self):
        """Log in to a Dropbox account."""
        self.__adapter.login()

    def logout(self):
        """Log out of the current Dropbox account."""
        self.__adapter.logout()

    def list_directory_contents(self, path):
        """Get all of the items in a directory.
        
        @param path: The relative path of directory to get contents of
        @type path: String
        @return: Contents of directory
        @rtype: List
        """
        return self.__adapter.list_directory_contents(self.__fix_path(path))

    def make_directory(self, path):
        """Create a new directory in a user's Dropbox.

        @param path: The relative path of directory to be created
        @type path: String
        """
        self.__adapter.make_directory(self.__fix_path(path))

    def remove(self, path):
        """Remove a file / directory from a user's Dropbox.

        @param path: The relative path of item to be removed
        @type path: String
        """
        self.__adapter.remove(self.__fix_path(path))

    def move(self, start, end):
        """Move a file / directory in a user's Dropbox.

        @param start: The relative path of item's current location
        @type start: String
        @param end: The relative path to move item to
        @type end: String
        """
        start = self.__fix_path(start)
        end = self.__fix_path(end)
        self.__adapter.move(start,end)

    def get_metadata(self, path):
        """Get the metadata for a file or folder.

        @param path: The relative path of item to retrieve metadata from.
        @type path: String
        @return: The metadata of provided item.
        @rtype: Dict
        """
        return self.__adapter.get_metadata(self.__fix_path(path))
    
    def read_file(self, path):
        """Get the contents of a file or folder.

        @param path: The relative path of file to retrieve contents of
        @type path: String
        @return: The contents of provided file
        @rtype: String
        """
        return self.__adapter.read_file(self.__fix_path(path))

    def save_file(self, path, data, overwrite=True):
        """Write to a file.

        @param path: The relative path of file to be saved
        @type path: String
        @param data: The contents of file being saved
        @type data: ????
        @param overwrite: Whether to overwrite an existing file
        @type overwrite: Boolean
        """
        self.__adapter.save_file(self.__fix_path(path), data, overwrite)

    def __fix_path(self, orig_path):
        """Create a relative path for the given path.

        @param orig_path: The absolute path to fix.
        @type orig_path: String
        @return: Path relative to base of Dropbox folder.
        @rtype: String
        """
        if orig_path.startswith(self.__base_path):
            return orig_path[len(self.__base_path):]
        else:
            return orig_path


class CacheEntry(object):

    def __init__(self, payload):
        self.__payload = payload
        self.__creation = datetime.datetime.now()

    def has_expired(self, lifetime):
        return datetime.datetime.now() > self.__creation + datetime.timedelta(seconds=lifetime)

    def get_payload(self):
        return self.__payload


class DropboxAdapterCachingDecorator(object):
    """Decorator around a dropbox adapter that caches results from Dropbox."""

    def __init__(self, adapter, timeout=300):
        self.__adapter = adapter
        self.__timeout = timeout
        self.__directory_contents = {}
        self.__metadata = {}
        self.__file_contents = {}

    def login(self):
        """Log in to a Dropbox account."""
        self.__adapter.login()

    def logout(self):
        """Log out of the current Dropbox account."""
        self.__adapter.logout()

    def list_directory_contents(self, path):
        """Get all of the items in a directory.
        
        @param path: The relative path of directory to get contents of
        @type path: String
        @return: Contents of directory
        @rtype: List
        """
        if not self.__has_cached(self.__directory_contents, path):
            contents = self.__adapter.list_directory_contents(path)
            self.__directory_contents[path] = CacheEntry(contents)
        return self.__directory_contents[path].get_payload()

    def make_directory(self, path):
        """Create a new directory in a user's Dropbox.

        @param path: The relative path of directory to be created
        @type path: String
        """
        self.__invalidate_parent_cache(self.__directory_contents, path)
        self.__adapter.make_directory(path)

    def remove(self, path):
        """Remove a file / directory from a user's Dropbox.

        @param path: The relative path of item to be removed
        @type path: String
        """
        self.__invalidate_parent_cache(self.__directory_contents, path)
        self.__invalidate_cache(self.__file_contents, path)
        self.__adapter.remove(path)

    def move(self, start, end):
        """Move a file / directory in a user's Dropbox.

        @param start: The relative path of item's current location
        @type start: String
        @param end: The relative path to move item to
        @type end: String
        """
        self.__invalidate_parent_cache(self.__directory_contents, start)
        self.__invalidate_cache(self.__file_contents, start)
        self.__invalidate_parent_cache(self.__directory_contents, end)
        self.__invalidate_cache(self.__file_contents, end)

        self.__adapter.move(start,end)

    def get_metadata(self, path):
        """Get the metadata for a file or folder.

        @param path: The relative path of item to retrieve metadata from.
        @type path: String
        @return: The metadata of provided item.
        @rtype: Dict
        """
        if not self.__has_cached(self.__metadata, path):
            metadata = self.__adapter.get_metadata(path)
            self.__metadata[path] = CacheEntry(metadata)
        return self.__metadata[path].get_payload()
    
    def read_file(self, path):
        """Get the contents of a file or folder.

        @param path: The relative path of file to retrieve contents of
        @type path: String
        @return: The contents of provided file
        @rtype: String
        """
        if not self.__has_cached(self.__file_contents, path):
            file_contents = self.__adapter.read_file(path)
            self.__file_contents[path] = CacheEntry(file_contents)
        return self.__file_contents[path].get_payload()

    def save_file(self, path, data, overwrite=True):
        """Write to a file.

        @param path: The relative path of file to be saved
        @type path: String
        @param data: The contents of file being saved
        @type data: ????
        @param overwrite: Whether to overwrite an existing file
        @type overwrite: Boolean
        """
        self.__invalidate_cache(self.__file_contents, path)
        self.__adapter.save_file(path, data, overwrite)

    def __get_parent_dir(self, path):
        """Get the parent directory of a file / directory.

        @param path: The path to the file / directory the parent for which the
                parent is being requested.
        @type path: String
        
        """
        components = os.path.split(test2)
        parent_components = components[0:-1]
        return os.path.join(parent_components)[0]

    def __has_cached(self, cache, target):
        if not target in cache:
            return False
        elif cache[target].has_expired(self.__timeout):
            return False

        return True

    def __invalidate_cache(self, cache, target):
        if target in cache:
            del cache[target]

    def __invalidate_parent_cache(self, cache, target):
        parent = self.__get_parent_dir(target)
        self.__invalidate_cache(cache, parent)
