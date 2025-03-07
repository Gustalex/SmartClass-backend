from rest_framework import serializers
from ..models import Curso, Materia  

class CursoSerializer(serializers.ModelSerializer):
    materias = serializers.PrimaryKeyRelatedField(queryset=Materia.objects.all(), many=True)

    class Meta:
        model = Curso
        fields = ['id', 'nome', 'materias']

    def update(self, instance, validated_data):
        instance.nome = validated_data.get('nome', instance.nome)

        if 'materias' in validated_data:
            instance.materias.set(validated_data['materias'])

        instance.save()
        return instance
    
