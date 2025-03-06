from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'cpf', 'email', 'role', 'password', 'is_student', 'is_teacher', 'is_manager', 'created_at', 'updated_at')

    def validate_role(self, value):
        if value not in ['student', 'teacher', 'manager', None]:
            raise serializers.ValidationError("Invalid role. Must be one of: student, teacher, manager")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.pop('role', None)
        cpf = validated_data.get('cpf')
        email = validated_data.get('email')
        name = validated_data.get('name')
        
        return User.objects.create_user_entity(role, cpf, email, password, name=name)
    
class LoginSerializer(serializers.Serializer):
    cpf = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(cpf=attrs['cpf'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Incorrect credentials')
        return {'user': user}

    