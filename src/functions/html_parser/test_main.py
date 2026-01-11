import main
import unittest
from unittest.mock import Mock, patch

class TestParseJobPosting(unittest.TestCase):
    @patch('main.requests.get')
    def test_parse_job_posting_success(self, mock_get):
        # Mock successful HTML response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'<html><head><title>Test Job</title></head><body><script>var x=1;</script><p>Job Description Here.</p></body></html>'
        mock_get.return_value = mock_response

        # Request
        data = {'url': 'http://example.com/job'}
        req = Mock(get_json=Mock(return_value=data), args=data)

        # Execute
        res, status_code = main.parse_job_posting(req)

        # Verify
        self.assertEqual(status_code, 200)
        self.assertEqual(res['title'], 'Test Job')
        self.assertEqual(res['text'], 'Job Description Here.')
        self.assertNotIn('var x=1', res['text']) # Script should be removed

    @patch('main.requests.get')
    def test_parse_job_posting_fetch_error(self, mock_get):
        # Mock request exception
        mock_get.side_effect = main.requests.exceptions.RequestException("Connection refused")

        req = Mock(get_json=Mock(return_value={'url': 'http://bad-url.com'}), args={})
        
        res, status_code = main.parse_job_posting(req)
        
        self.assertEqual(status_code, 500)
        self.assertIn('Failed to fetch URL', res['error'])

    def test_parse_job_posting_no_url(self):
        req = Mock(get_json=Mock(return_value={}), args={})
        
        res, status_code = main.parse_job_posting(req)
        
        self.assertEqual(status_code, 400)
        self.assertEqual(res['error'], 'Please provide a URL parameter')

if __name__ == '__main__':
    unittest.main()
