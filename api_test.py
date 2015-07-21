import api
import json
import os
import unittest
from webtest import TestApp


class ApiTestCase(unittest.TestCase):

    def test_should_have_ELASTIC_SEARCH_IP_defined(self):
        self.assertIsNotNone(api.ELASTIC_SEARCH_IP)

    def test_ELASTIC_SEARCH_HOST_should_be_filled_by_environ_var(self):
        IP = "192.169.56.2"

        os.environ["ELASTIC_SEARCH_IP"] = IP
        reload(api)
        self.assertEqual(IP, api.ELASTIC_SEARCH_IP)

    def test_add_should_return_empty_body(self):
        self.assertEqual(("", 201), api.add_instance())

    def test_bind_should_return_elasticsearch_host_as_json_in_body(self):
        self.assertDictEqual({"ELASTICSEARCH_HOST": api.ELASTIC_SEARCH_IP,
                                "ELASTICSEARCH_PORT": "9200"},
                             json.loads(api.bind_app("test")[0]) )

    def test_unbind_body_should_be_empty(self):

        self.assertEqual( ("", 200), api.unbind("test"))



class ApiRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(api.app)

    def test_should_post_to_add_and_get_a_201(self):
        response = self.app.post("/resources")
        self.assertEqual(201, response.status_code)

    def test_should_post_to_bind_passing_a_name_and_receive_201(self):
        response = self.app.post("/resources/myappservice/bind")
        self.assertEqual(201, response.status_code)

    def test_should_delete_to_unbind_and_receive_200(self):
        response = self.app.delete("/resources/myappservice")
        self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    unittest.main()
