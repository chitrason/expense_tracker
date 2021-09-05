from django.db import models
from django.urls import reverse
from datetime import date
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Income(models.Model):
  source = models.CharField(max_length=100)
  description = models.CharField(max_length=100)
  amount = models.FloatField() #can be a decimal
  date = models.DateField(default=now)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.source  

  class Meta: #most recent at the top
    ordering = ['-date']

  def get_absolute_url(self): #this will link us to the income detail page
    return reverse('incomes_index')
    # return reverse('incomes_detail', kwargs={'income_id': self.id})

class Category(models.Model):
  name = models.CharField(max_length=100)
  # expense = models.ForeignKey(Expense, on_delete=models.CASCADE)

  class Meta:
    verbose_name_plural = 'Categories'

  def __str__(self):
    return self.name 

  def get_absolute_url(self): #this will link us to the income detail page
    return reverse('expenses_index')


class Expense(models.Model):
  title = models.CharField(max_length=100)
  amount = models.FloatField()
  date = models.DateField(default=now)
  description = models.CharField(max_length=100)
  owner = models.ForeignKey(User, on_delete=models.CASCADE) 
  category = models.ForeignKey(Category, on_delete=models.CASCADE) 
  # category = models.CharField(max_length=250) 
  # change this to category

  def __str__(self):
    return self.title 

  class Meta:
    ordering = ['-date']

  def get_absolute_url(self): #this will link us to the income detail page
    return reverse('expenses_index')
