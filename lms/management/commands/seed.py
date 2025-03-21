import json
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from lms.models import Curso, Aula, Atividade, Turma

User = get_user_model()

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados iniciais'

    def handle(self, *args, **kwargs):
        with open('seed.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

            users = {}
            for user_data in data['users']:
                user = User.objects.create_user_entity(
                    role=user_data['role'],
                    cpf=user_data['cpf'],
                    email=user_data['email'],
                    name=user_data['name'],
                    password=user_data['password']
                )
                users[user.id] = user
            self.stdout.write(self.style.SUCCESS('Usuários criados com sucesso!'))

            cursos = {}
            for curso_data in data['cursos']:
                curso = Curso.objects.create(nome=curso_data['nome'])
                cursos[curso.id] = curso 
            self.stdout.write(self.style.SUCCESS('Cursos criados com sucesso!'))

            aulas = {}
            for aula_data in data['aulas']:
                aula = Aula.objects.create(
                    titulo=aula_data['titulo'],
                    descricao=aula_data['descricao'],
                    conteudo=aula_data['conteudo'],
                )
                aulas[aula.id] = aula 
                
            atividades = {}
            for atividade_data in data['atividades']:
                aula = aulas[atividade_data['aula']]
                atividade = Atividade.objects.create(
                    titulo=atividade_data['titulo'],
                    descricao=atividade_data['descricao'],
                    conteudo=atividade_data['conteudo'],
                    aula=aula,
                    data_entrega=atividade_data['data_entrega']
                )
                atividades[atividade.id] = atividade 
                aula.atividades.add(atividade)
            self.stdout.write(self.style.SUCCESS('Atividades criadas e associadas às aulas com sucesso!'))

            for user in users.values():
                if user.is_student:
                    user.curso = cursos[1]
                    user.save()

                    user.cursos.add(cursos[1])

                elif user.is_teacher:
                    user.cursos.add(cursos[1])

            self.stdout.write(self.style.SUCCESS('Usuários associados a cursos com sucesso!'))

            for turma_data in data['turmas']:
                curso = cursos[turma_data['curso']] 
                professor = users[turma_data['professor']]
                turma = Turma.objects.create(
                    nome=turma_data['nome'],
                    curso=curso,
                    professor=professor,
                    materia=turma_data['materia']
                )
                for aluno_id in turma_data['alunos']:
                    if aluno_id in users:
                        aluno = users[aluno_id]
                        turma.alunos.add(aluno)
                    else:
                        self.stdout.write(self.style.WARNING(f'Aluno com ID {aluno_id} não encontrado.'))
            self.stdout.write(self.style.SUCCESS('Turmas criadas com sucesso!'))