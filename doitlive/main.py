import os
import sys

import fuse

import decorators
import fuse_adapter
import dropbox_adapter
import dto

APP_KEY = "h9j5r8xzwq8twxn"
APP_SECRET = "af33a3wtka2t8tc"     


def start_service(relative_path):
    """Start the FUSE file system that mirrors a user's Dropbox.

    @param full_path: Path to where the FUSE file system should be mounted.
    @type full_path: String
    """
    full_path = os.path.abspath(relative_path)
    dropbox = dropbox_adapter.DropboxAdapter(APP_KEY, APP_SECRET)
    dropbox.login()

    decorated_dropbox = decorators.DropboxAdapterPathDecorator(
            dropbox,
            full_path
    )
    decorated_dropbox = decorators.DropboxAdapterCachingDecorator(
        decorated_dropbox)

    fuse.FUSE(fuse_adapter.FuseAdapter(
        decorated_dropbox),
        full_path,
        foreground=True
    )

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print 'usage: %s <mountpoint>' % sys.argv[0]
        exit(1)

    full_path = os.path.abspath(sys.argv[1])

    start_service(full_path)