from django.contrib import admin
from .models import Account, Category, Transaction, RecurringTransaction, Tag, TransactionTag

admin.site.register(Account)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(RecurringTransaction)
admin.site.register(Tag)
admin.site.register(TransactionTag)