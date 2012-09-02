import os
import sys

import fuse

import decorators
import fuse_adapter
import dropbox_adapter
import dto

APP_KEY = "h9j5r8xzwq8twxn"
APP_SECRET = "af33a3wtka2t8tc"     


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print 'usage: %s <mountpoint>' % sys.argv[0]
        exit(1)

    full_path = os.path.abspath(sys.argv[1])

    dropbox_adapter = dropbox_adapter.DropboxAdapter(APP_KEY, APP_SECRET)
    dropbox_adapter.login()
    decorated_dropbox_adapter = decorators.DropboxAdapterPathDecorator(
            dropbox_adapter,
            full_path
    )
    fuse.FUSE(fuse_adapter.FuseAdapter(decorated_dropbox_adapter), sys.argv[1], foreground=True)