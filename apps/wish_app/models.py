from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from datetime import datetime 
import re

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name_input']) < 3:
            errors["first_name_input"] = "First name should be a minimum of 3 characters"
        if len(postData['last_name_input']) < 3:
            errors["last_name_input"] = "Last name should be a minimum of 3 characters"
        if not re.match('[^@]+@[^@]+\.[^@]+', postData['email_input']):
            errors["email_input"] = "Email is not valid"
        if User.objects.filter(email=postData['email_input']):
            errors["email_input"] = "Email already in use"
        if len(postData['password_input']) < 8:
            errors["password_input"] = "Password is less than 8 characters"
        if (postData['password_input']) != (postData['password_confirmation_input']):
            errors['password_confirmation_input'] = "Passwords do not match"
        return errors

class User(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=20)
    objects = UserManager()

class WishManager(models.Manager):
    def wish_validator(self, postData):
        wish_errors = {}
        if len(postData["item_input"]) < 3:
            wish_errors["item_input"] = "Item must be a minimum of 3 characters"
        if len(postData["description_input"]) < 3:
            wish_errors["description_input"] = "Description must be a minimum of 3 characters"
        return wish_errors

class Wish(BaseModel):
    item = models.CharField(max_length=255)
    description = models.TextField()
    granted = models.ManyToManyField(User, related_name="granted_wish")
    creator = models.ForeignKey(User, related_name="created_wish")
    like = models.ManyToManyField(User, related_name="liked_wish")
    objects = WishManager()