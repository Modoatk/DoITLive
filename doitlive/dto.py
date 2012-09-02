import stat
import time

class FileInfoDecorator(object):

    def __init__(self, native):
        self.__native = native

    def get_modified(self):
        return time.strptime(
            self.__native["modified"],
            "%a, %d %b %Y %H:%M:%S +0000"
        )

    def get_mode(self):
        if self.__native["is_dir"]:
            mode = stat.S_IFDIR
        else:
            mode = stat.S_IFREG

        mode |= stat.S_IRWXU | stat.S_IRWXU

        return mode

    def is_directory(self):
        return self.__native["is_dir"]

    def get_size(self):
        return self.__native['bytes']