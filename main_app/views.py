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
from .forms import ExpenseForm
from django.http import JsonResponse
from django.http import HttpResponse


class Home(LoginView):
  template_name = 'home.html'

@login_required
def incomes_index(request):
  incomes = Income.objects.filter(user=request.user)
  if len(incomes) == 0:
    return redirect('incomes_create')

  todays_date = datetime.date.today()
  thirty_days_ago = todays_date-datetime.timedelta(days=30)
  incomes_thirty_days_ago = Income.objects.filter(user=request.user,
    date__gte=thirty_days_ago, date__lte=todays_date)
  paginator = Paginator(incomes, 3) #split up in pages. 3 per page
  page_number = request.GET.get('page')
  page_obj = Paginator.get_page(paginator, page_number)

  def incomes_total(incomes):
    amount = 0

    for income in incomes_thirty_days_ago:
      amount += income.amount
      format_float = "{:.2f}".format(amount)
    print('expense amount', format_float)
    return format_float

  income_index = {
    'incomes': incomes,
    'page_obj': page_obj,
    'total': incomes_total(incomes)
  }
  return render(request, 'incomes/index.html', income_index)

@login_required
def expenses_index(request):
  expenses = Expense.objects.filter(user=request.user)
  if len(expenses) == 0:
    return redirect('expenses_create')

  todays_date = datetime.date.today()
  thirty_days_ago = todays_date-datetime.timedelta(days=30)
  expenses_thirty_days_ago = Expense.objects.filter(user=request.user,
    date__gte=thirty_days_ago, date__lte=todays_date)
  paginator = Paginator(expenses, 3)
  page_number = request.GET.get('page')
  page_obj = Paginator.get_page(paginator, page_number)

  def expenses_total(expenses):
    amount = 0

    for expense in expenses_thirty_days_ago:
      amount += expense.amount
      format_float = "{:.2f}".format(amount)
    print('expense amount', format_float)

    return format_float

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
      format_float = "{:.2f}".format(amount)
    return format_float

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

  def get_income_amount(source):
    amount = 0
    filtered_by_source = incomes.filter(source=source)

    for item in filtered_by_source:
      amount += item.amount
      format_float = "{:.2f}".format(amount)
    return format_float

  for x in incomes:
    for y in source_list:
      finalrep[y] = get_income_amount(y)

  return JsonResponse({'income_data': finalrep}, safe=False)

def income_expense_summary(request):
  incomes = Income.objects.filter(user=request.user)
  expenses = Expense.objects.filter(user=request.user)
  if len(incomes) == 0 and len(expenses) == 0:
    return redirect('incomes_create')
  
  todays_date = datetime.date.today()
  thirty_days_ago = todays_date-datetime.timedelta(days=30)
  incomes_thirty_days_ago = Income.objects.filter(user=request.user,
    date__gte=thirty_days_ago, date__lte=todays_date)
  expenses_thirty_days_ago = Expense.objects.filter(user=request.user,
    date__gte=thirty_days_ago, date__lte=todays_date)

  def incomes_total(incomes):
    income_total = 0

    for income in incomes_thirty_days_ago:
      income_total += income.amount
    return income_total

  def expenses_total(expenses):
    expense_total = 0

    for expense in expenses_thirty_days_ago:
      expense_total += expense.amount
    return expense_total

  def net_worth(income_total, expense_total):
    net = income_total - expense_total
    return net  

  context = {
    'incomes': incomes,
    'expenses': expenses,
    'expenses_total': "{:.2f}".format(expenses_total(expenses_thirty_days_ago)),
    'incomes_total': "{:.2f}".format(incomes_total(incomes_thirty_days_ago)),
    'net_worth': "{:.2f}".format(net_worth(incomes_total(incomes_thirty_days_ago), expenses_total(expenses_thirty_days_ago))),
    'percent_savings': "{:.2f}".format((100*(incomes_total(incomes_thirty_days_ago) - expenses_total(expenses_thirty_days_ago)))/(incomes_total(incomes_thirty_days_ago)))
  }

  return render(request, 'summary.html', context)

