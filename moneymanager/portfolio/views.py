from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Holding
from .forms import HoldingForm
from .utils import fetch_stock_price, fetch_mf_price

@login_required
def portfolio_list(request):
    holdings = Holding.objects.filter(user=request.user)
    portfolio = []
    total_invested = 0
    total_current = 0
    for h in holdings:
        price = (
            fetch_stock_price(h.symbol)
            if h.asset_type == "stock"
            else fetch_mf_price(h.symbol)
        )
        invested = float(h.invested)
        current_value = float(h.quantity) * price if price else invested
        total_invested += invested
        total_current += current_value
        portfolio.append({
            "holding": h,
            "live_price": price,
            "current_value": current_value,
            "gain": current_value - invested,
            "gain_pct": ((current_value - invested) / invested * 100) if invested else 0,
        })
    return render(
        request,
        "portfolio/portfolio_list.html",
        {
            "portfolio": portfolio,
            "total_invested": total_invested,
            "total_current": total_current,
        },
    )

@login_required
def holding_add(request):
    if request.method == "POST":
        form = HoldingForm(request.POST)
        if form.is_valid():
            hold = form.save(commit=False)
            hold.user = request.user
            hold.save()
            return redirect("portfolio_list")
    else:
        form = HoldingForm()
    return render(request, "portfolio/holding_form.html", {"form": form})