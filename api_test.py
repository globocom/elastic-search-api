import api
import json
import os
import unittest
import responses
from webtest import TestApp


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = TestApp(api.app)
        self.app.authorization = ('Basic', ('admin', 'password'))

    def test_should_have_ELASTICSEARCH_HOST_defined(self):
        self.assertIsNotNone(api.ELASTICSEARCH_HOST)

    def test_ELASTIC_SEARCH_HOST_should_be_filled_by_environ_var(self):
        IP = "192.169.56.2"

        os.environ["ELASTICSEARCH_HOST"] = IP
        reload(api)
        self.assertEqual(IP, api.ELASTICSEARCH_HOST)

    def test_add_should_return_empty_body(self):
        self.assertEqual(201, self.app.post("/resources").status_code )

    def test_bind_should_return_elasticsearch_host_as_json_in_body(self):
        self.assertDictEqual({"ELASTICSEARCH_HOST": api.ELASTICSEARCH_HOST,
                                "ELASTICSEARCH_PORT": "9200"},
                             json.loads(self.app.post("/resources/example_app/bind-app").body))

    def test_unbind_body_should_be_empty(self):
        self.assertEqual( ("", 200), api.unbind("test"))



class ApiRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(api.app)
        self.app.authorization = ('Basic', ('admin', 'password'))

    def test_should_return_a_list_of_plans(self):
        response = self.app.get("/resources/plans")
        self.assertEqual(200, response.status_code)

    def test_should_post_to_add_and_get_a_201(self):
        response = self.app.post("/resources")
        self.assertEqual(201, response.status_code)

    def test_should_post_to_bind_passing_a_name_and_receive_201(self):
        response = self.app.post("/resources/myappservice/bind")
        self.assertEqual(201, response.status_code)

    def test_should_delete_to_unbind_and_receive_200(self):
        response = self.app.delete("/resources/myappservice")
        self.assertEqual(200, response.status_code)

    @responses.activate
    def test_status_OK(self):
        HOST = "1.2.3.4"
        os.environ["ELASTICSEARCH_HOST"] = HOST
        reload(api)

        elasticsearch_healthy = '''
{
  "status" : 200,
  "name" : "Briquette",
  "cluster_name" : "elasticsearch",
  "version" : {
    "number" : "1.6.0",
    "build_hash" : "cdd3ac4dde4f69524ec0a14de3828cb95bbb86d0",
    "build_timestamp" : "2015-06-09T13:36:34Z",
    "build_snapshot" : false,
    "lucene_version" : "4.10.4"
  },
  "tagline" : "You Know, for Search"
}
        '''

        responses.add(responses.GET, 'http://1.2.3.4:9200/',
                  body=elasticsearch_healthy, status=200,
                  content_type='application/json')

        response = self.app.get("/resources/myappservice/status")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(204, response.status_code)

    @responses.activate
    def test_status_error(self):
        HOST = "1.2.3.4"
        os.environ["ELASTICSEARCH_HOST"] = HOST
        reload(api)

        responses.add(responses.GET, 'http://1.2.3.4:9200/',
                  body='broken', status=404,
                  content_type='application/json')

        response = self.app.get("/resources/myappservice/status", status = 500)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(500, response.status_code)


if __name__ == "__main__":
    unittest.main()
