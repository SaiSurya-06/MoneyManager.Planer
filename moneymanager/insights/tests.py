from django.test import TestCase
from django.contrib.auth.models import User
from transactions.models import Account, Category, Transaction
from .services import get_savings_tip

class InsightsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        self.account = Account.objects.create(user=self.user, name='Bank', account_type='bank', balance=1000)
        self.category = Category.objects.create(user=self.user, name='Food')
        Transaction.objects.create(
            user=self.user, date='2025-01-01', description='Lunch',
            amount=100, transaction_type='expense', account=self.account, category=self.category
        )

    def test_savings_tip(self):
        tip = get_savings_tip(self.user)
        self.assertIn('Food', tip)