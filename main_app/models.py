from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Income(models.Model):
  source = models.CharField(max_length=100)
  income = models.IntegerField()
  date = models.DateField('date')
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.source  

  def get_absolute_url(self):
    return reverse('incomes_detail', kwargs={'income_id': self.id})