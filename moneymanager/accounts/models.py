from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"

class PartnerAccount(models.Model):
    user = models.ForeignKey(User, related_name='partner_user', on_delete=models.CASCADE)
    partner = models.ForeignKey(User, related_name='partner_partner', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    can_edit = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'partner')

    def __str__(self):
        return f"{self.user.username} ↔ {self.partner.username}"