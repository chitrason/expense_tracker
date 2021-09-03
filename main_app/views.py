from django.shortcuts import render, redirect
from .models import Income
from django.http import HttpResponse

# Create your views here.
def home(request):
  return HttpResponse('home page for expense app')

def incomes_index(request):
  incomes = Income.objects.all()
  return render(request, 'incomes/index.html', { 'incomes': incomes})