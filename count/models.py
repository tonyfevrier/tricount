from django.db import models
from jsonfield import JSONField


# Create your models here.
class Participants(models.Model):
    name = models.TextField(default='') 
    number = models.IntegerField(default=0)

class Counts(models.Model):
    title = models.TextField(default='')
    description = models.TextField(default='')
    category = models.TextField(default='')
    participants = models.ManyToManyField(Participants)

class Spending(models.Model):
    title = models.TextField(default='')
    amount = models.FloatField(default=0.)
    payer = models.TextField(default='')
    receivers = JSONField(default = dict)
    number = models.IntegerField(default = 0)
