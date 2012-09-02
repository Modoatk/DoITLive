import os
from StringIO import StringIO

import locale
from dropbox import client, rest, session

def catch_404(f):
    """Decorator to deal with file not found on dropbox"""

    def decorated_func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except rest.ErrorResponse as e:
            if e.status == 404:
                raise FileNotFoundException(str(e))
            else: raise DropboxException(str(e))

    return decorated_func

class DropboxException(Exception):
    pass

class FileNotFoundException(Exception):
    pass

class DropboxAdapter:
    """Define file operation functions"""
        #Access type can be either 'dropbox' or 'app_folder'
    def __init__(self, app_key, app_secret, access_type = 'app_folder'):
        #Initialize dropbox api client
        self.sess = StoredSession(app_key, app_secret, access_type)
        self.api_client = client.DropboxClient(self.sess)

    def login(self):
        """log in to a Dropbox account"""
        try:
            if not self.sess.load_creds():
                self.sess.link()
        except rest.ErrorResponse, e:
            self.stdout.write('Error: %s\n' % str(e))

    def logout(self):
        """log out of the current Dropbox account"""
        self.sess.unlink()

    @catch_404
    def list_directory_contents(self, path):
        """
        @param path: The relative path of directory to get contents of
        @type path: String
        @return: Contents of directory
        @rtype: List
        """
        resp = self.api_client.metadata(path)
        x = []
    
        if 'contents' in resp:
            for f in resp['contents']:
                name = os.path.basename(f['path'])
                encoding = locale.getdefaultlocale()[1]
                x.append(name.encode(encoding))
        return x

    @catch_404
    def make_directory(self, path):
        """
        @param path: The relative path of directory to be file_create_folder
        @type path: String
        """
        self.api_client.file_create_folder(path)

    @catch_404
    def remove(self, path):
        """
        @param path: The relative path of item to be removed
        @type path: String
        """
        self.api_client.file_delete(path)

    @catch_404
    def move(self, start, end):
        """
        @param start: The relative path of item's current location
        @type start: String
        @param end: The relative path to move item to
        @type end: String
        """
        self.api_client.file_move(start,end)

    @catch_404
    def get_metadata(self, path):
        """
        @param path: The relative path of file to retrieve metadata from
        @type path: String
        @return: The metadata of provided file
        @rtype: Dict
        """
        x = self.api_client.metadata(path)
        return x
    
    @catch_404
    def read_file(self, path):
        """
        @param path: The relative path of file to retrieve contents of
        @type path: String
        @return: The contents of provided file
        @rtype: String
        """
        x = self.api_client.get_file(path).read()
        return x

    @catch_404
    def save_file(self, path, data, overwrite=True):
        """
        @param path: The relative path of file to be saved
        @type path: String
        @param data: The contents of file being saved
        @type data: ????
        @param overwrite: Whether to overwrite an existing file
        @type overwrite: Boolean
        """
        self.api_client.put_file(path, StringIO(data), overwrite)
        
class StoredSession(session.DropboxSession):
    """a wrapper around DropboxSession that stores a token to a file on disk"""
    TOKEN_FILE = "token_store.txt"

    def load_creds(self):
        """Load tokens from local file"""
        try:
            stored_creds = open(self.TOKEN_FILE).read()
            self.set_token(*stored_creds.split('|'))
            print "[loaded access token]"
            return True
        except IOError:
            return False

    def write_creds(self, token):
        """
        @param token: App's authentication token
        @type token: String
        """
        f = open(self.TOKEN_FILE, 'w')
        f.write("|".join([token.key, token.secret]))
        f.close()

    def delete_creds(self):
        """Delete local token file"""
        os.unlink(self.TOKEN_FILE)

    def link(self):
        """Link app to dropbox account"""
        request_token = self.obtain_request_token()
        url = self.build_authorize_url(request_token)
        print "url:", url
        print "Please authorize in the browser. After you're done, press enter."
        raw_input()

        self.obtain_access_token(request_token)
        self.write_creds(self.token)

    def unlink(self):
        """Unlink app from dropbox account"""
        self.delete_creds()
        session.DropboxSession.unlink(self)
