from django.db import models

# Create your models here.
class Counts(models.Model):
    title = models.TextField(default='')
    description = models.TextField(default='')
    category = models.TextField(default='')