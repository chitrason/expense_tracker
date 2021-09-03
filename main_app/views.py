from django.shortcuts import render, redirect
from .models import Income, Expense
from django.http import HttpResponse

# Create your views here.
def home(request):
  return HttpResponse('home page for expense app')

def incomes_index(request):
  incomes = Income.objects.all()
  return render(request, 'incomes/index.html', { 'incomes': incomes})

def expenses_index(request):
  expenses = Expense.objects.all()
  return render(request, 'expenses/index.html', { 'expenses': expenses})

# def create_expense(request):
#   return render(request, 'expenses/create_expense.html')