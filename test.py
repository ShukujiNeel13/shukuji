import os.path
import unittest

import app
app.APP.config['TESTING'] = True


# TODO: Any exception or error in test must teardown app context
#  So that the DB is reset (otherwise future tests are affected)
#  Or use the setup and teardown pattern for the test class

# TODO: How to reuse portion of code in multiple tests.

# TODO: Reuse the DB connection inside the test class
class EntityTest(unittest.TestCase):

    def setUp(self) -> None:
        """
        Runs before every test function in this class

        1. Initializes a new test database

        :return:
        """

        self.app = app.APP.test_client()
        app._db_initialize()

    def tearDown(self):

        app.DB.drop_all()

    def test_db_file_exists(self):

        _db_file_exists = os.path.exists(app.DIR_PATH_DB)
        self.assertTrue(_db_file_exists, '(DB file not found)')

    def test_index(self):

        response = self.app.get('/')
        self.assertIn(b'Hello World', response.data)

    # region Tests for generic Entity

    def test_get_entities_none_exist(self):

        response = self.app.get('/entity/')
        assert b'No records in table' in response.data

    def test_add_entity(self, data: dict = None):

        if data is None:
            data = {
                'title': 'Test Entry 1',
                'text': 'Random Entry No. 1'
            }

        response = self.app.post(
            '/entity/add',
            data=data
        )

        response_data = response.json
        self.assertTrue(response_data['success'])

    def test_add_and_delete_entity(self):

        # region Add entity
        entity_data = {
            'title': 'Test Entry 1',
            'text': 'Random Entry No. 1'
        }

        self.app.post(
            '/entity/add',
            data=entity_data
        )
        # endregion

        # region Test delete the entity added
        delete_response = self.app.post(
            '/entity/delete',
            data={'entryId': 1}
        )

        self.assertTrue(delete_response.json['success'])
        # endregion

    def test_get_entity_does_not_exist(self):

        get_response = self.app.post(
            '/entity/get',
            data={'entryId': 1}
        )

        _response_data = get_response.json
        self.assertFalse(_response_data['success'])
        # self.assertEqual('This entry does not exist', _response_data['text'])

    def test_add_and_get_entity(self):

        # region Add entity
        entity_data = {
            'title': 'Test Entry 1',
            'text': 'Random Entry No. 1'
        }

        self.app.post(
            '/entity/add',
            data=entity_data
        )
        # endregion

        # region Test get the entity added
        get_response = self.app.post(
            '/entity/get',
            data={'entryId': 1}
        )

        self.assertTrue(get_response.json['success'])
        # endregion

    def test_add_and_get_entities(self):

        # region Add entity
        entity_data = {
            'title': 'Test Entry 1',
            'text': 'Random Entry No. 1'
        }

        self.app.post(
            '/entity/add',
            data=entity_data
        )
        # endregion

        get_response = self.app.get('/entity/')
        self.assertIn(b'1 records in table', get_response.data)

    # endregion
