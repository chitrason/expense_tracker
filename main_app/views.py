from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from .models import Category, Income, Expense
from .forms import ExpenseForm
from django.http import HttpResponse

# Create your views here.
class Home(LoginView):
  template_name = 'home.html'

def incomes_index(request):
  incomes = Income.objects.all()
  paginator=Paginator(incomes, 2) #split up in pages. 2 per page
  page_number=request.GET.get('page')
  page_obj=Paginator.get_page(paginator, page_number)
  context = {
    'incomes': incomes,
    'page_obj': page_obj
  }
  return render(request, 'incomes/index.html', context)
  # return render(request, 'incomes/index.html', { 'incomes': incomes})

def expenses_index(request):
  expenses = Expense.objects.all()
  return render(request, 'expenses/index.html', { 'expenses': expenses})

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
