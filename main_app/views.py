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
    
  paginator=Paginator(incomes, 3) #split up in pages. 2 per page
  page_number=request.GET.get('page')
  page_obj=Paginator.get_page(paginator, page_number)
  income_index = {
    'incomes': incomes,
    'page_obj': page_obj,
    # 'balance': returnSum()
  }
  return render(request, 'incomes/index.html', income_index)
  # return render(request, 'incomes/index.html', { 'incomes': incomes})

def expenses_index(request):
  expenses = Expense.objects.all()
  paginator=Paginator(expenses, 2) #split up in pages. 2 per page
  page_number=request.GET.get('page')
  page_obj=Paginator.get_page(paginator, page_number)
  expense_index = {
    'expenses': expenses,
    'page_obj': page_obj
  }
  return render(request, 'expenses/index.html', expense_index)
  # return render(request, 'expenses/index.html', { 'expenses': expenses})

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

# def add_expense(request, category_id):
#   new_expense = None
#   form = ExpenseForm(request.POST)
#   if form.is_valid():
#     new_expense = form.save(commit=False)
#     new_expense.category_id = category_id
#     new_expense.save()
#   return redirect('expenses_index', category_id=category_id)  

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)

class CategoryCreate(CreateView):
  model = Category
  fields = ['name']

# 

def expense_category_summary(request):
  # todays_date = datetime.date.today()
  # six_months_ago = todays_date-datetime.timedelta(days=30*6)
  # expenses = Expense.objects.all()
  expenses = Expense.objects.filter(owner=request.user)
    # date__gte=six_months_ago, date__lte=todays_date)
  print('expenses', expenses) #these are getting categories
  finalrep = {}

  def get_category(expense):
    return expense.category
  
  category_list = list(set(map(get_category, expenses))) #filters out duplicate categories

  print('category_list', category_list)

  def get_expense_category_amount(category):
    amount = 0
    filtered_by_category = expenses.filter(category=category)
  
    for item in filtered_by_category:
      amount += item.amount
    # print('filtered_by_category the sum of each category', amount) # we get 8 results but the totals are correct
    return amount               #getting the total of each category

  for x in expenses:
    for y in category_list:
      finalrep[y] = get_expense_category_amount(y)
      # print('each category in the category list :', y) 

  print('finalrep', finalrep)
  return JsonResponse('hello', safe=False)
  # return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats_view(request):
  return render(request, 'expenses/stats.html')
