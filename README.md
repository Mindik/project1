# Project 1
Web Programming with Python and JavaScript
---

Project completed in [CS50W](https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript) course.
Used Goodreads [API](https://www.goodreads.com/api) and [Heroku](https://www.heroku.com/postgres) PostgreSQL database.


The project was implemented in [PyCharm](https://www.jetbrains.com/pycharm/) 2020.1.2 (Professional Edition).
Applied technology [Flask](https://flask.palletsprojects.com/en/1.1.x/), 
[Jinja2](https://jinja.palletsprojects.com/en/2.11.x/), [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript), 
[HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5), [CSS3](https://www.w3schools.com/css/).

The task can be viewed at the link - [Project 1: Books](https://docs.cs50.net/web/2020/x/projects/1/project1.html).


The task sounds like this:
>«In this project, you’ll build a book review website. Users will be able to register for your website and 
><br>then log in using their username and password. Once they log in, they will be able to search for books, 
><br>leave reviews for individual books, and see the reviews made by other people. You’ll also use the a third-party 
><br>API by Goodreads, another book review website, to pull in ratings from a broader audience. Finally, 
><br>users will be able to query for book details and book reviews programmatically via your website’s API.»

Data for connecting to the database is specified in the application.py file. The 10,000 rows Heroku provided for free 
<br>was not enough for me, so I temporarily bought the next database plan (10,000,000 rows), which costs $ 9 per month. 
<br>After checking my project, I will not pay for the database, so it may not work. In addition, Heroku periodically 
<br>changes connection data when using its first tariffs, so the database may stop working before I cancel my
 subscription.

The server is temporarily deployed on [AWS EB](http://project1-env.eba-4pwgu3zp.us-east-2.elasticbeanstalk.com/)

Importing the source data about books from the books.csv table was done by a program that is written in Python in the import.py file. 
<br>(Additionally downloaded 5000 (!) Images and texts for each book ([parc_img_text.py](parc_img_text.py)).

## Sign up
![Sign up](https://i.ibb.co/mqkGgrv/register.png)

To use the functions of the site you need to register, indicating the name, surname, email address and password. 
<br>Using [Bootstrap 4](https://getbootstrap.com/docs/4.5/components/forms/#validation) validation.

![Validation](https://i.ibb.co/f4k29yX/register-valid.png)

Additionally, the function of checking the coincidence of passwords and viewing the entered passwords is implemented.

![Password check and view](https://i.ibb.co/mXBbJw4/register-pass.png)

After entering the data and submitting the form, the server will process the request, 
<br>enter the new data into the database and send an email with a link to confirm the mailbox.

![Send email](https://i.ibb.co/N2XC35v/register-send-email.png)

![Activate](https://i.ibb.co/6bzWmSP/05register-email.png)

If the specified mailbox address is already in use, you will see a message about this.

![Error](https://i.ibb.co/Q9Cqy2h/04-1-reg-error-email.png)


####ATTENTION! The mailbox name is not case sensitive (MyEMail@exaMPLe.com == myemail@example.com), unlike the rest of the fields.

If the user tries to enter the site without confirming the mailbox, the application will not allow this, and the sign in form will offer to re-send the letter.

![Resend](https://i.ibb.co/4fx3FFg/08resend-email.png)

On the page for re-sending the letter, you need to specify your mailing address. If you specify a mailbox that 
<br>is not in the database or it has already been verified, you will receive an error message.

![Resend form](https://i.ibb.co/hKHY3Pn/10resend-error.png)

Otherwise, you will receive a letter to the specified mailbox, in which there will be a link with a GET request.

![Resend mail](https://i.ibb.co/r4RTjhC/12resend-get.png)

![GET](https://i.ibb.co/MSnb9Ft/06reg-validation-get.png)

After clicking on the link from the letter, you will automatically activate your account.

![Reg fine](https://i.ibb.co/0BWCm6q/07reg-fine.png)

## Sign in

After activation, you can log in with your account.

![Sign in](https://i.ibb.co/pLF0r3z/14fg.png)

Forgot your password? Do not despair! It can be reset! How? Again through your mailing address.

![Forgot password](https://i.ibb.co/BKJQMFJ/15fg-reset.png)

You need to go to the forgot password link and specify the address of your mailbox. If such an address exists, then 
<br>a letter will be sent to you, and on the screen you will see a message

![Ok reset](https://i.ibb.co/WfLWW3Q/16fg-ok-send-email.png)

In case of an error, the message will be different!

![Error reset password](https://i.ibb.co/LtDb0VQ/Screenshot-1.png)

After clicking on the link from the letter, you will see a form that will allow you to change your password.
When you submit a login form, if you provide an incorrect username or password, you will receive a message about this. 
<br>Otherwise, you will be taken to the main page of the site.

![Sign in form](https://i.ibb.co/tJ213H1/22sign-in-error.png)