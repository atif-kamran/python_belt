from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    confirm_password = models.CharField(max_length = 100)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)

    #need to look up password hash equivalent
