from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from .models import Category, Income, Expense
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from .forms import ExpenseForm
from django.http import JsonResponse
from django.http import HttpResponse

# Create your views here.
# def home(request):
#   incomes = Income.objects.all()
#   expenses = Expense.objects.all()
#   context = {
#     'incomes': incomes,
#     'expenses': expenses
#   }

#   return render(request, 'home.html', context)

class Home(LoginView):
  template_name = 'home.html'

@login_required
def incomes_index(request):
  todays_date = datetime.date.today()
  thirty_days_ago = todays_date-datetime.timedelta(days=30)
  incomes_thirty_days_ago = Income.objects.filter(user=request.user,
    date__gte=thirty_days_ago, date__lte=todays_date)
  incomes = Income.objects.filter(user=request.user)
  paginator = Paginator(incomes, 3) #split up in pages. 3 per page
  page_number = request.GET.get('page')
  page_obj = Paginator.get_page(paginator, page_number)

  def incomes_total(incomes):
    amount = 0

    for income in incomes_thirty_days_ago:
      amount += income.amount
    print('expense amount', amount)
    return amount

  income_index = {
    'incomes': incomes,
    'page_obj': page_obj,
    'total': incomes_total(incomes)
  }
  return render(request, 'incomes/index.html', income_index)

@login_required
def expenses_index(request):
  todays_date = datetime.date.today()
  thirty_days_ago = todays_date-datetime.timedelta(days=30)
  expenses_thirty_days_ago = Expense.objects.filter(user=request.user,
    date__gte=thirty_days_ago, date__lte=todays_date)
  expenses = Expense.objects.filter(user=request.user)
  paginator = Paginator(expenses, 3)
  page_number = request.GET.get('page')
  page_obj = Paginator.get_page(paginator, page_number)

  def expenses_total(expenses):
    amount = 0

    for expense in expenses_thirty_days_ago:
      amount += expense.amount
    print('expense amount', amount)
    return amount

  expense_index = {
    'expenses': expenses,
    'page_obj': page_obj,
    'total': expenses_total(expenses)
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

@login_required
def expense_category_summary(request):
  todays_date = datetime.date.today()
  thirty_days_ago = todays_date-datetime.timedelta(days=30)
  expenses = Expense.objects.filter(user=request.user,
  date__gte=thirty_days_ago, date__lte=todays_date)
  finalrep = {}

  def get_category(expense):
    return expense.category
  category_list = list(set(map(get_category, expenses)))
  print(category_list)

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

@login_required
def income_summary(request):
  todays_date = datetime.date.today()
  thirty_days_ago = todays_date-datetime.timedelta(days=30)
  incomes = Income.objects.filter(user=request.user,
  date__gte=thirty_days_ago, date__lte=todays_date)
  finalrep = {}

  def get_source(income):
    return income.source
  source_list = list(set(map(get_source, incomes)))  
  print(source_list)
  
  # def get_amount(income):
  #   return income.amount
  # amount_list = list(set(map(get_amount, incomes)))  
  # print(amount_list)

  # for x in incomes:
  #   for y in source_list:
  #     finalrep[y] = get_amount(y)
  # print(finalrep)

  def get_income_amount(source):
    amount = 0
    filtered_by_source = incomes.filter(source=source)

    for item in filtered_by_source:
      amount += item.amount
    return amount

  for x in incomes:
    for y in source_list:
      finalrep[y] = get_income_amount(y)

  return JsonResponse({'income_data': finalrep}, safe=False)
