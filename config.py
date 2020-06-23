from tempfile import mkdtemp

CSRF_ENABLED = True
SECRET_KEY = "\xb3\xc6\xd5\xaeYS9\x919\x812\x99a\x03L8y\xf6\x16\r\xb9,\x19\xc2"
TESTING = False
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = "cs50web.project1.perm@gmail.com"
MAIL_PASSWORD = "CS50web_project1_perm353"
MAIL_DEFAULT_SENDER = "cs50web.project1.perm@gmail.com"
MAIL_MAX_EMAILS = None
MAIL_ASCII_ATTACHMENTS = False
TEMPLATES_AUTO_RELOAD = True
MAX_CONTENT_LENGTH = 5 * 1024 * 1024
UPLOAD_FOLDER = "./static/ava"
SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"
SESSION_FILE_DIR = mkdtemp()
PROPAGATE_EXCEPTIONS = True
JSON_SORT_KEYS = False
