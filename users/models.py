from django.db import models

from datetime import datetime, timedelta
from django.conf import settings

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.utils.translation import gettext_lazy as _

from django.db.models.signals import post_save
from django.dispatch import receiver



class UserManager(BaseUserManager):
    def create_user(self,username, email,first_name,last_name, password=None):
        """Create and return a `User` with an email, username and password."""

        if email is None:
            raise TypeError('Users must have an email address.')
        if username is None:
            raise TypeError('Users must have an username.')
        if first_name is None:
            raise TypeError('Users must have an first name')
        if last_name is None:
            raise TypeError('Users must have an last name')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, first_name, last_name, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','first_name','last_name']

    objects = UserManager()

    def __str__(self):
        return self.email   

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True
    
    def __str__(self):
        return self.email


    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name

    def get_short_name(self):
        return self.first_name