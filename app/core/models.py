from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email_add, password=None, **extra_fields):
        """Creates a new user using email and password passed as arguements"""
        if not email_add:
            raise ValueError('Please provide a valid email id \
                              for user creation')
        user = self.model(
            email_add=self.normalize_email(email_add),
            **extra_fields
            )
        user.set_password(password)

        user.save(self._db)

        return user

    def create_superuser(self, email_add, password=None):
        """
        Creates a new super user using email and password
        passed as arguements
        """
        superuser = self.create_user(
            email_add,
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


class Tag(models.Model):
    """Tag model for recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient model for recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe model for recipe"""
    title = models.CharField(max_length=255)
    # Removing the user will remove all the associated recipes
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.title
