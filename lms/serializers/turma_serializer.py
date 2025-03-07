from rest_framework import serializers
from auth_service.serializers import UserSerializer
from ..models import Turma
from ..serializers import CursoSerializer, MateriaSerializer

class TurmaSerializer(serializers.ModelSerializer):
    professor = UserSerializer(read_only=True)
    materia = MateriaSerializer(read_only=True)
    curso = CursoSerializer(read_only=True)
    alunos = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Turma
        fields = ['id', 'nome', 'curso', 'materia', 'professor', 'alunos']