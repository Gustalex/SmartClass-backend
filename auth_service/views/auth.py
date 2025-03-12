from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import UserSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response({'error': f'Missing required field: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed as e:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       

class LogoutView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        return None

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response("Logout com sucesso.", status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail" : str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RefreshView(generics.GenericAPIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            return Response({
                'access': str(token.access_token),
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail" : str(e)}, status=status.HTTP_400_BAD_REQUEST)