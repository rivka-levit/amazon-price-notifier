from unittest import TestCase
from unittest.mock import patch

from app import app


class TestApp(TestCase):
    """Test Flask app."""

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_index_get(self):
        """Test index page get returns index.html"""

        r = self.client.get('/')

        self.assertEqual(r.status_code, 200)
        self.assertIn('Enter the URL:', r.get_data(as_text=True))

    @patch('time.sleep', return_value=None)
    @patch('utils.watcher.AmazonPriceWatcher.watch', return_value=None)
    def test_index_post(self, patched_watch, patched_sleep):
        """Test index page post returns started.html"""

        url = ('https://www.amazon.com/Amazon-Essentials-Womens-Surplice-X-'
               'Large/dp/B097K8N1SC/ref=sr_1_5?_encoding=UTF8&content-id='
               'amzn1.sym.b0c3902d-ae70-4b80-8f54-4d0a3246745a&crid=Y67PJX929'
               'LXO&keywords=Dresses&pd_rd_r=a6e6eb6c-07bf-4ea7-8c0f-dadb492a'
               'ecef&pd_rd_w=B3YIb&pd_rd_wg=rSnk8&pf_rd_p=b0c3902d-ae70-4b80-'
               '8f54-4d0a3246745a&pf_rd_r=S85JJC1JNM45G95A4JYX&qid=1703350904'
               '&refinements=p_36%3A-3000&rnid=2661611011&sprefix=dresses%2'
               'Caps%2C149&sr=8-5&th=1&psc=1')

        r = self.client.post('/', data=dict(product=url), follow_redirects=True)

        self.assertEqual(patched_watch.call_count, 1)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.request.path, '/started')
        self.assertIn('Well done!', r.get_data(as_text=True))

    @patch('time.sleep', return_value=None)
    @patch('utils.watcher.AmazonPriceWatcher.watch', return_value=None)
    def test_index_post_wrong_url_error_page(self, patched_watch, patched_sleep):
        """Test index page post with wrong url returns error.html"""

        url = 'https://www.udemy.com'

        r = self.client.post('/', data=dict(product=url), follow_redirects=True)

        self.assertEqual(patched_watch.call_count, 0)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.request.path, '/error')
