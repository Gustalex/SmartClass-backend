from django.urls import path
from .views import CursoViewSet, CursoLisRetrievetViewSet, AtividadeViewSet, TurmaViewSet, AulaViewSet

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
    # Turma
    path('list-turmas/', TurmaViewSet.as_view({'get':'list_turmas'}), name='list_turmas'),
    path('turmas/<int:pk>/', TurmaViewSet.as_view({'get':'retrieve_turma'}), name='turma'),
    path('create-turma/', TurmaViewSet.as_view({'post':'create_turma'}), name='create_turma'),
    path('turmas/<int:pk>/update/', TurmaViewSet.as_view({'patch':'update_turma'}), name='update_turma'),
    path('turmas/<int:pk>/delete/', TurmaViewSet.as_view({'delete':'delete_turma'}), name='delete_turma'),  
    # Aula
    path('list-aulas/', AulaViewSet.as_view({'get':'list_aulas'}), name='list_aulas'),
    path('aulas/<int:pk>/', AulaViewSet.as_view({'get':'retrieve_aula'}), name='aula'),
    path('create-aula/', AulaViewSet.as_view({'post':'create_aula'}), name='create_aula'),
    path('aulas/<int:pk>/update/', AulaViewSet.as_view({'patch':'update_aula'}), name='update_aula'),
    path('aulas/<int:pk>/delete/', AulaViewSet.as_view({'delete':'delete_aula'}), name='delete_aula'),
]
