from django.db import models

# Create your models here.
class Like(models.Model):
    count =  models.IntegerField()
