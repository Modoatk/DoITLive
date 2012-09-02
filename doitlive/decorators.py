import os
from dropbox import client, rest, session

class DropboxAdapterPathDecorator:
    """Decorator around a dropbox adapter that adjusts paths."""

    def __init__(self, adapter, base_path):
        self.__adapter = adapter
        self.__base_path = base_path

    def login(self):
        """log in to a Dropbox account"""
        self.__adapter.login()

    def logout(self):
        """log out of the current Dropbox account"""
        self.__adapter.logout()

    def list_directory_contents(self, path):
        return self.__adapter.list_directory_contents(self.__fix_path(path))

    def make_directory(self, path):
        self.__adapter.make_directory(self.__fix_path(path))

    def remove(self, path):
        self.__adapter.remove(self.__fix_path(path))

    def move(self, start, end):
        start = self.__fix_path(start)
        end = self.__fix_path(end)
        self.__adapter.move(start,end)

    def get_metadata(self, path):
        return self.__adapter.get_metadata(self.__fix_path(path))
    
    def read_file(self, path):
        return self.__adapter.read_file(self.__fix_path(path))

    def save_file(self, path, data, overwrite=True):
        self.__adapter.save_file(self.__fix_path(path), data, overwrite)

    def __fix_path(self, orig_path):
        if orig_path.startswith(self.__base_path):
            return orig_path[len(self.__base_path):]
        else:
            return orig_path
