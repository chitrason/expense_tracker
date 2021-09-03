from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('incomes/', views.incomes_index, name='incomes_index' )
]