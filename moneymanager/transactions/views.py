import pandas as pd
import fitz  # PyMuPDF
import re
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from django.http import JsonResponse, HttpResponse
from django.utils.dateparse import parse_date
from .models import (
    Transaction, Category, Account,
    RecurringTransaction, Tag, TransactionTag
)
from .forms import (
    TransactionForm, StatementUploadForm,
    CategoryForm, AccountForm,
    RecurringTransactionForm, TagForm
)
=======
from .models import Transaction, Category, Account
from .forms import TransactionForm, StatementUploadForm, CategoryForm, AccountForm
>>>>>>> parent of bbb7610 (update 2)


@login_required
def transaction_upload(request):
    if request.method == 'POST':
        form = StatementUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            try:
                txn_count = 0
                duplicate_count = 0

                if file.name.endswith('.pdf'):
                    file.seek(0)
                    text = ""
                    with fitz.open(stream=file.read(), filetype="pdf") as doc:
                        for page in doc:
                            text += page.get_text()

                    lines = text.split('\n')
                    account_obj = Account.objects.filter(user=request.user).first()
                    if not account_obj:
                        messages.error(request, "Please add at least one account before uploading.")
                        return redirect('account_list')

                    i = 0
                    while i < len(lines) - 1:
                        line1 = lines[i].strip()
                        line2 = lines[i + 1].strip()

                        if re.match(r"\d{2}-[A-Z]{3}-\d{4}\s+\d{2}-[A-Z]{3}-\d{4}", line1):
                            try:
                                parts = line1.split()
                                date_str = parts[0]
                                value_date_str = parts[1]
                                desc_start = line1.find(value_date_str) + len(value_date_str)
                                description = line1[desc_start:].strip()

                                # fallback: collect numeric amounts in line2
                                amounts = re.findall(r"\d{1,3}(?:,\d{3})*(?:\.\d{2})", line2)
                                withdrawal, deposit = None, None
                                if len(amounts) == 3:
                                    withdrawal, deposit, _ = amounts
                                elif len(amounts) == 2:
                                    if 'Cr' in line2:
                                        deposit = amounts[0]
                                    else:
                                        withdrawal = amounts[0]
                                elif len(amounts) == 1:
                                    if 'Cr' in line2:
                                        deposit = amounts[0]
                                    else:
                                        withdrawal = amounts[0]

                                if withdrawal:
                                    amount = float(withdrawal.replace(',', ''))
                                    txn_type = 'expense'
                                elif deposit:
                                    amount = float(deposit.replace(',', ''))
                                    txn_type = 'income'
                                else:
                                    i += 2
                                    continue

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

                    if txn_count:
                        msg = f"{txn_count} transaction(s) uploaded successfully!"
                        if duplicate_count:
                            msg += f" {duplicate_count} duplicate(s) skipped."
                        messages.success(request, msg)
                    else:
                        messages.error(request, "No valid new transactions found in PDF.")
                    return redirect('transaction_list')

                elif file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                    dfs = [df]
                elif file.name.endswith('.xls') or file.name.endswith('.xlsx'):
                    df = pd.read_excel(file)
                    dfs = [df]
                else:
                    messages.error(request, "Unsupported file type.")
                    return redirect('transaction_upload')

                if not file.name.endswith('.pdf'):
                    col_map_variants = {
                        'date': ['date', 'Date', 'transaction date', 'Transaction Date'],
                        'description': ['description', 'Description', 'desc', 'Desc'],
                        'amount': ['amount', 'Amount', 'amt', 'Amt'],
                        'type': ['type', 'Type', 'transaction type', 'Transaction Type'],
                        'category': ['category', 'Category']
                    }
                    required_cols = set(col_map_variants.keys())

                    for df in dfs:
                        norm_cols = [col.strip().lower() for col in df.columns]
                        df.columns = norm_cols
                        rename_dict = {}
                        for target, variants in col_map_variants.items():
                            for v in variants:
                                if v.lower() in norm_cols:
                                    rename_dict[v.lower()] = target
                        df = df.rename(columns=rename_dict)
                        if not required_cols.issubset(df.columns):
                            continue

                        account_obj = Account.objects.filter(user=request.user).first()
                        for _, row in df.iterrows():
                            if pd.isnull(row.get('date')) or pd.isnull(row.get('amount')):
                                continue
                            try:
                                txn_date = pd.to_datetime(row['date']).date()
                            except Exception:
                                continue

                            category_name = row.get('category', 'Uncategorized')
                            description = str(row.get('description', ''))
                            txn_type = str(row.get('type', 'expense')).lower()
                            amount = row['amount']
                            category_obj, _ = Category.objects.get_or_create(user=request.user, name=category_name)

                            if Transaction.objects.filter(
                                user=request.user,
                                date=txn_date,
                                amount=amount,
                                description=description,
                                account=account_obj
                            ).exists():
                                duplicate_count += 1
                                continue

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

                    if txn_count:
                        msg = f"{txn_count} transaction(s) uploaded successfully!"
                        if duplicate_count:
                            msg += f" {duplicate_count} duplicate(s) skipped."
                        messages.success(request, msg)
                    else:
                        messages.error(request, "No valid new transactions found in statement.")

            except Exception as e:
                messages.error(request, f"Error: {e}")
            return redirect('transaction_list')
    else:
        form = StatementUploadForm()
    return render(request, 'transactions/transaction_upload.html', {'form': form})


@login_required
def transaction_edit(request, pk):
    txn = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=txn)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction updated successfully!")
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=txn)
    return render(request, 'transactions/transaction_form.html', {'form': form})


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.user = request.user
            cat.is_custom = True
            cat.save()
            messages.success(request, "Category added!")
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'transactions/category_form.html', {'form': form})


@login_required
def category_list(request):
    cats = Category.objects.filter(user=request.user)
    return render(request, 'transactions/category_list.html', {'categories': cats})


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


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions})


@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            txn = form.save(commit=False)
            txn.user = request.user
            txn.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transactions/transaction_form.html', {'form': form})
