import json
import os
import uuid

from flask import render_template, redirect, session, request, flash, jsonify
from markupsafe import Markup
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from application import app, db
from helpers import login_required, send_mail, allowed_file
from forms import LoginForm, ResendMail, SignUp, ForgotPassword, ResetPass, User, ChangeEmail, BookPageInfo, \
    Reviews, ChangePass, Api


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        user = User(id=session["user_id"])

        countBooks = db.execute("SELECT count(id) FROM books").fetchall()
        db.commit()
        countReviews = db.execute("SELECT count(id) FROM reviews").fetchall()
        db.commit()
        countUsers = db.execute("SELECT count(id) FROM users").fetchall()
        db.commit()

        return render_template("index.html", user=user.infoDb(), review_text=user.countDb()[0][0],
                               score=user.countDb()[0][1], countBooks=countBooks[0].count,
                               countReviews=countReviews[0].count, countUsers=countUsers[0].count)


@app.route('/file_ava', methods=["POST"])
def file_ava():
    if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):
            file.filename = str(uuid.uuid4().hex) + file.filename
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db.execute("UPDATE users SET avatar_img = :avatar_img WHERE id = :id",
                       {"avatar_img": filename, "id": session["user_id"]})
            db.commit()
            return redirect("/")
        return redirect("/")


# Sign in users
@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    """Login user"""
    # Clear session
    session.clear()
    if request.method == "GET":
        # Render html page
        return render_template("sign_in.html")

    if request.method == "POST":
        # Check user in db class LoginForm (forms.py)
        form = LoginForm()
        # Check users and password. Render flash msg
        if len(form.checkDb()) < 1 or not check_password_hash(form.checkDb()[0].hash_psw, form.password.data):
            flash(Markup('''
            <div class="alert alert-danger flash" role="alert">
                Wrong login or password!
            </div>'''))
        elif form.checkDb()[0].verification == 0:
            flash(Markup('''
            <div class="alert alert-warning" role="alert">
                Verify your account!
                <br>Didn’t receive a message?
                <a class="resend" href="/resend">Resend.</a>
            </div>'''))
        else:
            # Save user id in session
            session["user_id"] = form.checkDb()[0].id
            return redirect("/")
        return render_template("sign_in.html")


# Logout
@app.route("/logout")
@login_required
def logout():
    # Clear session and redirect sign in page
    session.clear()
    return redirect("/sign_in")


# Send message again
@app.route("/resend", methods=["GET", "POST"])
def resend():
    """Resend mail"""
    if request.method == "GET":
        # Render html page
        return render_template("resend.html")

    if request.method == "POST":
        form = ResendMail()
        # Check user in DB (hash_email, verification and count row DB)
        if len(form.checkDb()) < 1 or form.checkDb()[0].verification_code == None or not check_password_hash(
                form.checkDb()[0].verification_code, form.email.data.lower()):
            flash("Check your login!")
        else:
            # Send new email
            send_mail("Resend!!", form.checkDb()[0].email, 'mail.html', hash_email=form.checkDb()[0].verification_code)
            # return message OK!
            return render_template("resend.html", ok=1)
        return render_template("resend.html")


# Sign up
@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    """Register user"""
    if request.method == "GET":
        # Check for GET request
        if request.args.get("check_reg") is not None:
            # Getting user data by GET request
            user_db = db.execute("SELECT * FROM users WHERE verification_code = :verification_code",
                                 {"verification_code": request.args.get("check_reg")}).fetchall()
            # If there is no user
            if len(user_db) == 0:
                return render_template("sign_up.html")
            else:
                # Update DB
                db.execute("UPDATE users SET verification_code = NULL, verification = 1 WHERE id = :id",
                           {"id": user_db[0].id})
            db.commit()

            return render_template("sign_up.html", verification=1)
        return render_template("sign_up.html")

    if request.method == "POST":
        form = SignUp()
        print(form.email.data)
        # Check database users
        if form.checkDb() != 0:
            flash("This mailbox is already in use!")
            return render_template("sign_up.html")
        else:
            # Hash_pass
            hash_pass = generate_password_hash(form.password.data)
            # Hash_email for verification_code :)
            hash_email = generate_password_hash(form.email.data.lower())
            # Insert DB
            form.insertDb(hash_pass, hash_email)
            # Send mail for verification!
            send_mail("Hello!", form.email.data.lower(), "mail.html", hash_email=hash_email)
            return render_template("sign_up.html", mail_send=1, name=form.firstname.data, lastname=form.lastname.data)


# Forgot password
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    """Forgot password"""
    if request.method == "GET":
        # Render html page
        return render_template("forgot_password.html")

    if request.method == "POST":
        form = ForgotPassword()
        # Check user in DB (hash_email, verification and count row DB)
        if len(form.checkDb()) == 1 and \
                check_password_hash(generate_password_hash(form.checkDb()[0].email), form.email.data.lower()):
            # Send new email
            send_mail("Reset!", form.checkDb()[0].email, 'resetMail.html',
                      hash_email=generate_password_hash(form.checkDb()[0].email), email=form.checkDb()[0].email)
            # return message OK!
            return render_template("forgot_password.html", ok=1)
        # Return message Error!
        flash("Check your login!")
        return render_template("forgot_password.html")


# Change password
@app.route("/change_pass", methods=["POST"])
def changePass():
    form = ChangePass()
    checkPsw = form.checkPswDb()

    if len(checkPsw) != 0 and check_password_hash(checkPsw[0].hash_psw, form.old_password.data):
        form.updatePsw(generate_password_hash(form.new_password.data), checkPsw[0].id)
        return render_template("fine.html", ok=3)
    return render_template("error.html", error="You have entered the wrong old password!")

# Reset password
@app.route("/reset", methods=["GET", "POST"])
def reset():
    """Reset password"""

    if request.method == "GET":
        # Check for GET requests
        if request.args.get("reset") is not None and request.args.get("email") is not None:
            # Getting user data by GET request
            user_db = db.execute("SELECT * FROM users WHERE email = :email",
                                 {"email": request.args.get("email").lower()}).fetchall()
            # If there is no user
            if len(user_db) == 0:
                return redirect("/sign_in")
            else:
                return render_template("reset.html", email=request.args.get("email").lower())
        return redirect("/sign_in")

    if request.method == "POST":
        form = ResetPass()

        # If check users return None in DB
        if form.checkDb:
            # Update password in DB
            form.updateDb(generate_password_hash(form.new_password.data), form.checkDb()[0].id)
            return render_template("reset.html", reset_pass=1)
        return render_template("reset.html", error=1, email=form.reset_email.data.lower())


@app.route("/change")
def change():
    if request.method == "GET":
        # Check for GET requests
        if request.args.get("change_email") is not None and request.args.get("email") is not None:
            # Getting user data by GET request
            user_db = db.execute("SELECT * FROM users WHERE verification_code = :verification_code",
                                 {"verification_code": request.args.get("change_email")}).fetchall()
            # If there is no user
            if len(user_db) == 0:
                return render_template("error.html", error="Error code")
            else:
                db.execute("UPDATE users SET verification = 1, verification_code = NULL WHERE id = :id",
                           {"id": user_db[0].id})
                db.commit()
                return render_template("fine.html", ok=2)
        return redirect("/sign_in")


@app.route("/change_email", methods=["POST"])
@login_required
def change_email():
    if request.method == "POST":
        form = ChangeEmail()
        if len(form.checkDbEmail()) == 0:
            if check_password_hash(form.checkDb(session["user_id"])[0].hash_psw, form.password.data):
                hash_change_email = generate_password_hash(form.email.data.lower())
                form.updateDb(session["user_id"], hash_change_email)
                # Send new email
                send_mail("Change!", form.email.data.lower(), 'changeMail.html',
                          hash_email=hash_change_email, email=form.email.data.lower())
                return render_template("fine.html", ok=1)
            return render_template("error.html", error="You entered the wrong password!")
        return render_template("error.html", error="This email address is already in use!")


# Search
@app.route('/search', methods=['POST'])
@login_required
def search():
    text_search = json.loads(request.form['name'])

    json_list = []
    result_search_db = db.execute("SELECT isbn, title, author, year, less, more, img_name, review_count, "
                                  "average_score FROM books "
                                  "LEFT JOIN img_text ON img_text.books_id = books.id "
                                  "LEFT JOIN rating ON rating.books_id = books.id "
                                  "WHERE isbn ILIKE :search or title ILIKE :search or author ILIKE :search",
                                  {"search": '%' + text_search + '%'}).fetchall()
    db.commit()

    for row in result_search_db:
        if row.review_count is None and row.average_score is None:

            row_dict = {"isbn": row.isbn, "title": row.title, "author": row.author, "year": row.year, "less": row.less,
                        "more": row.more, "img_name": row.img_name, "review_count": 0, "average_score": 0}
        else:
            row_dict = {"isbn": row.isbn, "title": row.title, "author": row.author, "year": row.year, "less": row.less,
                        "more": row.more, "img_name": row.img_name, "review_count": row.review_count,
                        "average_score": row.average_score}

        json_list.append(row_dict)

    return jsonify(json_list)


@app.route("/page_book/<isbnBook>", methods=["GET", "POST"])
@login_required
def page_book(isbnBook):

    if request.method == "GET":
        book = BookPageInfo(isbn=isbnBook)
        bookInfo = book.infoBookIsbn()
        bookReview = book.reviewDb()

        reviewError = 0
        for check in bookReview:
            if check.users_id == session["user_id"]:
                reviewError = 1


        if book.goodReads() is not None:
            goodreads_count = book.goodReads()["books"][0]["work_ratings_count"]
            goodreads_rating = book.goodReads()["books"][0]["average_rating"]
        else:
            goodreads_count = "No"
            goodreads_rating = "No"


        if bookInfo[0].more is None:
            text = bookInfo[0].less
        else:
            text = bookInfo[0].more

        if bookInfo[0].review_count is None and bookInfo[0].average_score is None:
            review_count = 0
            average_score = 0.00
            percent = 0
            color = "#f3f3f3"
            if len(bookReview) == 0:
                return render_template("page_book.html", bookInfo=bookInfo[0], review_count=review_count,
                                       average_score=average_score, percent=percent, color=color, text=text,
                                       goodreads_count=goodreads_count, goodreads_rating=goodreads_rating, reviewError=reviewError)

            return render_template("page_book.html", bookInfo=bookInfo[0], review_count=review_count,
                                   average_score=average_score, percent=percent, color=color, text=text,
                                   goodreads_count=goodreads_count, goodreads_rating=goodreads_rating, review=bookReview, reviewError=reviewError)
        else:
            percent = bookInfo[0].average_score * 100 / 5
            color = "#f55f2c"
            print(bookInfo[0].review_count)
            print(bookInfo[0].average_score)
            if len(bookReview) == 0:
                return render_template("page_book.html", bookInfo=bookInfo[0], review_count=bookInfo[0].review_count,
                                       average_score=bookInfo[0].average_score, percent=percent, color=color, text=text,
                                       goodreads_count=goodreads_count, goodreads_rating=goodreads_rating, reviewError=reviewError)

            return render_template("page_book.html", bookInfo=bookInfo[0], review_count=bookInfo[0].review_count,
                                   average_score=bookInfo[0].average_score, percent=percent, color=color, text=text,
                                   goodreads_count=goodreads_count, goodreads_rating=goodreads_rating, review=bookReview, reviewError=reviewError)


    if request.method == "POST":
        text_review = json.loads(request.form['text'])
        review = Reviews(text_review["isbn"], text_review["score"], text_review["text"])
        id = review.idDb()
        review.insertDb(session["user_id"], id)
        avg_count = review.avgCount(id)
        review.updateDB(avg_count[0].count, avg_count[0].round, id)
        name = review.newReview(session["user_id"])

        return jsonify({
            "firstname": name[0].firstname,
            "lastname": name[0].lastname,
            "text": review.text,
            "count": avg_count[0].count,
            "score": str(avg_count[0].round),
            "ava": name[0].avatar_img
        })


# API
@app.route("/api/<isbn>")
def api(isbn):
    ibook = Api(isbn)
    infoBook = ibook.infoApi()

    if len(infoBook) == 0:
        return jsonify({"error": "Book not found"}), 404
    print(infoBook)
    return jsonify({
        "title": infoBook[0].title,
        "author": infoBook[0].author,
        "year": infoBook[0].year,
        "isbn": infoBook[0].isbn,
        "review_count": infoBook[0].review_count,
        "average_score": infoBook[0].average_score
    })

# Errors
@app.errorhandler(413)
def app_handle_413(e):
    return render_template('error.html', error="File size must not exceed 3 megabytes"), 413

@app.errorhandler(405)
def app_handle_405(e):
    return redirect("/")

@app.errorhandler(404)
def app_handle_404(e):
    return redirect("/")