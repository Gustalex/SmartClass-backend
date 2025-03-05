from django.db import models
from .factory_model import FactoryModel

class Materia(FactoryModel):
    nome = models.CharField(max_length=255)
    carga_horaria = models.IntegerField()
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, related_name='materias_curso')  
    aulas = models.ManyToManyField('Aula', related_name='materias_aula')  
    professor = models.ForeignKey('auth_service.User', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nome
    
    class Meta:
        db_table = 'materia'
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'