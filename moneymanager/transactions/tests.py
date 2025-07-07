from django.test import TestCase
from django.contrib.auth.models import User
from .models import Account, Category, Transaction
from django.urls import reverse

class TransactionsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        self.account = Account.objects.create(user=self.user, name='Bank', account_type='bank', balance=1000)
        self.category = Category.objects.create(user=self.user, name='Food')

    def test_account_creation(self):
        self.assertEqual(Account.objects.count(), 1)

    def test_transaction_creation(self):
        txn = Transaction.objects.create(
            user=self.user, date='2025-01-01', description='Lunch',
            amount=100, transaction_type='expense', account=self.account, category=self.category
        )
        self.assertEqual(Transaction.objects.count(), 1)