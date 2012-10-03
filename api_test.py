import api
import json
import unittest


class ApiTestCase(unittest.TestCase):

    def test_add_should_return_201_status_code(self):
        response = api.add()
        self.assertEqual(201, response.status_code)

    def test_add_should_return_empty_body(self):
        response = api.add()
        self.assertEqual("", response.body)

    def test_bind_should_return_201_status_code(self):
        response = api.bind()
        self.assertEqual(201, response.status_code)

    def test_bind_should_return_elastic_search_host_as_json_in_body(self):
        response = api.bind()
        self.assertDictEqual({"ELASTIC_SEARCH_URL": api.ELASTIC_SEARCH_URL}, json.loads(response.body))

    def test_unbind_should_return_200(self):
        response = api.unbind()
        self.assertEqual(200, response.status_code)

    def test_unbind_body_should_be_empty(self):
        response = api.unbind()
        self.assertEqual("", response.body)


if __name__ == "__main__":
    unittest.main()
