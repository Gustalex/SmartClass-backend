from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import Atividade
from ..serializers import AtividadeSerializer
from auth_service.decorators import teacher_required, role_required

class AtividadeViewSet(ViewSet):
    serializer_class = AtividadeSerializer
    authentication_classes = [JWTAuthentication]

    @action(detail=False, methods=['get'])
    @role_required
    def list_atividades(self, request):
        try:
            atividades = Atividade.objects.all()
            serializer = AtividadeSerializer(atividades, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Erro ao listar atividades: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['get'])
    @role_required
    def retrieve_atividade(self, request, pk=None):
        try:
            atividade = Atividade.objects.get(pk=pk)
            serializer = AtividadeSerializer(atividade)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Atividade.DoesNotExist:
            return Response({'error': 'Atividade não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Erro ao recuperar atividade: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'])
    @teacher_required
    def create_atividade(self, request):
        try:
            serializer = AtividadeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Erro ao criar atividade: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        
    
    @action(detail=True, methods=['patch'])
    @teacher_required
    def update_atividade(self, request, pk = None):
        try:
            atividade = Atividade.objects.get(pk=pk)
            serializer = AtividadeSerializer(atividade, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Atividade.DoesNotExist:
            return Response({'error': 'Atividade não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Erro ao atualizar atividade: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        
    
    @action(detail=True, methods=['delete'])
    @teacher_required
    def delete_atividade(self, request, pk = None):
        try:
            atividade = Atividade.objects.get(pk=pk)
            atividade.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Atividade.DoesNotExist:
            return Response({'error': 'Atividade não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Erro ao deletar atividade: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    

    

