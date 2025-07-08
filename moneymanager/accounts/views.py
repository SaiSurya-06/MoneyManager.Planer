from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm, PartnerLinkForm
from .models import Profile, PartnerAccount
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
    partners = PartnerAccount.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {'p_form': p_form, 'partners': partners})

@login_required
def partner_link(request):
    if request.method == 'POST':
        form = PartnerLinkForm(request.POST)
        if form.is_valid():
            partner = form.cleaned_data['partner']
            if partner == request.user:
                messages.error(request, "You cannot add yourself as a partner.")
            else:
                PartnerAccount.objects.get_or_create(user=request.user, partner=partner, defaults={'can_edit': form.cleaned_data['can_edit']})
                messages.success(request, f"Partner {partner.username} linked.")
            return redirect('profile')
    else:
        form = PartnerLinkForm()
    return render(request, 'accounts/partner_link.html', {'form': form})

@login_required
def partner_profile(request, partner_id):
    partner_user = get_object_or_404(User, id=partner_id)
    if not PartnerAccount.objects.filter(user=request.user, partner=partner_user).exists():
        messages.error(request, "No partner relationship.")
        return redirect('profile')
    partner_profile = partner_user.profile
    return render(request, 'accounts/partner_profile.html', {'partner': partner_profile, 'partner_user': partner_user})

from transactions.models import Transaction  # or your actual model import

@login_required
def partner_transactions(request, partner_id):
    partner_user = get_object_or_404(User, id=partner_id)
    if not PartnerAccount.objects.filter(user=request.user, partner=partner_user).exists():
        messages.error(request, "No partner relationship.")
        return redirect('profile')
    transactions = Transaction.objects.filter(user=partner_user)
    return render(request, 'accounts/partner_transactions.html', {
        'partner_user': partner_user,
        'transactions': transactions
    })