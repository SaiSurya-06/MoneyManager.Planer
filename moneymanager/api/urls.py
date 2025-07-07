from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'profile', views.ProfileViewSet, basename='profile')
router.register(r'accounts', views.AccountViewSet, basename='accounts')
router.register(r'categories', views.CategoryViewSet, basename='categories')
router.register(r'transactions', views.TransactionViewSet, basename='transactions')
router.register(r'budgets', views.BudgetViewSet, basename='budgets')
router.register(r'holdings', views.HoldingViewSet, basename='holdings')

urlpatterns = router.urls