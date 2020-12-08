"""
API Models
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


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

        user = self.model(email=self.normalize_email(email),
                          username=username, full_name=full_name)

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


class User(AbstractBaseUser, PermissionsMixin):
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

    def has_perm(self, perm, obj=None):
        """
        has_perm
        """
        return self.is_active


class Category(models.Model):
    """
    Category model
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='children', on_delete=models.CASCADE
    )

    class Meta:
        # enforcing that there can not be two categories under a parent with same slug

        # __str__ method elaborated later in post.  use __unicode__ in place of

        # __str__ if you are using python 2

        unique_together = ('slug', 'parent',)
        verbose_name_plural = "categories"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class Article(models.Model):
    """
    Article model for blog posts
    """
    title = models.CharField(max_length=100, default='New Post')
    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='articles', default='1'
    )
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.CASCADE
    )
    slug = models.SlugField(unique=True)
    draft = models.BooleanField(default=True)
    publish_date = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.title

    def get_cat_list(self):
        """
        returns list of categories
        """
        k = self.category  # for now ignore this instance method

        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]

    def asdict(self):
        """
        Converts Article object to a dict
        """
        return {
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "category": self.category,
            "slug": self.slug,
            "draft": self.draft,
            "publish_date": self.publish_date
        }
