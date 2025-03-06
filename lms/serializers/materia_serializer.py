from rest_framework import serializers
from ..models import Materia
from .aula_serializer import AulaSerializer

class MateriaSerializer(serializers.ModelSerializer):
    aulas = AulaSerializer(many=True, read_only=True)

    class Meta:
        model = Materia
        fields = ['id', 'nome', 'carga_horaria', 'curso', 'professor', 'aulas']