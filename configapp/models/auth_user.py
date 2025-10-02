from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator


class BaseModel(models.Model):
    created_ed = models.DateField(auto_now_add=True)
    updated_ed = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email kiritilishi kerak")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Staff uchun is_staff=True bo‘lishi kerak")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser uchun is_superuser=True bo‘lishi kerak")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r'^\+9989\d{8}$',
        message="Telefon raqam +9989XXXXXXXX formatida bo‘lishi kerak"
    )

    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=13,
        null=True,
        blank=True
    )
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=128)

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    # override qilinayotgan joy
    groups = models.ManyToManyField(
        'auth.Group',
        related_name="custom_user_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="custom_user_permissions",
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email or self.phone_number or "NoEmailUser"
