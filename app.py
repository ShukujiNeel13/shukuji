import os
import sys
import sqlite3
from pprint import pformat

from flask import (
    Flask,
    request,
    jsonify,
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

# TODO: Next step - Add SQLAlchemy to better manage db.
# TODO: Add the HTML and JS to view the items on web.


# TODO: How to check current number of connections to SQLite DB?


@APP.route('/')
def get_entries():
    print('Request received on index')

    db = get_db()
    cursor = db.execute('SELECT * FROM entries ORDER BY id DESC')
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


@APP.route('/get', methods=['POST'])
def get_entry():
    ...


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
        'INSERT INTO entries (title, text) VALUES (?, ?)',
        [title, text]
    )
    db.commit()

    result = {
        'success': True,
        'text': f'New entry added (title: {title}, text: {text})'
    }

    return jsonify(result)


@APP.route('/delete', methods=['POST'])
def delete_entry():
    data = request.form
    entry_id = data['entryId']
    print(f'entryId given is: {entry_id}')
    try:
        db = get_db()
        db.execute(f'DELETE FROM entries WHERE id={entry_id}')
        db.commit()
    except Exception as err:
        _err_type = type(err).__name__
        _err_text = str(err)
        err_info = f'{_err_type} deleting entry ID: {entry_id} ({_err_text})'

        result = {
            'success': False,
            'text': err_info
        }
    else:
        result = {
            'success': True,
            'text': f'Entry: {entry_id} deleted'
        }
    return jsonify(result)


def get_db() -> sqlite3.Connection:

    if 'db' not in app_globals:
        app_globals.db = _db_create_connection()

    return app_globals.db


@APP.teardown_appcontext
def close_db(error) -> None:

    if error:
        print('\nClosing DB (on Error)...', file=sys.stderr)
        print(f'Type of error is: {type(error)}')
        print(f'Error is: {error}')
    else:
        print('Closing DB...')

    if 'db' in app_globals:
        app_globals.db.close()
        print('DB Connection closed.')


def _db_initialize() -> sqlite3.Connection:
    """
    Create and initialize database (within app context)

    :return:
    """

    print('_db_initialize() called...')

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
    return db


def _db_create_connection() -> sqlite3.Connection:
    """
    Creates a new database connection

    :return:
    """

    _sqlite_connection = sqlite3.connect(DIR_PATH_DB)
    print('DB connection created')
    _sqlite_connection.row_factory = sqlite3.Row
    return _sqlite_connection


if __name__ == '__main__':
    _db_initialize()
    APP.run(debug=True)
