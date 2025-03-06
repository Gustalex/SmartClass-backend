from rest_framework import serializers
from .atividade_serializer import AtividadeSerializer
from ..models import Aula 

class AulaSerializer(serializers.ModelSerializer):
    atividades = AtividadeSerializer(many=True, read_only=True)
    class Meta:
        model = Aula
        fields = ['id', 'titulo', 'descricao', 'conteudo', 'materia', 'atividades']