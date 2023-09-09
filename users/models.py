from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class MyUser(AbstractUser):
#     USERNAME_FIELD = 'email'
#     email = models.EmailField(_('email address'), unique=True) # changes email to unique and blank to false
#     REQUIRED_FIELDS = [] # removes email from REQUIRED_FIELDS
