from django.forms import ModelForm
from .models import Expense, User

class ExpenseForm(ModelForm):
  class Meta:
    model = Expense
    fields = ['title', 'amount', 'date', 'description', 'category']

class LoginForm(ModelForm):
  class Meta:
    model = User
    fields = ['username', 'password']