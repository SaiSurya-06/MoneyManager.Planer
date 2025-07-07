from django import forms
from .models import Holding

class HoldingForm(forms.ModelForm):
    class Meta:
        model = Holding
        fields = ['asset_type', 'symbol', 'name', 'quantity', 'avg_price']