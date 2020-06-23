from bs4 import BeautifulSoup
from urllib.request import *
import os, csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Function for get html
def get_html(url):
    req = Request(url)
    html = urlopen(req).read()
    return html

def main():
    # All count parc page
    all_count = 0
    # List for text
    list_text = []
    # List for page not img
    no_img = []

    # Select isbn in db
    allisbn = db.execute("SELECT isbn, id FROM books").fetchall()

    # CREATE table, if not was created
    db.execute("CREATE TABLE if not exists img_text "
               "(id SERIAL PRIMARY KEY, less VARCHAR NOT NULL, "
               "more VARCHAR, img_name VARCHAR, "
               " books_id INTEGER NOT NULL REFERENCES books);")
    db.commit()

    #Проходим циклом
    for a in allisbn:
        dict_text = {}

        # Url for parc
        url = f"https://www.goodreads.com/search?q={a.isbn}&qid="
        # Get html
        html = get_html(url)
        # Get BS4
        soup = BeautifulSoup(html, 'html.parser')
        # Find id
        list = soup.find(id='coverImage')
        # If coverImage == True
        if (list):
            # Get new url (url image)
            src_cover_img = soup.find(id='coverImage')['src']
            # Find id
            list2 = soup.find(id='description')
            # If description == True
            if (list2):
                # Find all "span" (text less, text more)
                list3 = list2.find_all('span')
                # Temp variable for count
                tmp_count = 0
                for tag in list3:
                    # If span > 2
                    if len(list3) > 1:
                        if tmp_count == 0:
                            # One span save in less
                            less = " ".join(tag.text.split())
                            tmp_count += 1
                        else:
                            # Two span save in more
                            more = " ".join(tag.text.split())
                            # Dict isbn, less and more
                            dict_text = {'isbn': a.isbn+'.jpg', 'less' : less, 'more' : more,  "books_id" : a.id}
                            # Append in dict
                            list_text.append(dict_text)
                    else:
                        less = " ".join(tag.text.split())
                        more = None
                        dict_text = {'isbn': a.isbn+'.jpg', 'less': less, 'more': more, "books_id" : a.id}
                        list_text.append(dict_text)
                # Save img
                urlretrieve(src_cover_img, f'img/{a.isbn}.jpg')

                # Insert img name, less and more text in db
                db.execute("INSERT INTO img_text (less, more, img_name, books_id)"
                           "VALUES (:less, :more, :img_name, :books_id)",
                           {"less": dict_text["less"], "more": dict_text["more"], "img_name": dict_text["isbn"], "books_id": dict_text["books_id"]})
                db.commit()
                all_count += 1
        # If no img, save in dict
        dict_no_img_cover = {'isbn': a.isbn, "books_id": a.id}
        no_img.append(dict_no_img_cover)
    # Save file no cover img
    with open("no_cover_img1.csv", 'w', encoding="utf-8") as f:
        fieldnames = ['isbn', 'books_id']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        for d in no_img:
            writer.writerow(d)
    # Save file cover img
    with open("cover_img.csv1", 'w', encoding="utf-8") as fail:
        fieldnames = ['isbn', 'less', 'more', 'books_id']
        writer = csv.DictWriter(fail, fieldnames=fieldnames)
        for d in list_text:
            writer.writerow(d)

main()