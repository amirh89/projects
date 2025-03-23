from django.test import TestCase

# Create your tests here.

class Test(TestCase):
    def test_status_code(self):
        res = self.client.get('/hobby/objects/')
        self.assertEqual(res.status_code, 200)
