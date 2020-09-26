from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates a new user using email and password passed as arguements"""
        if not email:
            raise ValueError('Please provide a valid email id \
                              for user creation')
        user = self.model(
            email_add=self.normalize_email(email),
            **extra_fields
            )
        user.set_password(password)

        user.save(self._db)

        return user

    def create_superuser(self, email, password=None):
        """
        Creates a new super user using email and password
        passed as arguements
        """
        superuser = self.create_user(
            email,
            password,
            is_staff=True,
            is_superuser=True
        )
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user class that supports email instead of username"""
    email_add = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email_add'
