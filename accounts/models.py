from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser 

class User (AbstractUser):
    mobile_number = models.CharField(max_length=15,blank=True ,null=True)

