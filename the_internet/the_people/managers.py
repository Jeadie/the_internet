# from django.contrib.auth.models import (
#    BaseUserManager
# )

# from the_people.models import UserProfile

# class UserManager(BaseUserManager):

#    def create_user(self, email, password=None):
#        if not email:
#            raise ValueError('Users must have an email address')
 
#        user = self.model(email=self.normalize_email(email), profile=UserProfile.objects.create())
#        user.set_password(password)
#        user.save(using=self._db)
#        return user
 
#    def create_superuser(self, email,password=None):
#        """
#        Creates and saves a superuser with the given email, date of
#        birth and password.
#        """
#        user = self.create_user(email,password=password)
#        user.is_admin = True
#        user.save(using=self._db)
#        return user
