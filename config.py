import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Connect to the database
DATABASE_URI = os.path.join(basedir, 'database.db')
