from rest_framework import serializers
from ..models import Aula, Atividade  
from .atividade_serializer import AtividadeSerializer

class AulaSerializer(serializers.ModelSerializer):
    atividades = AtividadeSerializer(many=True, read_only=True)
    atividades_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        write_only=True, 
        queryset=Atividade.objects.all(), 
        source='atividades',
        required=False
        )

    class Meta:
        model = Aula
        fields = ['id', 'titulo', 'descricao', 'conteudo', 'atividades', 'atividades_ids']
    
    def create(self, validated_data):   
        atividades = validated_data.pop('atividades', [])
        aula = Aula.objects.create(**validated_data)
        aula.atividades.set(atividades)
        return aula
    
    def update(self, instance, validated_data):
        atividades = validated_data.pop('atividades', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if atividades is not None:
            instance.atividades.set(atividades)
        instance.save()
        return instance