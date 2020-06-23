import os #(1)

from flask import Flask
from flask_session import Session
from flask_mail import Mail

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Config for flask_mail
app.config.from_pyfile("config.py")
# Mail and session application
mail = Mail(app)
Session(app)

# Set up database
# engine = create_engine(os.getenv("DATABASE_URL")) #(1)
engine = create_engine("postgres://jkjcpacwmyvinj:4df9cc37966da638a050ca35ee5ed723d48cc89ac2980278e55c93f75bb24001@ec2-3-222-30-53.compute-1.amazonaws.com:5432/d99t3klcu7ronr")
db = scoped_session(sessionmaker(bind=engine))

key = "YMxYOwDXMM9F2IBJGrNeA"
goodreads = "https://www.goodreads.com/book/review_counts.json"

from views import *

# # Check for environment variable
# if not os.getenv("DATABASE_URL"): #(1)
#     raise RuntimeError("DATABASE_URL is not set") #(1)

if __name__ == '__name__':
    app.run()