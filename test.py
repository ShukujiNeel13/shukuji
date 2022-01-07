import os.path
import unittest

import app


# Steps for Creation of Tests (in TDD manner)
# 1. Create BasicTest class, for most fundamental tests (eg test route index)
# 2. Create DatabaseTest class for tests on database
# 3. Create LogicTest class for tests on the application logic (operations)


class DatabaseTests(unittest.TestCase):

    def test_db_initializer(self):

        print(f'\nIn {self.__class__.__name__}.test_database_exists()...')

        _db_file_exists = os.path.exists(app.DIR_PATH_DB)
        print(f'DB file exists?: {_db_file_exists}')
        self.assertTrue(_db_file_exists, '(DB file not found)')

    def test_empty_db(self):

        print(f'\n In {self.__class__.__name__}.test_empty_db()...')

        test_app_client = app.APP.test_client()
        response = test_app_client.get('/')
        response_data = response.data
        assert b'No entries in table' in response_data
        print(f'Response data is: {response_data}')


class LogicTest(unittest.TestCase):

    def test_create_entry(self):
        ...

    def test_get_entries_none_exist(self):
        ...

    def test_create_entry_and_get_entries(self):
        ...

    def test_delete_entry_not_exists(self):
        ...

    def test_create_and_delete_entry(self):
        ...

    def test_create_and_get_entry(self):
        ...
#
#     def test_login(self, username: str, password: str):
#
#         test_app_client = app.APP.test_client()
#
#         _data = {
#             'username': username,
#             'password': password
#         }
#
#         return test_app_client.post(
#             '/login',
#             data=_data,
#             follow_redirects=True
#         )
#
#     def test_logout(self):
#
#         test_app_client = app.APP.test_client()
#
#         return test_app_client.get(
#             '/logout', follow_redirects=True
#         )
#
#     def test_incorrect_login(self):
#         ...
#
