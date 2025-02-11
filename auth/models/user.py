from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user_entity(self, role, cpf, email, password=None, **extra_fields):
        if not cpf:
            raise ValueError('The CPF must be set')
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(cpf=cpf, email=email, **extra_fields)
        user.set_password(password)
        if role == 'student':
            extra_fields.setdefault('is_student', True)
        elif role == 'teacher':
            extra_fields.setdefault('is_teacher', True)
        elif role == 'manager':
            extra_fields.setdefault('is_manager', True)
        user.save(using=self._db)
        return user

class User(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['email','name','cpf']

    objects = UserManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'