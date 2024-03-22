from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import EmailValidator, MinLengthValidator


class UserManager(BaseUserManager):

    def create_user(self, email, full_name, age, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, age=age, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, age, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        return self.create_user(email, full_name, age, password, **extra_fields)


class User(AbstractBaseUser):

    email = models.EmailField(
        max_length=250,
        unique=True,
        validators=[EmailValidator("Please Enter the Valid Email Id")],
    )
    full_name = models.CharField(
        max_length=250,
        validators=[MinLengthValidator(3, message="please enter the valid name")],
    )
    age = models.IntegerField()
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "age"]


class Subscription(models.Model):
    gc_name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
