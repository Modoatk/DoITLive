import os
from dropbox import client, rest, session

class DropboxAdapter:
    """Define file operation functions"""
    def __init__(self, app_key, app_secret, access_type = 'app_folder'):
        #comment
        self.sess = StoredSession(app_key, app_secret, access_type)
        self.api_client = client.DropboxClient(self.sess)
        #Set Access type (either 'dropbox' or 'app_folder')

    def login(self):
        """log in to a Dropbox account"""
        try:
            self.sess.link()
        except rest.ErrorResponse, e:
            self.stdout.write('Error: %s\n' % str(e))

    def logout(self):
        """log out of the current Dropbox account"""
        self.sess.unlink()

    def list_directory_contents(self, path):
        resp = self.api_client.metadata(path)
    
        if 'contents' in resp:
            for f in resp['contents']:
                name = os.path.basename(f['path'])
                encoding = locale.getdefaultlocale()[1]
                x += name.encode(encoding)
        return x

    def make_directory(self, path):
        self.api_client.file_create_folder(path)

    def remove(self, path):
        self.api_client.file_delete(path)

    def move(self, start, end):
        self.api_client.file_move(start,end)

    def get_metadata(self, path):
        x = self.api_client.metadata(path)
        return x
    
    def read_file(self, path):
        x = self.api_client.get_file(path).read()
        return x

    def save_file(self, path, data, overwrite=True):
        self.api_client.put_file(path, data, overwrite)
        
class StoredSession(session.DropboxSession):
    """a wrapper around DropboxSession that stores a token to a file on disk"""
    TOKEN_FILE = "token_store.txt"

    def load_creds(self):
        try:
            stored_creds = open(self.TOKEN_FILE).read()
            self.set_token(*stored_creds.split('|'))
            print "[loaded access token]"
        except IOError:
            pass # don't worry if it's not there

    def write_creds(self, token):
        f = open(self.TOKEN_FILE, 'w')
        f.write("|".join([token.key, token.secret]))
        f.close()

    def delete_creds(self):
        os.unlink(self.TOKEN_FILE)

    def link(self):
        request_token = self.obtain_request_token()
        url = self.build_authorize_url(request_token)
        print "url:", url
        print "Please authorize in the browser. After you're done, press enter."
        raw_input()

        self.obtain_access_token(request_token)
        self.write_creds(self.token)

    def unlink(self):
        self.delete_creds()
        session.DropboxSession.unlink(self)
