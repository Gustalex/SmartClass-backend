from django.urls import path
from .views import CursoViewSet, CursoLisRetrievetViewSet, AtividadeViewSet

urlpatterns = [
    # Curso
    path('list-cursos/', CursoLisRetrievetViewSet.as_view({'get':'list_cursos'}), name='list_cursos'),
    path('cursos/<int:pk>/', CursoLisRetrievetViewSet.as_view({'get':'retrieve_curso'}), name='curso'),
    path('create-curso/', CursoViewSet.as_view({'post':'create_curso'}), name='create_curso'),
    path('cursos/<int:pk>/update/', CursoViewSet.as_view({'patch':'update_curso'}), name='update_curso'),
    path('cursos/<int:pk>/delete/', CursoViewSet.as_view({'delete':'delete_curso'}), name='delete_curso'),
    # Atividade
    path('list-atividades/', AtividadeViewSet.as_view({'get':'list_atividades'}), name='list_atividades'),
    path('atividades/<int:pk>/', AtividadeViewSet.as_view({'get':'retrieve_atividade'}), name='atividade'),
    path('create-atividade/', AtividadeViewSet.as_view({'post':'create_atividade'}), name='create_atividade'),
    path('atividades/<int:pk>/update/', AtividadeViewSet.as_view({'patch':'update_atividade'}), name='update_atividade'),
    path('atividades/<int:pk>/delete/', AtividadeViewSet.as_view({'delete':'delete_atividade'}), name='delete_atividade'),
]
