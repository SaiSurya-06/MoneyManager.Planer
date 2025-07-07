from rest_framework import serializers
from accounts.models import Profile, PartnerAccount
from transactions.models import Account, Category, Transaction
from budgets.models import Budget
from portfolio.models import Holding
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ['user', 'phone', 'avatar']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'account_type', 'balance']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'is_custom']

class TransactionSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Transaction
        fields = ['id', 'date', 'description', 'amount', 'transaction_type', 'account', 'category']

class BudgetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Budget
        fields = ['id', 'category', 'month', 'limit']

class HoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holding
        fields = ['id', 'asset_type', 'symbol', 'name', 'quantity', 'avg_price', 'added_on']