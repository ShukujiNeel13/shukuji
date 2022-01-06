import os
import sqlite3
from flask import Flask

APP = Flask(__name__)


DIR_PATH_PROJECT = os.path.dirname(os.path.abspath(__name__))
print(f'DIR_PATH_PROJECT is: {DIR_PATH_PROJECT}')

DB_NAME = 'shuku-store'
DIR_PATH_DB = f'{DIR_PATH_PROJECT}/{DB_NAME}'

APP.config.from_object(__name__)

# App Dev Steps (After creation of respective tests, for TDD manner)
# 1. Create Route for Index
# 2. Database functions (steps)
#   2.1. Create the DB
#     2.1.1. Get the DB connection
#       2.1.1.1. Connect to DB
#   2.2. Close the DB (connection)


@APP.route('/')
def hello_world():  # put application's code here
    # By default return type is: "text/html" (if returning string)
    return 'Hello World!'
    # print('hello')


def initialize_db() -> sqlite3.Connection:
    """
    Creates a database and initializes it

    :return:
    """

    db = _db_create_connection()

    with open('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())

    db.commit()  # Saves the changes
    return db


def close_db(db: sqlite3.Connection):
    # db = _db_create_connection()
    db.close()


def _db_create_connection() -> sqlite3.Connection:
    """
    Creates a new database connection

    :return:
    """

    _sqlite_connection = sqlite3.connect(DIR_PATH_DB)
    _sqlite_connection.row_factory = sqlite3.Row
    return _sqlite_connection


if __name__ == '__main__':
    close_db()
    # APP.run()
