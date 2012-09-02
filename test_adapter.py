from doitlive import dropbox_adapter
y=dropbox_adapter.DropboxAdapter('h9j5r8xzwq8twxn','af33a3wtka2t8tc')
y.login()
print y.list_directory_contents('/')
print y.get_metadata('/')
print y.read_file('/six.py')
y.remove('/six.py')

