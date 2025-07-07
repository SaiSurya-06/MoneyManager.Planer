from django.db import models
from django.contrib.auth.models import User
from transactions.models import Category

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    month = models.DateField(help_text='First day of month, e.g., 2025-07-01')
    limit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.month.strftime('%b %Y')}"