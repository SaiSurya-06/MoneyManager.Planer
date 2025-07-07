from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .services import get_savings_tip

@login_required
def insights_page(request):
    tip = get_savings_tip(request.user)
    return render(request, 'insights/insights.html', {'tip': tip})