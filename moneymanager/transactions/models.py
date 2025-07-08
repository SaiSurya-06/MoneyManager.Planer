from django.db import models
from django.contrib.auth.models import User

# --- ACCOUNT MODEL ---
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

# --- CATEGORY MODEL ---
class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    is_custom = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# --- TRANSACTION MODEL ---
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
        return f"{self.date} {self.description} ₹{self.amount}"

    def tag_list(self):
        return ', '.join(tag.tag.name for tag in self.transactiontag_set.all())

# --- TAG MODEL ---
class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# --- TAG RELATIONSHIP ---
class TransactionTag(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.transaction.description} - {self.tag.name}"

# --- RECURRING TRANSACTIONS ---
class RecurringTransaction(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    next_due = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=Transaction.TRANSACTION_TYPE)

    def __str__(self):
        return f"{self.description} ({self.frequency})"

# --- BUDGET MODEL (with related_name to avoid conflicts) ---
# class Budget(models.Model):`
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_budgets')
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='transaction_budgets')
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
#     month = models.DateField()  # Represented as the first day of the month

#     def __str__(self):
#         return f"{self.user.username} - {self.category.name} - {self.month.strftime('%B %Y')}"`