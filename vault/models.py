from django.db import models
from django.contrib.auth.models import User

class Passwords(models.Model):
    site=models.CharField(max_length=100)
    password=models.CharField(max_length=256)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.site
