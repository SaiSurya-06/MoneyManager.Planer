from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Budget
from .forms import BudgetForm

@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user).order_by('-month')
    return render(request, 'budgets/budget_list.html', {'budgets': budgets})

@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('budget_list')
    else:
        form = BudgetForm()
    return render(request, 'budgets/budget_form.html', {'form': form})