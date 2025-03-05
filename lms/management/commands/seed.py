import json
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from lms.models import Curso, Materia, Aula, Atividade, Turma

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

            materias = {}
            for materia_data in data['materias']:
                curso = cursos[materia_data['curso']] 
                professor = users[materia_data['professor']]
                materia = Materia.objects.create(
                    nome=materia_data['nome'],
                    carga_horaria=materia_data['carga_horaria'],
                    curso=curso,
                    professor=professor
                )
                materias[materia.id] = materia 

              
                curso.materias.add(materia)
            self.stdout.write(self.style.SUCCESS('Matérias criadas e associadas aos cursos com sucesso!'))

            aulas = {}
            for aula_data in data['aulas']:
                materia = materias[aula_data['materia']] 
                aula = Aula.objects.create(
                    titulo=aula_data['titulo'],
                    descricao=aula_data['descricao'],
                    conteudo=aula_data['conteudo'],
                    materia=materia
                )
                aulas[aula.id] = aula 

                
                materia.aulas.add(aula)
            self.stdout.write(self.style.SUCCESS('Aulas criadas e associadas às matérias com sucesso!'))

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

                    for materia in user.curso.materias.all():
                        user.materias.add(materia)
                elif user.is_teacher:
                    user.cursos.add(cursos[1])

                    for materia in materias.values():
                        if materia.professor == user:
                            user.materias.add(materia)
            self.stdout.write(self.style.SUCCESS('Usuários associados a cursos e matérias com sucesso!'))

            for turma_data in data['turmas']:
                curso = cursos[turma_data['curso']] 
                materia = materias[turma_data['materia']] 
                professor = users[turma_data['professor']]
                turma = Turma.objects.create(
                    nome=turma_data['nome'],
                    curso=curso,
                    materia=materia,
                    professor=professor
                )
                for aluno_id in turma_data['alunos']:
                    if aluno_id in users:
                        aluno = users[aluno_id]
                        turma.alunos.add(aluno)
                    else:
                        self.stdout.write(self.style.WARNING(f'Aluno com ID {aluno_id} não encontrado.'))
            self.stdout.write(self.style.SUCCESS('Turmas criadas com sucesso!'))