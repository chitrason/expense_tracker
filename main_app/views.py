from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Income, Expense
from django.http import HttpResponse

# Create your views here.
def home(request):
  return HttpResponse('home page for expense app')

def expenses_index(request):
  expenses = Expense.objects.all()
  return render(request, 'expenses/index.html', { 'expenses': expenses})

def incomes_index(request):
  incomes = Income.objects.all()
  return render(request, 'incomes/index.html', { 'incomes': incomes})


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