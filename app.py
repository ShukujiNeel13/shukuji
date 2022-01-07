import os
import sqlite3
from pprint import pformat

from flask import (
    Flask,
    request,
    g as app_globals
)

APP = Flask(__name__)


DIR_PATH_PROJECT = os.path.dirname(os.path.abspath(__name__))
print(f'DIR_PATH_PROJECT is: {DIR_PATH_PROJECT}')

DB_NAME = 'shuku-store.db'
DIR_PATH_DB = f'{DIR_PATH_PROJECT}/{DB_NAME}'

SCHEMA_FILENAME = 'schema.sql'
DIR_PATH_SCHEMA_FILE = f'{DIR_PATH_PROJECT}/{SCHEMA_FILENAME}'

APP.config.from_object(__name__)

# App Dev Steps (After creation of respective tests, for TDD manner)
# 1. Create Route for Index
# 2. Database functions (steps)
#   2.1. Create the DB
#     2.1.1. Get the DB connection
#       2.1.1.1. Connect to DB
#     2.1.2. Save the DB connection for re-use by the application
#   2.2. Close the DB (connection) - when app needs to close.
# 3. Create routes to perform desired operations.
# 4. Update the index route to more specific version (if desired)

# TODO: How to check current number of connections to SQLite DB?


@APP.route('/')
def get_entries():
    print('Request received on index')

    db = get_db()
    cursor = db.execute('select * from entries order by id desc')
    print('Obtained items from table')
    entries = cursor.fetchall()
    # print(f'Type of items from table is: {type(entries)}')
    print(pformat(entries))  # a list of entries

    if entries:
        no_of_entries = len(entries)
        print(f'{no_of_entries} entries in table: entries')
        return f'{no_of_entries} entries in table: entries'
    else:
        return 'No entries in table'


@APP.route('/add', methods=['POST'])
def add_entry():
    db = get_db()
    # data = request.data
    data = request.form
    # print(f'Request data (Type: {type(data)}) is:')
    # print(data)
    title = data['title']
    print(f'Title is: {title}')
    text = data['text']
    print(f'Text is: {text}')
    db.execute(
        'insert into entries (title, text) values (?, ?)',
        [title, text]
    )
    db.commit()
    return f'New entry added (title: {title}, text: {text})'


def get_db() -> sqlite3.Connection:

    if 'db' not in app_globals:
        app_globals.db = _db_create_connection()

    return app_globals.db


@APP.teardown_appcontext
def close_db(error) -> None:

    if error:
        print('Closing DB (on Error)...')
        print(f'Type of error is: {type(error)}')
        print(f'Error is: {error}')
    else:
        print('Closing DB...')

    if 'db' in app_globals:
        app_globals.db.close()
        print('DB Connection closed.')


def _db_initialize() -> None:
    """
    Create and initialize database (within app context)

    :return:
    """

    db = _db_create_connection()

    # with APP.open_resource(SCHEMA_FILENAME, mode='r'):
    #     ...
    # instead of opening a resource (file),
    # To open the file strictly for reading by the app,
    # and give it relative path (instead of absolute),
    # use the above with APP.open_resource() pattern

    with open(DIR_PATH_SCHEMA_FILE, mode='r') as f:
        db.cursor().executescript(f.read())  # Executes the sql script

    db.commit()  # Saves the changes


def _db_create_connection() -> sqlite3.Connection:
    """
    Creates a new database connection

    :return:
    """

    _sqlite_connection = sqlite3.connect(DIR_PATH_DB)
    _sqlite_connection.row_factory = sqlite3.Row
    return _sqlite_connection


if __name__ == '__main__':
    # _db_initialize()
    APP.run(debug=True)
