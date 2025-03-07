from django.urls import path
from .views import CursoViewSet, CursoLisRetrievetViewSet

urlpatterns = [
    path('list-cursos/', CursoLisRetrievetViewSet.as_view({'get':'list_cursos'}), name='list_cursos'),
    path('cursos/<int:pk>/', CursoLisRetrievetViewSet.as_view({'get':'retrieve_curso'}), name='curso'),
    path('create-curso/', CursoViewSet.as_view({'post':'create_curso'}), name='create_curso'),
    path('cursos/<int:pk>/update/', CursoViewSet.as_view({'patch':'update_curso'}), name='update_curso'),
    path('cursos/<int:pk>/delete/', CursoViewSet.as_view({'delete':'delete_curso'}), name='delete_curso'),
]
