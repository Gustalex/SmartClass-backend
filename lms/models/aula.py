from django.db import models
from .factory_model import FactoryModel

class Aula(FactoryModel):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    conteudo = models.TextField(blank=True, null=True, default=None)
    atividades = models.ManyToManyField('Atividade', related_name='aulas_atividade')   

    def __str__(self):
        return self.titulo
    
    class Meta:
        db_table = 'aula'
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['titulo']