import unittest
import responses
import vcr

from contiamo.resources import *
from contiamo.errors import *


class ErrorTestCase(unittest.TestCase):

  def _make_erroneous_request(self, api_key, api_base, project_id, dashboard_id):
    contiamo_client = Client(api_key, api_base=api_base)
    project = contiamo_client.Project(project_id)
    dashboard = project.Dashboard.retrieve(dashboard_id)

  def test_connection_error(self):
    with self.assertRaises(APIConnectionError):
      self._make_erroneous_request('some_api_key', 'http://xyz.wrong-domain-name.123', '456', '789')

  @vcr.use_cassette('tests/cassettes/test_auth_error.yaml')
  def test_auth_error(self):
    with self.assertRaises(AuthenticationError):
      self._make_erroneous_request('wrong_api_key', 'https://api.contiamo.com', '48590121', '345')

  @responses.activate
  def test_invalid_response(self):
    responses.add(responses.GET, 'https://api.contiamo.com/48590121/dashboards/345',
                  body='{"invalid":"json",', status=200, content_type='application/json')
    with self.assertRaises(ResponseError):
      self._make_erroneous_request('correct_api_key', 'https://api.contiamo.com', '48590121', '345')


if __name__ == '__main__':
  unittest.main()
