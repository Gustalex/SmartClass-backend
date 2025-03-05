from django.db import models
from .factory_model import FactoryModel

class Atividade(FactoryModel):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    conteudo = models.TextField(blank=False, null=False, default=None)
    aula = models.ForeignKey('Aula', on_delete=models.CASCADE)  
    data_entrega = models.DateField()

    def __str__(self):
        return self.titulo
    
    class Meta:
        db_table = 'atividade'
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'
        ordering = ['titulo']