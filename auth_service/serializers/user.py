from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'cpf', 'email', 'role', 'is_student', 'is_teacher', 'is_manager', 'created_at', 'updated_at')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def validate_role(self, value):
        if value not in ['student', 'teacher', 'manager']:
            raise serializers.ValidationError("Invalid role. Must be one of: student, teacher, manager")
        return value

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user_entity(role, **validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    cpf = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(cpf=attrs['cpf'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Incorrect credentials')
        return {'user': user}

    