from django import forms
from .models import Account, Transaction, Category

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'account_type', 'balance']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'description', 'amount', 'transaction_type', 'account', 'category']

class StatementUploadForm(forms.Form):
    file = forms.FileField(label="Upload Statement (PDF/Excel/CSV)")

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']