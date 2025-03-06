from rest_framework import serializers
from ..models import Curso
from .materia_serializer import MateriaSerializer

class CursoSerializer(serializers.ModelSerializer):
    materias = MateriaSerializer(many=True, read_only=True)  

    class Meta:
        model = Curso
        fields = ['id', 'nome', 'materias']