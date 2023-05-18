from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserProfile(AbstractUser):
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    region = models.CharField(max_length=200, blank=True)
    
    class Meta: 
        verbose_name = 'Profilo utente'
        verbose_name_plural = 'Profili utente'
    