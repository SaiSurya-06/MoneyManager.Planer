from django.urls import path
from . import views

urlpatterns = [
    path('', views.insights_page, name='insights'),
]