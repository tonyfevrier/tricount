from django.db import models

# Create your models here.
class Participants(models.Model):
    name = models.TextField(default='')
    #tricount = models.ForeignKey(Counts,on_delete=models.CASCADE)

class Counts(models.Model):
    title = models.TextField(default='')
    description = models.TextField(default='')
    category = models.TextField(default='')
    participants = models.ManyToManyField(Participants)