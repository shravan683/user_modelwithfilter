from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass

class Ticket(models.Model):  
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title
