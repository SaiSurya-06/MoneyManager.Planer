from django import forms
from .models import Budget

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'month', 'limit']
        widgets = {
            'month': forms.DateInput(attrs={'type': 'date'}),
        }