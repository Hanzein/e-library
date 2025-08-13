from django.contrib.auth.models import AbstractUser
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    name = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"Profile of {self.user.email}"