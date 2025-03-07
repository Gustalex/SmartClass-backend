from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from auth_service.decorators import manager_required
from ..serializers import CursoSerializer
from ..models import Curso

class CursoLisRetrievetViewSet(ViewSet):
    serializer_class = CursoSerializer

    @action(detail=False, methods=['get'])
    def list_cursos(self, request):
        try:
            cursos = Curso.objects.all()
            serializer = CursoSerializer(cursos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def retrieve_curso(self, request, pk=None):
        try:
            curso = Curso.objects.get(pk=pk)
            serializer = CursoSerializer(curso)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Curso.DoesNotExist:
            return Response({'error': 'Curso not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CursoViewSet(ViewSet):
    serializer_class = CursoSerializer
    authentication_classes = [JWTAuthentication]

    @action(detail=True, methods=['delete'])
    @manager_required
    def create_curso(self, request):
        try:
            curso_nome = request.data.get('nome')
            curso_materias = request.data.get('materias')
            curso = Curso.objects.create(nome=curso_nome)
            curso.materias.set(curso_materias)
            serializer = CursoSerializer(curso)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['delete'])
    @manager_required
    def delete_curso(self, request, pk=None):
        try:
            curso = Curso.objects.get(pk=pk)
            curso.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Curso.DoesNotExist:
            return Response({'error': 'Curso not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
    
    
    @action(detail=True, methods=['patch'])
    @manager_required
    def update_curso(self, request, pk=None):
        try:
            curso = Curso.objects.get(pk=pk)
            serializer = CursoSerializer(curso, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Curso.DoesNotExist:
            return Response({'error': 'Curso not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

