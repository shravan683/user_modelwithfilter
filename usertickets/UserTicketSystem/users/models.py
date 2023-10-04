from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
class CustomUser(AbstractUser):
    pass

class Ticket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=1)


    def __str__(self):
        return self.title

        return self.title
