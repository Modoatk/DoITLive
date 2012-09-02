from doitlive import dropbox_adapter
from doitlive.dropbox.rest import ErrorResponse
y=dropbox_adapter.DropboxAdapter('h9j5r8xzwq8twxn','af33a3wtka2t8tc')
y.login()

try:
	print y.read_file('/six.py')
except ErrorResponse as e:
	print e.status == 404

