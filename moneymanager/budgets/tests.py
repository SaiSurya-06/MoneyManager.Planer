from django.test import TestCase
from django.contrib.auth.models import User
from transactions.models import Category
from .models import Budget

class BudgetsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        self.category = Category.objects.create(user=self.user, name='Food')

    def test_budget_creation(self):
        budget = Budget.objects.create(user=self.user, category=self.category, month='2025-07-01', limit=5000)
        self.assertEqual(Budget.objects.count(), 1)