from django.urls import path
from . import views

urlpatterns = [
    path("", views.portfolio_list, name="portfolio_list"),
    path("add/", views.holding_add, name="holding_add"),
]