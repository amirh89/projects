from django.test import TestCase, SimpleTestCase
from .models import Ticket
from django.urls import reverse_lazy, reverse

# Create your tests here.

# without db
class SimpleTest(SimpleTestCase):
    def test_status_code(self):
        response = self.client.get('/blog/profile/')
        self.assertEqual(response.status_code, 200)

    def test_about_status_code(self):
        resp = self.client.get('/blog/postform')
        self.assertEqual(resp.status_code, 200)

# with db
class TicketModelTest(TestCase):
    def setUp(self):
        Ticket.objects.create(name='hi')

    def test_text_content(self):
        post = Ticket.objects.get(id=1)
        excepted_object_name = f'{post.name}'
        self.assertEqual(excepted_object_name,'hi')

class HomePageViewTest(TestCase):
    def setUp(self):
        Ticket.objects.create(message='another test')
    
    def test_view_url_location(self):
        response = self.client.get('/blog/ticket')
        self.assertEqual(response.status_code, 200)

    def test_view_url_name(self):
        path = reverse_lazy('ticket')
