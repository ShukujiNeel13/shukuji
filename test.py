import os.path
import unittest

import app


# Steps for Creation of Tests (in TDD manner)
# 1. Create BasicTest class, for most fundamental tests (eg test route index)
# 2. Create DatabaseTest class for tests on database
# 3. Create LogicTest class for tests on the application logic (operations)


class BasicTest(unittest.TestCase):

    def test_hello_world(self):
        print(f'\nIn {self.__class__.__name__}.test_hello_world()')
        test_app_client = app.APP.test_client()

        response = test_app_client.get('/')
        _response_status_code = response.status_code
        _status_text = f'Request index (/) returned status code: {_response_status_code}'
        print(_status_text)

        if response.data:
            print(f'"data" in response is is: {response.data}')

        self.assertEqual(response.status_code, 200, (_status_text))


class DatabaseTest(unittest.TestCase):

    def test_db_initializer(self):

        db = app.initialize_db()

        print(f'\nIn {self.__class__.__name__}.test_database_exists()...')

        _db_file_exists = os.path.exists(app.DIR_PATH_DB)
        print(f'DB file exists?: {_db_file_exists}')
        self.assertTrue(_db_file_exists, '(DB file not found)')

        app.close_db(db)


class LogicTest(unittest.TestCase):

    def test_login(self):
        ...

    def test_logout(self):
        ...

    def test_create_entry(self):
        ...

    def test_get_entry(self):
        ...

    def test_delete_entry(self):
        ...
