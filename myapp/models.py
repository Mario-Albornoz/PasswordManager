from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PasswordEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.BinaryField()
    iv = models.BinaryField()  # initialization vector for AES
    created_at = models.DateTimeField(auto_now_add=True)