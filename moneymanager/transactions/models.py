from django.db import models
from django.contrib.auth.models import User
<<<<<<< HEAD
from accounts.models import CustomUser
# --- ACCOUNT MODEL ---
=======

>>>>>>> parent of bbb7610 (update 2)
class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('bank', 'Bank'),
        ('cash', 'Cash'),
        ('card', 'Card'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name} ({self.account_type})"

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    is_custom = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.date} {self.description} {self.amount}"
