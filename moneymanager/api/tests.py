from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User

class APITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        self.client = APIClient()
        self.client.login(username='test', password='pass')

    def test_accounts_list(self):
        response = self.client.get(reverse('accounts-list'))
        self.assertEqual(response.status_code, 200)