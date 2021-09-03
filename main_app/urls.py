from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('incomes/', views.incomes_index, name='incomes_index'),
  path('expenses/', views.expenses_index, name='expenses_index'),
  # path('expenses/create/', views.create_expense, name='expenses_create'),
]