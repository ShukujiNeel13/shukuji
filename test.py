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


class UseCaseTests(unittest.TestCase):

    def setUp(self) -> None:
        """
        Runs before every test function in this class

        1. Initializes a new test database

        :return:
        """

        print('\nIn setUp()...')

        self.app = app.APP.test_client()
        # self.db_connection = app.get_db()
        app._db_initialize()
        # This Creates the desired tables (if not already)

    # def tearDown(self) -> None:
    #     """
    #     Runs after every test function in this class
    #
    #     1. Clear the test database
    #
    #     :return:
    #     """
    #
    #     print('\nIn tearDown()...')
    #     self.db_connection.execute('DROP TABLE IF EXISTS entries;')
    #     self.db_connection.commit()
    #     print('Entries Table dropped')

    def test_db_file_exists(self):

        _db_file_exists = os.path.exists(app.DIR_PATH_DB)
        print(f'DB file exists?: {_db_file_exists}')
        self.assertTrue(_db_file_exists, '(DB file not found)')

    def test_get_entries_none_exist(self):

        print(f'\nIn {self.__class__.__name__}.test_get_entries_none_exist()...')

        response = self.app.get('/')
        print('response data is:')
        print(response.data)
        assert b'No entries in table' in response.data

    def test_create_and_delete_entry(self):
        print(f'\nIn {self.__class__.__name__}.create_and_delete_entry()...')

        _title_of_test_entry = 'Test Entry 1'
        _text_of_test_entry = 'Random Entry No. 1'

        # region Test Create Entry
        response = self.app.post(
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

        print('Testing Delete ...')
        delete_response = self.app.post(
            '/delete',
            data={'entryId': 1}
        )

        print(f'Delete response is:\n{delete_response.json}')

        self.assertTrue(delete_response.json['success'])

    def test_create_and_get_entry(self):
        print(f'\nIn {self.__class__.__name__}.create_and_delete_entry()...')

        _title_of_test_entry = 'Test Entry 1'
        _text_of_test_entry = 'Random Entry No. 1'

        # region Test Create Entry
        response = self.app.post(
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

        print('Testing Get ...')
        get_response = self.app.post(
            '/get',
            data={'entryId': 1}
        )

        print(f'get response is:\n{get_response.json}')

        self.assertTrue(get_response.json['success'])


    # def test_get_entry_does_not_exist(self):
    #
    #     random_entry_id = 'randomEntryId'
    #     response = self.app.post(
    #         '/get',
    #         data={'entryId': random_entry_id}
    #     )
    #
    #     _response_data = response.data
    #     print(f'Response data is: {_response_data}')
    #     assert b'Entry does not exist' in _response_data

    # def test_create_entry_and_get_entry(self):
    #
    #     print(f'\nIn {self.__class__.__name__}.test_create_entity()...')
    #
    #     _title_of_test_entry = 'Test Entry 1'
    #     _text_of_test_entry = 'Random Entry No. 1'
    #
    #     # region Test Create Entry
    #     response = self.app.post(
    #         '/add',
    #         data={
    #             'title': _title_of_test_entry,
    #             'text': _text_of_test_entry
    #         }
    #     )
    #
    #     print(f'Response is: {response}')
    #
    #     response_data = response.json
    #     self.assertTrue(response_data['success'])
    #     self.assertEqual(
    #         response_data['text'],
    #         f'New entry added (title: {_title_of_test_entry}, text: {_text_of_test_entry})'
    #     )
    #     # endregion
    #
    # def test_create_entry_and_get_entries(self):
    #     pass

    #
    # def test_delete_entry_not_exists(self):
    #     pass
    #
    # def test_create_and_delete_entry(self):
    #     pass
    #
    # def test_create_and_get_entry(self):
    #     pass

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
