from django.db import models
import bcrypt
import re

# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, data):
        errors = []
        if len(data['name']) < 2:
            errors.append('Name must be at least 2 characters')
        if len(data['alias']) < 2:
            errors.append('alias must be at least 2 characters')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(data['email']):
            errors.append('Invalid email address')
        if data['password'] != data['confirm_password']:
            errors.append('Passwords do not match')
        existing_emails = User.objects.filter(email = data['email'])
        if len(existing_emails) > 0:
            errors.append('Email already in use')
        existing_alias = User.objects.filter(alias = data['alias'])
        if len(existing_alias) > 0:
            errors.append('Alias already in use')
        return errors

    def create_user(self, data):
        hashed_pw =bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            name =data['name'],
            alias =data['alias'],
            email =data['email'],
            password = hashed_pw
        )
        return user.id

    def login(self, data):
        existing_user = User.objects.filter(email = data['email'])
        if not existing_user:
            return (False, 'Invalid email or password')
        user = existing_user[0]
        if bcrypt.checkpw(data['password'].encode(), user.password.encode()):
            return (True, user)
        else:
            return (False, 'Invalid email or password')

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()