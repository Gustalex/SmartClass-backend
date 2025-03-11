from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import Turma
from ..serializers import TurmaSerializer
from auth_service.decorators import teacher_required, role_required

class TurmaViewSet(ViewSet):
    serializer_class = TurmaSerializer
    authentication_classes = [JWTAuthentication]

    @action(detail=False, methods=['post'])
    @teacher_required
    def create_turma(self, request):
        try:
            serializer = TurmaSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Erro ao criar turma: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['get'])
    @role_required
    def list_turmas(sel, request):
        try:
            turmas = Turma.objects.all()
            serializer = TurmaSerializer(turmas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Erro ao listar turmas: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    

    @action(detail=True, methods=['get'])
    @role_required
    def retrieve_turma(self, request, pk=None):
        try:
            turma = Turma.objects.get(pk=pk)
            serializer = TurmaSerializer(turma)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Turma.DoesNotExist:
            return Response({'error': 'Turma não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Erro ao recuperar turma: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        
    
    
    @action(detail=True, methods=['patch'])
    @teacher_required
    def update_turma(self, request, pk=None):
        try:
            turma = Turma.objects.get(pk=pk)
            serializer = TurmaSerializer(turma, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Turma.DoesNotExist:
            return Response({'error': 'Turma não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Erro ao atualizar turma: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    

    @action(detail=True, methods=['delete'])
    @teacher_required
    def delete_turma(self, request, pk=None):
        try:
            turma = Turma.objects.get(pk=pk)
            turma.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Turma.DoesNotExist:
            return Response({'error': 'Turma não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Erro ao deletar turma: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)    
