from django.urls import path
from . import views

urlpatterns = [
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/add/', views.account_create, name='account_create'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/add/', views.transaction_create, name='transaction_create'),
    path('upload/', views.transaction_upload, name='transaction_upload'),
    path('add_category/', views.add_category, name='add_category'),
    path('categories/', views.category_list, name='category_list'),
]