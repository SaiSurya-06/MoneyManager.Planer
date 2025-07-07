from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from transactions.models import Transaction, Account, Category
from budgets.models import Budget
from django.db.models import Sum
from datetime import date, timedelta

@login_required
def main_dashboard(request):
    # Summary statistics
    accounts = Account.objects.filter(user=request.user)
    recent_txns = Transaction.objects.filter(user=request.user).order_by('-date')[:10]
    total_income = Transaction.objects.filter(user=request.user, transaction_type='income').aggregate(total=Sum('amount'))['total'] or 0
    total_expense = Transaction.objects.filter(user=request.user, transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0

    # Simple chart data (monthly expense by category)
    categories = Category.objects.filter(user=request.user) | Category.objects.filter(user__isnull=True)
    chart_data = []
    for cat in categories.distinct():
        amount = Transaction.objects.filter(user=request.user, category=cat, transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0
        if amount > 0:
            chart_data.append({'category': cat.name, 'amount': float(amount)})

    context = {
        'accounts': accounts,
        'recent_txns': recent_txns,
        'total_income': total_income,
        'total_expense': total_expense,
        'chart_data': chart_data,
    }
    return render(request, 'dashboard/dashboard.html', context)