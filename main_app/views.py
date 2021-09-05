from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from .models import Category, Income, Expense
import datetime
# from .forms import ExpenseForm
from django.http import JsonResponse
from django.http import HttpResponse

# Create your views here.
class Home(LoginView):
  template_name = 'home.html'

def incomes_index(request):
  incomes = Income.objects.all()
    
  paginator=Paginator(incomes, 3) #split up in pages. 3 per page
  page_number=request.GET.get('page')
  page_obj=Paginator.get_page(paginator, page_number)
  income_index = {
    'incomes': incomes,
    'page_obj': page_obj,
  }
  return render(request, 'incomes/index.html', income_index)

def expenses_index(request):
  expenses = Expense.objects.all()
  paginator=Paginator(expenses, 3)
  page_number=request.GET.get('page')
  page_obj=Paginator.get_page(paginator, page_number)
  expense_index = {
    'expenses': expenses,
    'page_obj': page_obj
  }
  return render(request, 'expenses/index.html', expense_index)

class IncomeCreate(CreateView):
  model = Income
  fields = ['source','amount','date','description']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class IncomeUpdate(UpdateView):
  model = Income
  fields = ['source','amount','date','description']

class IncomeDelete(DeleteView):
  model = Income
  success_url = '/incomes'

class ExpenseCreate(CreateView):
  model = Expense
  fields = ['title','amount','date','description', 'category']
  
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


class ExpenseUpdate(UpdateView):
  model = Expense
  fields = ['title', 'amount', 'date', 'description', 'category']

class ExpenseDelete(DeleteView):
  model = Expense
  success_url = '/expenses'


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)

class CategoryCreate(CreateView):
  model = Category
  fields = ['name']


def expense_category_summary(request):
  expenses = Expense.objects.filter(user=request.user)
  finalrep = {}

  def get_category(expense):
    return expense.category
  category_list = list(set(map(get_category, expenses)))

  def get_expense_category_amount(category):
    amount = 0
    filtered_by_category = expenses.filter(category=category)

    for expense in filtered_by_category:
      amount += expense.amount
    return amount

  for x in expenses:
    for y in category_list:
      finalrep[y] = get_expense_category_amount(y)

  return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'expenses/stats.html')
