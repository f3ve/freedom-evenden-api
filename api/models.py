"""
User Models
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    """
    customer user manager incase I need to alter the way users are created in
    the future.
    """

    def create_user(self, email, username, full_name, password=None):
        """
        creates a user
        """

        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        if not full_name:
            raise ValueError("Name is required")

        user = self.model(email=self.normalize_email(email), username=username)

        user.set_password(password)
        user.save(self._db)
        return user

    def create_superuser(self, email, username, full_name, password):
        """
        creates a superuser
        """
        user = self.create_user(
            email=self.normalize_email(email), username=username, password=password,
            full_name=full_name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    Custom user model, Django recommends creating a custom user model to make it
    easier to alter it in the future.
    """

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    full_name = models.CharField(max_length=60)
    date_joined = models.DateTimeField(
        verbose_name="created", auto_now_add=True)
    last_modified = models.DateTimeField(
        verbose_name="modified", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "full_name"]

    objects = MyUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm):
        """
        has_perm
        """
        print(perm)
        return self.is_admin

    def has_module_perms(self, perm):
        """
        has_module_perms
        """
        if perm == "auth":
            return self.is_superuser
        return self.is_admin
