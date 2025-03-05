from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    def create_user_entity(self, role, cpf, email, password=None, **extra_fields):
        if not cpf:
            raise ValueError('The CPF must be set')
        if not email:
            raise ValueError('The email must be set')
        
        email = self.normalize_email(email)
        extra_fields.setdefault('username', cpf)
        user = self.model(cpf=cpf, email=email, **extra_fields)
        user.set_password(password)

        if role == 'student':
            user.is_student = True
        elif role == 'teacher':
            user.is_teacher = True
        elif role == 'manager':
            user.is_manager = True

        user.save(using=self._db)
        return user

class User(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=False, unique=True)
    curso = models.ForeignKey('lms.Curso', on_delete=models.SET_NULL, related_name='alunos_curso', null=True, blank=True)
    cursos = models.ManyToManyField('lms.Curso', related_name='professores_curso', blank=True) # professores podem estar em vários cursos
    materias = models.ManyToManyField('lms.Materia', related_name='users_materia', blank=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['email', 'name']

    objects = UserManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def clean(self):
        """
        Validação personalizada para garantir que:
        - Alunos só possam estar em um curso.
        - Professores possam estar em vários cursos.
        """
        super().clean()

        if self.pk is not None:
            if self.is_student and self.cursos.exists():
                raise ValidationError("Alunos não podem estar associados a múltiplos cursos. Use o campo 'curso'.")

            if self.is_teacher and self.curso:
                raise ValidationError("Professores não podem estar associados a um único curso. Use o campo 'cursos'.")

    def save(self, *args, **kwargs):
        self.clean() 
        super().save(*args, **kwargs)

    def get_materia_students(self):
        return self.materias.filter(users_materia__id=self.id, users_materia__is_student=True).distinct()

    def get_materia_teacher(self):
        return self.materias.filter(users_materia__id=self.id, users_materia__is_teacher=True).distinct()

    def get_cursos_teacher(self):
        if self.is_teacher:
            return self.cursos.all()
        return None
    
    def get_curso_student(self):
        if self.is_student:
            return self.curso
        return None