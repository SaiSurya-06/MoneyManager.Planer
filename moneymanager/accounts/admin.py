from django.contrib import admin
from .models import Profile, PartnerAccount

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')

@admin.register(PartnerAccount)
class PartnerAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'partner', 'can_edit', 'created_at')
    list_filter = ('can_edit',)