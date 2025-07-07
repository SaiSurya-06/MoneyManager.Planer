from django.urls import path
from . import views

urlpatterns = [
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/add/', views.account_create, name='account_create'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/add/', views.transaction_create, name='transaction_create'),
    path('transactions/import_pdf/', views.import_pdf, name='import_pdf'),
]