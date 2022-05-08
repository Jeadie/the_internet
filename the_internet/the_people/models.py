from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.utils import timezone
# from the_people.managers import UserManager

class UserProfile(models.Model):
    """Profile details of a user unrelated to the authentication mechanism."""


class UserManager(BaseUserManager):

    @classmethod
    def get_UserManager(cls):
        manager = UserManager()
        manager.model = User
        return manager

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), profile=UserProfile.objects.create())
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, email,password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """"""
    email = models.EmailField(verbose_name='email address', unique=True)
    profile = models.OneToOneField(to=UserProfile, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.email)