import os.path
import unittest

import app


APP_CLIENT = app.APP.test_client()


# Steps for Creation of Tests (in TDD manner)
# 1. Create BasicTest class, for most fundamental tests (eg test route index)
# 2. Create DatabaseTest class for tests on database
# 3. Create LogicTest class for tests on the application logic (operations)


class DatabaseTests(unittest.TestCase):

    def test_db_init(self):

        print(f'\nIn {self.__class__.__name__}.test_database_init()...')

        app._db_initialize()

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


class UseCaseTests(unittest.TestCase):

    def test_create_entry(self):

        print(f'\nIn {self.__class__.__name__}.test_create_entity()...')

        _title_of_test_entry = 'Test Entry 1'
        _text_of_test_entry = 'Random Entry No. 1'

        # region Test Create Entry
        response = APP_CLIENT.post(
            '/add',
            data={
                'title': _title_of_test_entry,
                'text': _text_of_test_entry
            }
        )

        print(f'Response is: {response}')

        response_data = response.json
        self.assertTrue(response_data['success'])
        self.assertEqual(
            response_data['text'],
            f'New entry added (title: {_title_of_test_entry}, text: {_text_of_test_entry})'
        )
        # endregion

        response_get_entries = APP_CLIENT.get('/')

    def test_create_entry_and_get_entries(self):
        pass

    def test_delete_entry_not_exists(self):
        pass

    def test_create_and_delete_entry(self):
        pass

    def test_create_and_get_entry(self):
        pass
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
