#This is a file from CS50 Finance
from functools import wraps

from flask import redirect, render_template, session
from threading import Thread
from flask_mail import Message
from application import app, mail

ALLOWED_EXTENSIONS = {"png", "PNG", "jpg", "jpeg", "JPG", "JPEG"}

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/sign_in")
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# Send message function
def async_send_mail(applic, msg):
    with applic.app_context():
        mail.send(msg)

def send_mail(subject, recipient, template, **kwargs):
    msg = Message(subject, recipients=[recipient])
    msg.html = render_template(template, **kwargs)
    thr = Thread(target=async_send_mail, args=[app, msg])
    thr.start()
    return thr