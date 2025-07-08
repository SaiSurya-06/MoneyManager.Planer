import pandas as pd
import tabula
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Transaction, Category, Account
from .forms import TransactionForm, StatementUploadForm, CategoryForm, AccountForm

@login_required
def transaction_upload(request):
    if request.method == 'POST':
        form = StatementUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                    dfs = [df]
                elif file.name.endswith('.xls') or file.name.endswith('.xlsx'):
                    df = pd.read_excel(file)
                    dfs = [df]
                elif file.name.endswith('.pdf'):
                    dfs = tabula.read_pdf(file, pages='all', multiple_tables=True)
                else:
                    raise Exception("Unsupported file type")
                if dfs:
                    # Column variants mapping
                    col_map_variants = {
                        'date': ['date', 'Date', 'transaction date', 'Transaction Date'],
                        'description': ['description', 'Description', 'desc', 'Desc'],
                        'amount': ['amount', 'Amount', 'amt', 'Amt'],
                        'type': ['type', 'Type', 'transaction type', 'Transaction Type'],
                        'category': ['category', 'Category']
                    }
                    required_cols = set(col_map_variants.keys())
                    txn_count = 0
                    duplicate_count = 0
                    for df in dfs:
                        # Normalize columns: lowercase and strip spaces
                        norm_cols = [col.strip().lower() for col in df.columns]
                        df.columns = norm_cols
                        # Map columns to expected names
                        rename_dict = {}
                        for target, variants in col_map_variants.items():
                            for v in variants:
                                if v.lower() in norm_cols:
                                    rename_dict[v.lower()] = target
                        df = df.rename(columns=rename_dict)
                        # Only process if all required columns are there
                        if not required_cols.issubset(df.columns):
                            continue
                        for _, row in df.iterrows():
                            # Defensive: skip rows with missing required fields
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
                            account_obj = Account.objects.filter(user=request.user).first()
                            # DUPLICATE CHECK: skip if identical transaction exists
                            exists = Transaction.objects.filter(
                                user=request.user,
                                date=txn_date,
                                amount=amount,
                                description=description,
                                account=account_obj,
                            ).exists()
                            if exists:
                                duplicate_count += 1
                                continue
                            Transaction.objects.create(
                                user=request.user,
                                date=txn_date,
                                description=description,
                                amount=amount,
                                transaction_type=txn_type,
                                account=account_obj,
                                category=category_obj,
                            )
                            txn_count += 1
                    if txn_count > 0:
                        msg = f"{txn_count} transaction(s) uploaded successfully!"
                        if duplicate_count > 0:
                            msg += f" {duplicate_count} duplicate(s) skipped."
                        messages.success(request, msg)
                    else:
                        messages.error(request, "No valid new transactions found in statement. (Duplicates may have been skipped.) Make sure your file has columns for date, description, amount, type, and category.")
                else:
                    messages.error(request, "No data found in statement.")
            except Exception as e:
                messages.error(request, f"Error: {e}")
            return redirect('transaction_list')
    else:
        form = StatementUploadForm()
    return render(request, 'transactions/transaction_upload.html', {'form': form})

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