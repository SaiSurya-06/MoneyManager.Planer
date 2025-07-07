from django.db import models
from django.contrib.auth.models import User

class Holding(models.Model):
    ASSET_TYPE_CHOICES = [
        ("stock", "Stock"),
        ("mf", "Mutual Fund"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset_type = models.CharField(max_length=10, choices=ASSET_TYPE_CHOICES)
    symbol = models.CharField(max_length=20, help_text="Ticker symbol or MF code")
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    avg_price = models.DecimalField(max_digits=12, decimal_places=2)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"

    @property
    def invested(self):
        return self.quantity * self.avg_price