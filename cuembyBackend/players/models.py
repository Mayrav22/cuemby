from django.db import models

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=150)
    position = models.CharField(max_length=5)
    nation = models.CharField(max_length=50)
    club = models.CharField(max_length=50)
    id_fut = models.IntegerField(null=True)
    
    

