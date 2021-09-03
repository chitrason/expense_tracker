from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Income(models.Model):
  source = models.CharField(max_length=100)
  income = models.IntegerField()
  date = models.DateField('date')
  age = models.IntegerField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name  

#this will take us back to the cat details that we just created
  def get_absolute_url(self):
    return reverse('incomes_detail', kwargs={'cat_id': self.id})