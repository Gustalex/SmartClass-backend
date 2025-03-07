from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from lms.models import Curso

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=True)
    curso = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), required=False)
    cursos = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), many=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'name', 'cpf', 'email', 'role', 'password', 'is_student', 'is_teacher', 'is_manager', 'curso', 'cursos', 'created_at', 'updated_at')

    def validate(self, data):
        role = data.get('role')
        curso = data.get('curso')
        cursos = data.get('cursos')

        if 'role' in data:
            if (role == 'student' or role is None) and not curso:
                raise serializers.ValidationError("O campo 'curso' é obrigatório para alunos.")

            if role == 'teacher' and not cursos:
                raise serializers.ValidationError("O campo 'cursos' é obrigatório para professores.")

            if role == 'student' and cursos:
                raise serializers.ValidationError("Alunos não podem estar associados a múltiplos cursos. Use o campo 'curso'.")

            if role == 'teacher' and curso:
                raise serializers.ValidationError("Use o campo 'cursos'.")

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.pop('role', None)
        curso = validated_data.pop('curso', None)
        cursos = validated_data.pop('cursos', [])

        user = User.objects.create_user_entity(
            role=role,
            password=password,
            curso=curso,  
            cursos=cursos, 
            **validated_data
        )
        return user
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.cpf = validated_data.get('cpf', instance.cpf)

        role = validated_data.get('role')
        if role is not None:
            instance.is_student = False
            instance.is_teacher = False
            instance.is_manager = False

            if role == 'student' or role is None:
                instance.is_student = True
                instance.curso = validated_data.get('curso', instance.curso)
                instance.cursos.clear()
            elif role == 'teacher':
                instance.is_teacher = True
                instance.curso = None  
                instance.cursos.set(validated_data.get('cursos', instance.cursos.all()))
            elif role == 'manager':
                instance.is_manager = True
                instance.curso = None  
                instance.cursos.clear()  

        instance.save()
        return instance
    
class LoginSerializer(serializers.Serializer):
    cpf = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(cpf=attrs['cpf'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Incorrect credentials')
        return {'user': user}

    