from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from auth_service.decorators import teacher_required
from ..models import Aula
from ..serializers import AulaSerializer


class AulaViewSet(ViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = AulaSerializer


    @action(detail=False, methods=['post'])
    @teacher_required
    def create_aula(self,request):
        try:
            serializer = AulaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    @action(detail=False, methods=['get'])
    @teacher_required
    def list_aulas(self, request):
        try:
            aulas = Aula.objects.all()
            serializer = AulaSerializer(aulas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    @action(detail=True, methods=['get'])
    @teacher_required
    def retrieve_aula(self, request, pk=None):
        try:
            aula = Aula.objects.get(pk=pk)
            serializer = AulaSerializer(aula)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Aula.DoesNotExist:
            return Response({'error': 'Aula não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=True, methods=['patch'])
    @teacher_required
    def update_aula(self, request, pk=None):
        try:
            aula = Aula.objects.get(pk=pk)
            aula=serializer = AulaSerializer(aula, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Aula.DoesNotExist:
            return Response({'error': 'Aula não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['delete'])
    @teacher_required
    def delete_aula(self, request, pk=None):
        try:
            aula = Aula.objects.get(pk=pk)
            aula.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Aula.DoesNotExist:
            return Response({'error': 'Aula não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
