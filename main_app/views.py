from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
  return HttpResponse('home page for expense app')

def incomes_index(request):
  return HttpResponse('incomes index')