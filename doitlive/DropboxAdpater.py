import os

Class DropboxAdapter:
    def __init__(self, app_key, app_secret):
        #Get dropbox app key and secret
            self.APP_KEY    = app_key
            self.APP_SECRET = app_secret
        #Set Access type (either 'dropbox' or 'app_folder')
            self.ACCESS_TYPE = 'app_folder'

    def list_directory_contents(path)
        resp = self.api_client.metadata(self.current_path)
    
        if 'contents' in resp:
            for f in resp['contents']:
                name = os.path.basename(f['path'])
                encoding = locale.getdefaultlocale()[1]

    def make_directory(path):
        DropboxClient.file_create_folder(path)

    def remove(path):
        DropboxClient.file_delete(path)

    def move(start, end):
        DropboxClient.file_move(start,end)

    def get_metadata(path):
        self.metadata = DropboxClient.metadata(path)
        return x
    
    def read_file(path):
        x = DropboxClient.get_file(path).read()
        return x

    def save_file(path, data, overwrite=True):
        DropboxClient.put_file(path, data, overwrite)
        
