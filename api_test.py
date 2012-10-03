import api
import json
import unittest
from webtest import TestApp


class ApiTestCase(unittest.TestCase):

    def test_add_should_return_empty_body(self):
        self.assertEqual("", api.add())

    def test_bind_should_return_elastic_search_host_as_json_in_body(self):
        self.assertDictEqual({"ELASTIC_SEARCH_URL": api.ELASTIC_SEARCH_URL},
                             json.loads(api.bind("test")))

    def test_unbind_body_should_be_empty(self):
        self.assertEqual("", api.unbind("test"))


class ApiRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(api.app)

    def test_should_post_to_add_and_get_a_201(self):
        response = self.app.post("/resources")
        self.assertEqual(201, response.status_code)

    def test_should_post_to_bind_passing_a_name_and_receive_201(self):
        response = self.app.post("/resources/myappservice")
        self.assertEqual(201, response.status_code)

    def test_should_delete_to_unbind_and_receive_200(self):
        response = self.app.delete("/resources/myappservice")
        self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    unittest.main()
