from django.test import TestCase, Client
from agendar_reuniao.models import Agendamento
from django.contrib.auth.models import User


class ScheduleTest(TestCase):

    global registro
    registro = {
        'username': 'test555',
        'password': '123456',
        'name': 'joao',
        'email': 'jj@asb.com',
        'cpf': '1234',
        'tipo_cae': 'Municipal',
        'user_type': 'advisor',
        'nome_cae': 'CAE',
        'cep': '72430107',
        'bairro': 'setor norte',
        'municipio': 'Brasilia',
        'uf': 'DF'
    }

    def setUp(self):
        self.cliente = Client()
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.user.save()
        data = {
            'username': 'test555',
            'password': '123456',
            'name': 'joao',
            'email': 'jj@asb.com',
            'cpf': '1234',
            'tipo_cae': 'Municipal',
            'user_type': 'advisor',
            'nome_cae': 'CAE',
            'cep': '72430107',
            'bairro': 'setor norte',
            'municipio': 'Brasilia',
            'uf': 'DF'
        }

        self.advisor = self.client.post('/registro/', data)
        self.client.force_login(self.user)
        self.agenda = Agendamento.objects.create(
            data='12/08',
            horario='13:00',
            local='gama',
            tema='discussão',
            observacoes='levem lanche',
            nome_cae_schedule='newton')
        self.agenda.save

    def test_index_schedule_post(self):
        data = {
            'date': '22 de janeiro',
            'time': 'dez e vinte',
            'local': 'no parque',
            'note': 'levem lanche'
        }
        # self.response = self.client.post('/agendar-reuniao/', data,
        #                                  follow=True)
        # self.assertEqual(self.data['local'], Agendamento.objects.last().local)
        # self.assertEqual(self.data['time'],
        #                  Agendamento.objects.last().horario)
        # self.assertEqual(data['date'], Agendamento.objects.last().data)
        # self.assertEqual(data['note'],
        #                  Agendamento.objects.last().observacoes)
        # self.assertEqual(self.response.status_code, 200)
        # self.assertTemplateUsed(self.response, 'scheduled.html')

    def test_edit_schedule_get(self):
        response = self.cliente.get('/editar-reuniao/{}/'.format(
            self.agenda.pk))
        self.assertEqual(response.status_code, 302)

    def test_edit_schedule_post(self):
        data = {
            'data': '2/4',
            'horario': '22:00',
            'local': 'parque',
            'observacoes': '2 horas'
        }
        response = self.cliente.post('/editar-reuniao/{}/'.format(
            self.agenda.pk), data)
        self.assertEqual(response.status_code, 302)

    def test_template_indexScheduleMeeting(self):
        response = self.cliente.get('/agendar-reuniao/')
        self.assertTemplateUsed(response, 'Base.html')
        self.assertTemplateUsed(response, 'indexScheduleMeeting.html')
        self.assertEquals(200, response.status_code)

    def test_template_schedules(self):
        response = self.cliente.get('/eventos/')
        self.assertTemplateUsed(response, 'Base.html')
        self.assertTemplateUsed(response, 'schedules.html')
        self.assertEquals(200, response.status_code)

    def test_scheduled(self):
        self.cliente.login(username='testuser', password='12345')
        response = self.cliente.get('/reunioes-agendadas/')
        self.assertTemplateUsed(response, 'Base.html')
        self.assertTemplateUsed(response, 'scheduled.html')
        self.assertEquals(200, response.status_code)

    def test_save(self):
        data = '22/10/2017'
        local = 'teste'
        horario = '22:00'
        tema = 'teste'
        observacoes = 'teste function'
        nome_cae = 'CAE test'
        novo_agendamento = Agendamento()
        novo_agendamento.data = data
        novo_agendamento.local = local
        novo_agendamento.horario = horario
        novo_agendamento.tema = tema
        novo_agendamento.observacoes = observacoes
        novo_agendamento.nome_cae_schedule = nome_cae
        novo_agendamento.save()
        test_agendamento = Agendamento.objects.get(nome_cae_schedule=nome_cae)
        self.assertEquals(data, test_agendamento.data)
        self.assertEquals(local, test_agendamento.local)
        self.assertEquals(horario, test_agendamento.horario)
        self.assertEquals(tema, test_agendamento.tema)
        self.assertEquals(observacoes, test_agendamento.observacoes)
        self.assertEquals(nome_cae, test_agendamento.nome_cae_schedule)

    def test_edit_schedule(self):
        self.cliente.login(username='testuser', password='12345')
        self.assertTemplateUsed('Base.html')
        self.assertTemplateUsed('edit_schedule.html')

    def test_schedule_delete(self):
        self.cliente.login(username='testuser', password='12345')
        self.assertTemplateUsed('Base.html')
        self.assertTemplateUsed('schedule_delete.html')



      
