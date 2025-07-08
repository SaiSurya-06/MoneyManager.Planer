from celery import shared_task
from django.utils.timezone import now
from .models import RecurringTransaction, Transaction

@shared_task
def process_recurring_transactions():
    today = now().date()
    for rt in RecurringTransaction.objects.filter(next_due__lte=today):
        Transaction.objects.create(
            user=rt.user,
            date=today,
            description=rt.description,
            amount=rt.amount,
            transaction_type=rt.transaction_type,
            account=rt.account,
            category=rt.category
        )
        # Update next due
        if rt.frequency == 'monthly':
            rt.next_due = today + relativedelta(months=1)
        elif rt.frequency == 'weekly':
            rt.next_due = today + relativedelta(weeks=1)
        elif rt.frequency == 'daily':
            rt.next_due = today + relativedelta(days=1)
        elif rt.frequency == 'yearly':
            rt.next_due = today + relativedelta(years=1)
        rt.save()
