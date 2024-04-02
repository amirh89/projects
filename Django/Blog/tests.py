from django.test import TestCase, SimpleTestCase

# Create your tests here.

# without db
class SimpleTest(SimpleTestCase):
    def test_about_status_code(self):
        resp = self.client.get('/blog/postform')
        self.assertEqual(resp.status_code, 200)
