from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'transactions/account_list.html', {'accounts': accounts})

@login_required
def account_create(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            acc = form.save(commit=False)
            acc.user = request.user
            acc.save()
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

from .forms import PDFUploadForm
from PyPDF2 import PdfReader
import pandas as pd
import tabula

@login_required
def import_pdf(request):
    if request.method == "POST":
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['file']
            # Simple text extraction example:
            reader = PdfReader(pdf_file)
            all_text = ""
            for page in reader.pages:
                all_text += page.extract_text() or ""
            # You would parse 'all_text' to find transaction lines, then create Transaction objects
            
            # -- For tabular PDFs --
            # pdf_file.seek(0)  # Required if you read it above
            # dfs = tabula.read_pdf(pdf_file, pages='all', multiple_tables=True, stream=True)
            # for df in dfs:
            #     # Process each DataFrame row as a transaction

            messages.success(request, "PDF parsed (demo). Implement transaction parsing logic!")
            return redirect('transaction_list')
    else:
        form = PDFUploadForm()
    return render(request, 'transactions/import_pdf.html', {'form': form})