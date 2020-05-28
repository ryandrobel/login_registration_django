from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, post_data):
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(post_data['first_name']) < 1 or len(post_data['first_name']) > 32:
            errors["first_name"] = 'First Name must be 1 to 32 characters long'

        if len(post_data['last_name']) < 1 or len(post_data['last_name']) > 32:
            errors["last_name"] = 'Last Name must be 1 to 32 characters long'
        
        if len(post_data['username']) < 1 or len(post_data['username']) > 32:
            errors["username"] = 'Username must be 1 to 32 characters long'

        if not email_regex.match(post_data['email']):
            errors['email'] = 'Please provide a valid email address'
        try:
            User.objects.get(email = post_data['email'])
            errors['email'] = 'Email already in use'
        except:
            pass

        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least eight characters long'

        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = 'Password do not match'

        return errors
        # add keys and values to errors dictionary for each invalid field
        

class User(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.CharField(max_length=254)
    password = models.CharField(max_length=60)
    username = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
