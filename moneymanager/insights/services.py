from transactions.models import Transaction
from django.db.models import Sum

def get_savings_tip(user):
    # Very basic tip: find top expense category
    data = (Transaction.objects.filter(user=user, transaction_type='expense')
            .values('category__name')
            .annotate(total=Sum('amount'))
            .order_by('-total'))
    if data and data[0]['total'] > 0:
        top_cat = data[0]['category__name']
        return f"Tip: You spent most on {top_cat}. Try reducing this category for better savings."
    return "Great job! No major expense hotspots this month."