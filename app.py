import json
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

from flask_sqlalchemy import SQLAlchemy

DIR_PATH_PROJECT = os.path.dirname(os.path.abspath(__name__))
# print(f'DIR_PATH_PROJECT is: {DIR_PATH_PROJECT}')

DB_NAME = 'shuku-store.db'
DIR_PATH_DB = f'{DIR_PATH_PROJECT}/{DB_NAME}'


APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////{DIR_PATH_DB}'
DB = SQLAlchemy(APP)

SCHEMA_FILENAME = 'schema.sql'
DIR_PATH_SCHEMA_FILE = f'{DIR_PATH_PROJECT}/{SCHEMA_FILENAME}'

# APP.config.from_object(__name__)

# TODO: Next step - Add SQLAlchemy to better manage db.
# TODO: Add the HTML and JS to view the items on web.


# TODO: How to check current number of connections to SQLite DB?

# TODO: every db. operation must be inside try catch to catch the errors


class Entity(DB.Model):

    print('In Class Entity')
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    title = DB.Column(DB.Text, nullable=False)
    text = DB.Column(DB.Text, nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__} {self.title}'


@APP.route('/')
def hello_world():

    return 'Hello World'


@APP.route('/entity/')
def get_entities():
    _request_path = request.path
    print(f'Request received on path: {_request_path}')

    entities = Entity.query.all()

    if entities:
        no_of_entries = len(entities)
        print(f'{no_of_entries} records in table')
        return f'{no_of_entries} records in table'
    else:
        return 'No records in table'


@APP.route('/entity/get', methods=['POST'])
def get_entity():
    _request_path = request.path
    print(f'Request received on path: {_request_path}')

    form_data = request.form
    print('Form data given is:')
    print(form_data)

    entry_id = form_data['entryId']
    print(f'entryId given is: {entry_id}')

    desired_entity = Entity.query.filter_by(id=entry_id).first()

    if desired_entity is None:
        result = {
            'success': False,
            'text': 'This entry does not exist'
        }
    else:
        result = {
            'success': True,
            'text': f'Obtained entry with given id: {entry_id}'
        }

    return jsonify(result)

    # data_return = {
    #     'success': True,
    #     'text': ''
    # }


@APP.route('/entity/add', methods=['POST'])
def add_entity():

    _request_path = request.path
    print(f'Request received on path: {_request_path}')

    # db = get_db()
    # data = request.data
    data = request.form
    # print(f'Request data (Type: {type(data)}) is:')
    # print(data)
    title = data['title']
    print(f'Title is: {title}')
    text = data['text']
    print(f'Text is: {text}')

    entity = Entity(title=title, text=text)
    DB.session.add(entity)
    DB.session.commit()

    result = {
        'success': True,
        'text': f'New entry added (title: {title}, text: {text})'
    }

    return jsonify(result)


# Note: Delete SQL command completes even if no records are deleted
@APP.route('/entity/delete', methods=['POST'])
def delete_entity():

    _request_path = request.path
    print(f'Request received on path: {_request_path}')

    data = request.form
    entry_id = data['entryId']
    print(f'entryId given is: {entry_id}')
    try:
        db = get_db()
        db.execute(f'DELETE FROM Entity WHERE id={entry_id}')
        db.commit()
    except Exception as err:
        _err_type = type(err).__name__
        _err_text = str(err)
        err_info = f'{_err_type} deleting record with id: {entry_id} ({_err_text})'

        result = {
            'success': False,
            'text': err_info
        }
    else:
        result = {
            'success': True,
            'text': f'record deleted'
        }
    return jsonify(result)


def get_db() -> sqlite3.Connection:

    if 'db' not in app_globals:
        app_globals.db = _db_create_connection()

    return app_globals.db


@APP.teardown_appcontext
def close_db(error) -> None:
    """This function executes after each request completed or failed."""

    if error:
        print('\nClosing DB (on Error)...', file=sys.stderr)
        print(f'Type of error is: {type(error)}')
        print(f'Error is: {error}')
    else:
        print('Closing DB...')

    if 'db' in app_globals:
        app_globals.db.close()
        print('DB Connection closed.')


def _db_initialize() -> None:
    """
    Executes script to create desired tables in database

    This must be executed only once during the app lifecycle

    :param db_connection: Connection to the SQL database
    :return:
    """

    print('_db_initialize() called...')

    DB.create_all()

    # db_connection = _db_create_connection()

    # with APP.open_resource(SCHEMA_FILENAME, mode='r'):
    #     ...
    # instead of opening a resource (file),
    # To open the file strictly for reading by the app,
    # and give it relative path (instead of absolute),
    # use the above with APP.open_resource() pattern

    # with open(DIR_PATH_SCHEMA_FILE, mode='r') as f:
    #     db_connection.cursor().executescript(f.read())  # Executes the sql script

    # db_connection.commit()  # Saves the changes
    # db_connection.close()
    # return db_connection


def _db_create_connection() -> sqlite3.Connection:
    """
    Creates a new database connection

    :return:
    """

    _sqlite_connection = sqlite3.connect(DIR_PATH_DB)
    print('DB connection created')
    _sqlite_connection.row_factory = sqlite3.Row
    return _sqlite_connection


# TODO: remove below statement after launch / run scripts are ready.
if __name__ == '__main__':
    _db_initialize()  # WARNING: Call only once during app
    APP.run(debug=True)
