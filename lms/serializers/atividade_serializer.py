from rest_framework import serializers
from ..models import Atividade

class AtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atividade
        fields = ['id', 'titulo', 'descricao', 'conteudo', 'aula', 'data_entrega']