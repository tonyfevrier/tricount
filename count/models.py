from django.db import models
from django.utils import timezone

# Create your models here.

class Counts(models.Model):
    title = models.TextField(default='')
    password = models.TextField(default='')
    description = models.TextField(default='')
    currency = models.TextField(default = '')
    category = models.TextField(default='')
    participants = models.JSONField(default=[]) 
    data = models.TextField(default='') # contains credits for calculations of equilibria.
    admins = models.JSONField(default=[]) 

class Spending(models.Model):
    title = models.TextField(default='')
    amount = models.FloatField(default=0.)
    payer = models.TextField(default='')
    receivers = models.JSONField(default=[]) 
    tricount = models.ForeignKey(Counts, on_delete=models.CASCADE, related_name='spendings')
    date = models.DateField(default = timezone.now) 
