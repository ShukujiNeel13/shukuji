import os.path
import unittest

import app
app.APP.config['TESTING'] = True


# Steps for Creation of Tests (in TDD manner)
# 1. Create BasicTest class, for most fundamental tests (eg test route index)
# 2. Create DatabaseTest class for tests on database
# 3. Create LogicTest class for tests on the application logic (operations)


# TODO: Any exception or error in test must teardown app context
#  So that the DB is reset (otherwise future tests are affected)
#  Or use the setup and teardown pattern for the test class


class DatabaseTests(unittest.TestCase):

    def test_db_init(self):

        print(f'\nIn {self.__class__.__name__}.test_database_init()...')

        app._db_initialize()

        # region Check DB file exists
        _db_file_exists = os.path.exists(app.DIR_PATH_DB)
        print(f'DB file exists?: {_db_file_exists}')
        self.assertTrue(_db_file_exists, '(DB file not found)')
        # endregion


class UseCaseTests(unittest.TestCase):

    def setUp(self) -> None:
        """
        Runs before every test function in this class

        1. Initializes a new test database

        :return:
        """

        self.app = app.APP.test_client()
        self.db_connection = app._db_initialize()

    def tearDown(self) -> None:
        """
        Runs after every test function in this class

        1. Clear the test database

        :return:
        """

        self.db_connection.execute('DELETE FROM entries;')

    def test_get_entries_none_exist(self):

        print(f'\nIn {self.__class__.__name__}.test_get_entries_none_exist()...')

        response = app.APP.test_client().get('/')
        assert b'No entries in table' in response.data

    def test_create_entry(self):

        print(f'\nIn {self.__class__.__name__}.test_create_entity()...')

        _title_of_test_entry = 'Test Entry 1'
        _text_of_test_entry = 'Random Entry No. 1'

        # region Test Create Entry
        response = app.APP.test_client().post(
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
