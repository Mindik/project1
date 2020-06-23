import os, csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#CREATE table, if not was created
db.execute("CREATE TABLE if not exists books "
           "(id SERIAL PRIMARY KEY, isbn VARCHAR NOT NULL, "
           "title VARCHAR NOT NULL, author VARCHAR NOT NULL, year INTEGER NOT NULL);")
db.commit()

# Open file for read
with open("books.csv", "r") as f:
    reader = csv.DictReader(f)
    for a in reader:
        # Insert in db
        db.execute("INSERT INTO books (isbn, title, author, year)"
                   "VALUES (:isbn, :title, :author, :year)",
                   {"isbn" : a["isbn"], "title" : a["title"], "author" : a["author"], "year" : a["year"]})
db.commit()