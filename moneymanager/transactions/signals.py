# transactions/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Transaction, Account
from django.db.models import Sum

def update_account_balance(account):
    income_total = account.transaction_set.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    expense_total = account.transaction_set.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    account.balance = income_total - expense_total
    account.save()

@receiver(post_save, sender=Transaction)
def on_transaction_save(sender, instance, **kwargs):
    update_account_balance(instance.account)

@receiver(post_delete, sender=Transaction)
def on_transaction_delete(sender, instance, **kwargs):
    update_account_balance(instance.account)
