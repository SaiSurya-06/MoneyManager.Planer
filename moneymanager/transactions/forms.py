from django import forms
from .models import (
    Account,
    Transaction,
    Category,
    RecurringTransaction,
    Budget,
    Tag
)

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'account_type', 'balance']

class TransactionForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="Comma-separated tags", widget=forms.TextInput(attrs={'placeholder': 'e.g. food, office, urgent'}))

    class Meta:
        model = Transaction
        fields = ['date', 'description', 'amount', 'transaction_type', 'account', 'category']

class StatementUploadForm(forms.Form):
    file = forms.FileField(label="Upload Statement (PDF/Excel/CSV)")

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class RecurringTransactionForm(forms.ModelForm):
    class Meta:
        model = RecurringTransaction
        fields = ['amount', 'description', 'frequency', 'next_due', 'category', 'account', 'transaction_type']

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
