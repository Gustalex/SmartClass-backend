from django.db import models
from .factory_model import FactoryModel

class Turma(FactoryModel):
    nome = models.CharField(max_length=255)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, related_name='turmas_curso')  
    materia = models.CharField(max_length=255)
    professor = models.ForeignKey('auth_service.User', on_delete=models.DO_NOTHING, related_name='turmas_professor')
    alunos = models.ManyToManyField('auth_service.User', related_name='turmas_aluno')  

    def __str__(self):
        return self.nome
    
    class Meta:
        db_table = 'turma'
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'