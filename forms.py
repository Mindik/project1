import requests
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.widgets import PasswordInput

from application import db, goodreads, key

# Class for sign in form
class LoginForm(FlaskForm):
    email = StringField("email")
    password = StringField('password', widget=PasswordInput(hide_value=False))

    # Check email in db
    def checkDb(self):
        check = db.execute("SELECT * FROM users WHERE email = :email", {"email": self.email.data.lower()}).fetchall()
        db.commit()
        return check

# Class for resend email
class ResendMail(FlaskForm):
    email = StringField("email")

    # Check email in db
    def checkDb(self):
        check = db.execute("SELECT * FROM users WHERE email = :email", {"email": self.email.data.lower()}).fetchall()
        db.commit()
        return check

# Class for sign up form
class SignUp(FlaskForm):
    firstname = StringField("firstname")
    lastname = StringField("lastname")
    email = StringField("email")
    password = StringField('password', widget=PasswordInput(hide_value=False))

    # Check email in db
    def checkDb(self):
        check = db.execute("SELECT * FROM users WHERE email = :email", {"email": self.email.data.lower()}).rowcount
        db.commit()
        return check

    # Insert new user in db
    def insertDb(self, hash_pass, hash_email):
        db.execute("INSERT INTO users (firstname, lastname, email, hash_psw, verification_code)"
                   "VALUES (:firstname, :lastname, :email, :hash_psw, :verification_code)",
                   {"firstname": self.firstname.data, "lastname": self.lastname.data, "email": self.email.data.lower(),
                    "hash_psw": hash_pass,
                    "verification_code": hash_email})
        db.commit()

# Form dor forgot password
class ForgotPassword(FlaskForm):
    email = StringField("email")

    # Check email in db
    def checkDb(self):
        check = db.execute("SELECT * FROM users WHERE email = :email", {"email": self.email.data.lower()}).fetchall()
        db.commit()
        return check

# Form for change password
class ChangePass(FlaskForm):
    reset_email = HiddenField("reset_email")
    old_password = StringField('old_password', widget=PasswordInput(hide_value=False))
    new_password = StringField('new_password', widget=PasswordInput(hide_value=False))

    # Check password in db
    def checkPswDb(self):
        checkPsw = db.execute("SELECT * FROM users WHERE email = :email", {"email": self.reset_email.data.lower()}).fetchall()
        db.commit()
        return checkPsw

    # Update new password in db
    def updatePsw(self, hash_pass, id):
        db.execute("UPDATE users SET hash_psw = :hash_psw WHERE id = :id", {"hash_psw": hash_pass, "id": id})
        db.commit()

# Form for reset password
class ResetPass(FlaskForm):
    reset_email = HiddenField("reset_email")
    new_password = StringField('new_password', widget=PasswordInput(hide_value=False))

    # Check email in db
    def checkDb(self):
        check = db.execute("SELECT * FROM users WHERE email = :email", {"email": self.reset_email.data.lower()}).fetchall()
        db.commit()
        return check

    # Update new password in db
    def updateDb(self, hash_pass, id):
        db.execute("UPDATE users SET hash_psw = :hash_psw WHERE id = :id", {"hash_psw": hash_pass, "id": id})
        db.commit()

# Class user
class User:
    # Init id
    def __init__(self, id):
        self.id = id

    # Information from the database
    def infoDb(self):
        info = db.execute("SELECT * FROM users WHERE id = :id", {"id": self.id}).fetchall()
        db.commit()
        return info

    # Information from the database given for rating and counter
    def countDb(self):
        count = db.execute("select count(review_text), count(score) from reviews WHERE users_id = :id", {"id": self.id}).fetchall()
        db.commit()
        return count

# Form for change email
class ChangeEmail(FlaskForm):
    email = StringField("email")
    password = StringField('password', widget=PasswordInput(hide_value=False))

    # Check email in db
    def checkDbEmail(self):
        check = db.execute("SELECT * FROM users WHERE email = :email", {"email": self.email.data.lower()}).fetchall()
        db.commit()
        return check

    # Check id in db
    def checkDb(self, id):
        check = db.execute("SELECT * FROM users WHERE id = :id", {"id": id}).fetchall()
        db.commit()
        return check

    # Update db
    def updateDb(self, id, verification_code):
        db.execute("UPDATE users SET email = :email, verification = 0, verification_code = :verification_code WHERE id = :id",
                   {"verification_code": verification_code, "id": id, "email": self.email.data.lower()})
        db.commit()

# Class for information book page
class BookPageInfo:
    def __init__(self, isbn):
        self.isbn = isbn

    # book information
    def infoBookIsbn(self):
        info = db.execute("SELECT books.isbn, books.title, books.author, "
                   "books.year, img_text.less, img_text.more, img_text.img_name, "
                   "rating.review_count, rating.average_score "
                   "FROM books "
                   "LEFT JOIN img_text ON img_text.books_id = books.id "
                   "LEFT JOIN rating ON rating.books_id = books.id "
                   "WHERE isbn = :isbn", {"isbn": self.isbn}).fetchall()
        db.commit()
        return info

    # book reviews
    def reviewDb(self):
        review = db.execute("SELECT reviews.review_text, reviews.score, reviews.users_id, users.firstname, users.lastname,"
                            " users.avatar_img FROM reviews "
                            "JOIN books ON books.id = reviews.books_id "
                            "JOIN users ON reviews.users_id = users.id "
                            "WHERE books.isbn = :isbn",
                            {"isbn": self.isbn}).fetchall()
        db.commit()
        return review

    # JSON goodreads
    def goodReads(self):
        res = requests.get(goodreads, params={"key": key, "isbns": self.isbn})
        if res.status_code != 200:
            return None
        return res.json()

# Class for reviews
class Reviews:
    def __init__(self, isbn, score, text):
        self.isbn = isbn
        self.score = score
        self.text = text

    # Check user in db
    def idDb(self):
        id = db.execute("SELECT id FROM books WHERE isbn = :isbn", {"isbn": self.isbn}).fetchall()
        db.commit()
        return id[0].id

    # Insert new review
    def insertDb(self, user, id):
        db.execute("INSERT INTO reviews (review_text, score, users_id, books_id)"
                   "VALUES (:review_text, :score, :users_id, :books_id)",
                   {"review_text": self.text, "score": self.score, "users_id": user,
                    "books_id": id})
        db.commit()

    # Select new reviews data
    def avgCount(self, id):
        avg_count = db.execute("SELECT round(AVG(score),2), COUNT(id) FROM reviews WHERE books_id = :id",
                                {"id": id}).fetchall()
        db.commit()
        return avg_count

    # Update new rating
    def updateDB(self, count, score, id):
        if db.execute("SELECT * FROM rating WHERE books_id = :id", {"id": id}).fetchall():
            db.execute("UPDATE rating SET review_count = :count, average_score = :score WHERE books_id = :id",
                       {"count": count, "score": score, "id": id})
            db.commit()
        else:
            db.execute("INSERT INTO rating (review_count, average_score, books_id) "
                       "VALUES (:count, :score, :id)", {"count": count, "score": score, "id": id})
            db.commit()

    # Data user for new review
    def newReview(self, id):
        name = db.execute("SELECT firstname, lastname, avatar_img FROM users WHERE id = :id", {"id": id}).fetchall()
        db.commit()
        return name

# API
class Api:
    def __init__(self, isbn):
        self.isbn = isbn

    def infoApi(self):
        infoApi = db.execute("SELECT books.title, books.author, books.year, books.isbn, rating.review_count, "
                             "rating.average_score FROM books JOIN rating ON rating.books_id = books.id WHERE isbn = "
                             ":isbn", {"isbn": self.isbn}).fetchall()
        db.commit()
        return infoApi
