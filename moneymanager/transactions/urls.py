from django.urls import path
from . import views

urlpatterns = [
    # Dashboard & CSV Export
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transactions/export/', views.export_transactions_csv, name='export_transactions_csv'),

    # Transactions
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/add/', views.transaction_create, name='transaction_create'),
    path('transactions/<int:pk>/edit/', views.transaction_edit, name='transaction_edit'),
    path('upload/', views.transaction_upload, name='transaction_upload'),

    # Accounts
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/add/', views.account_create, name='account_create'),

    # Categories
    path('add_category/', views.add_category, name='add_category'),
    path('categories/', views.category_list, name='category_list'),

    # Recurring Transactions
    path('recurring/', views.recurring_transaction_list, name='recurring_transaction_list'),
    path('recurring/add/', views.recurring_transaction_create, name='recurring_transaction_create'),

    # Budgets
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/add/', views.budget_create, name='budget_create'),

    # Tags
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/add/', views.tag_create, name='tag_create'),
]
