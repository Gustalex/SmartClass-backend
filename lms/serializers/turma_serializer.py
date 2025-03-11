from rest_framework import serializers
from auth_service.serializers import UserSerializer
from ..models import Turma, Curso
from django.contrib.auth import get_user_model
from ..serializers import CursoSerializer

User = get_user_model()

class TurmaSerializer(serializers.ModelSerializer):
    professor = UserSerializer(read_only=True)
    curso = CursoSerializer(read_only=True)
    alunos = UserSerializer(many=True, read_only=True)

    curso_id = serializers.PrimaryKeyRelatedField(source='curso', queryset=Curso.objects.all(), write_only=True)
    professor_id = serializers.PrimaryKeyRelatedField(source='professor', queryset=User.objects.all(), write_only=True)
    alunos_ids = serializers.PrimaryKeyRelatedField(source='alunos', many=True, queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Turma
        fields = [
            'id', 'nome', 'curso', 'materia', 'professor', 'alunos',
            'curso_id', 'professor_id', 'alunos_ids'
        ]

    def create(self, validated_data):
        alunos = validated_data.pop('alunos', [])
        turma = Turma.objects.create(**validated_data)
        turma.alunos.set(alunos)
        return turma

    def update(self, instance, validated_data):
        alunos = validated_data.pop('alunos', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if alunos is not None:
            instance.alunos.set(alunos)

        instance.save()
        return instance