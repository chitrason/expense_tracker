from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('incomes/', views.incomes_index, name='incomes_index'),
  path('expenses/', views.expenses_index, name='expenses_index'),
  path('expenses/create/', views.ExpenseCreate.as_view(), name='expenses_create'),
  path('incomes/create/', views.IncomeCreate.as_view(), name='incomes_create'),
  path('incomes/<int:pk>/update', views.IncomeUpdate.as_view(), name='incomes_update'),
  path('incomes/<int:pk>/delete', views.IncomeDelete.as_view(), name='incomes_delete'),
  path('accounts/signup/', views.signup, name='signup'),

]