import pandas as pd
import fitz  # PyMuPDF
import re
import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.utils.dateparse import parse_date
from .models import (
    Transaction, Category, Account,
    RecurringTransaction, Budget, Tag, TransactionTag
)
from .forms import (
    TransactionForm, StatementUploadForm,
    CategoryForm, AccountForm,
    RecurringTransactionForm, BudgetForm, TagForm
)


# ========== DASHBOARD ==========
@login_required
def dashboard(request):
    from django.db.models import Sum
    from django.utils.timezone import now

    user = request.user
    today = now().date()
    year = today.year

    transactions = Transaction.objects.filter(user=user, date__year=year)

    category_data = (
        transactions.filter(transaction_type='expense')
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    monthly_data = []
    for month in range(1, 13):
        income = transactions.filter(transaction_type='income', date__month=month).aggregate(Sum('amount'))['amount__sum'] or 0
        expense = transactions.filter(transaction_type='expense', date__month=month).aggregate(Sum('amount'))['amount__sum'] or 0
        monthly_data.append({
            'month': month,
            'income': float(income),
            'expense': float(expense),
            'savings': float(income - expense),
        })

    context = {
        'category_data': list(category_data),
        'monthly_data': monthly_data,
    }
    return render(request, 'transactions/dashboard.html', context)


# ========== CSV EXPORT ==========
@login_required
def export_transactions_csv(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user)

    # Optional filters
    query = request.GET.get('q')
    txn_type = request.GET.get('type')
    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if query:
        transactions = transactions.filter(description__icontains=query)
    if txn_type:
        transactions = transactions.filter(transaction_type=txn_type)
    if category:
        transactions = transactions.filter(category__name__icontains=category)
    if start_date:
        transactions = transactions.filter(date__gte=parse_date(start_date))
    if end_date:
        transactions = transactions.filter(date__lte=parse_date(end_date))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Description', 'Amount', 'Type', 'Account', 'Category'])

    for txn in transactions:
        writer.writerow([
            txn.date,
            txn.description,
            txn.amount,
            txn.transaction_type,
            txn.account.name,
            txn.category.name if txn.category else ''
        ])
    return response


# ========== TRANSACTION VIEWS ==========
@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    query = request.GET.get('q')
    txn_type = request.GET.get('type')
    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if query:
        transactions = transactions.filter(description__icontains=query)
    if txn_type:
        transactions = transactions.filter(transaction_type=txn_type)
    if category:
        transactions = transactions.filter(category__name__icontains=category)
    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)

    return render(request, 'transactions/transaction_list.html', {'transactions': transactions})


@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            txn = form.save(commit=False)
            txn.user = request.user
            txn.save()

            # Save tags
            tags_input = request.POST.get('tags', '')
            if tags_input:
                tag_names = [t.strip() for t in tags_input.split(',')]
                for name in tag_names:
                    tag_obj, _ = Tag.objects.get_or_create(user=request.user, name=name)
                    TransactionTag.objects.create(transaction=txn, tag=tag_obj)
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transactions/transaction_form.html', {'form': form})


@login_required
def transaction_edit(request, pk):
    txn = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=txn)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=txn)
    return render(request, 'transactions/transaction_form.html', {'form': form})


# ========== PDF/EXCEL UPLOAD ==========
@login_required
def transaction_upload(request):
    if request.method == 'POST':
        form = StatementUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            txn_count = 0
            duplicate_count = 0

            try:
                if file.name.endswith('.pdf'):
                    text = ""
                    with fitz.open(stream=file.read(), filetype="pdf") as doc:
                        for page in doc:
                            text += page.get_text()
                    lines = text.split('\n')
                    account_obj = Account.objects.filter(user=request.user).first()
                    if not account_obj:
                        return JsonResponse({'success': False, 'message': 'Add an account first.'})

                    i = 0
                    while i < len(lines) - 1:
                        line1 = lines[i].strip()
                        line2 = lines[i + 1].strip()

                        if re.match(r"\d{2}-[A-Z]{3}-\d{4}", line1):
                            try:
                                parts = line1.split()
                                date_str = parts[0]
                                description = ' '.join(parts[2:])
                                amounts = re.findall(r"\d{1,3}(?:,\d{3})*(?:\.\d{2})", line2)

                                amount = None
                                txn_type = None

                                if 'Cr' in line2:
                                    amount = float(amounts[0].replace(',', ''))
                                    txn_type = 'income'
                                else:
                                    amount = float(amounts[0].replace(',', ''))
                                    txn_type = 'expense'

                                txn_date = datetime.strptime(date_str, "%d-%b-%Y").date()

                                if Transaction.objects.filter(
                                    user=request.user,
                                    date=txn_date,
                                    amount=amount,
                                    description=description,
                                    account=account_obj
                                ).exists():
                                    duplicate_count += 1
                                    i += 2
                                    continue

                                category_name = "UPI" if 'upi' in description.lower() else "Uncategorized"
                                category_obj, _ = Category.objects.get_or_create(user=request.user, name=category_name)

                                Transaction.objects.create(
                                    user=request.user,
                                    date=txn_date,
                                    description=description,
                                    amount=amount,
                                    transaction_type=txn_type,
                                    account=account_obj,
                                    category=category_obj
                                )
                                txn_count += 1
                            except Exception:
                                pass
                            i += 2
                        else:
                            i += 1

                    msg = f"{txn_count} transactions uploaded."
                    if duplicate_count:
                        msg += f" {duplicate_count} duplicates skipped."
                    return JsonResponse({'success': True, 'message': msg})
                else:
                    return JsonResponse({'success': False, 'message': 'Unsupported file type'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
    else:
        form = StatementUploadForm()
    return render(request, 'transactions/import_pdf.html', {'form': form})


# ========== ACCOUNT ==========
@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'transactions/account_list.html', {'accounts': accounts})


@login_required
def account_create(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_list')
    else:
        form = AccountForm()
    return render(request, 'transactions/account_form.html', {'form': form})


# ========== CATEGORY ==========
@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.user = request.user
            cat.is_custom = True
            cat.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'transactions/category_form.html', {'form': form})


@login_required
def category_list(request):
    cats = Category.objects.filter(user=request.user)
    return render(request, 'transactions/category_list.html', {'categories': cats})


# ========== RECURRING TRANSACTIONS ==========
@login_required
def recurring_transaction_list(request):
    rec_txns = RecurringTransaction.objects.filter(user=request.user).order_by('next_due')
    return render(request, 'transactions/recurring_list.html', {'recurring_transactions': rec_txns})


@login_required
def recurring_transaction_create(request):
    if request.method == 'POST':
        form = RecurringTransactionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('recurring_transaction_list')
    else:
        form = RecurringTransactionForm()
    return render(request, 'transactions/recurring_form.html', {'form': form})


# ========== BUDGET ==========
@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'transactions/budget_list.html', {'budgets': budgets})


@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('budget_list')
    else:
        form = BudgetForm()
    return render(request, 'transactions/budget_form.html', {'form': form})


# ========== TAGS ==========
@login_required
def tag_list(request):
    tags = Tag.objects.filter(user=request.user)
    return render(request, 'transactions/tag_list.html', {'tags': tags})


@login_required
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect('tag_list')
    else:
        form = TagForm()
    return render(request, 'transactions/tag_form.html', {'form': form})
