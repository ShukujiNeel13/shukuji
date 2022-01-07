import os.path
import unittest

import app


# Steps for Creation of Tests (in TDD manner)
# 1. Create BasicTest class, for most fundamental tests (eg test route index)
# 2. Create DatabaseTest class for tests on database
# 3. Create LogicTest class for tests on the application logic (operations)


class DatabaseTest(unittest.TestCase):

    def test_db_initializer(self):

        db = app.get_db()

        print(f'\nIn {self.__class__.__name__}.test_database_exists()...')

        _db_file_exists = os.path.exists(app.DIR_PATH_DB)
        print(f'DB file exists?: {_db_file_exists}')
        self.assertTrue(_db_file_exists, '(DB file not found)')


# class LogicTest(unittest.TestCase):
#
#     # TO BE UPDATED WITH ACTUAL Response to INDEX
#     def test_index(self):
#
#         test_app_client = app.APP.test_client()
#
#         response = test_app_client.get('/', content_type="html/text")
#         assert response.status_code == 200
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
#     def test_create_entry(self):
#         ...
#
#     def test_get_entry(self):
#         ...
#
#     def test_delete_entry(self):
#         ...
