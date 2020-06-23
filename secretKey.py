# Generate SECRET_KEY for Flask
# https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY
import os

print(os.urandom(24))