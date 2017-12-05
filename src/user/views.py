from .models import Advisor, President, Administrator
from django.contrib.auth.models import User, Permission
from django.contrib.auth import login as django_login, authenticate
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from user.forms import AdvisorForm, AdministratorForm
from user.forms import PresidentForm, ConfirmUserForm
import smtplib
from random import choice
import re
from django.forms import modelformset_factory
# from nuvem_civica.services import postUser


def password_sucess(request):
    return render(request, 'password_sucess.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        usuario_id = request.user.id
        user = User.objects.get(id=usuario_id)
        new_password = request.POST['password']
        new_password_confirm = request.POST['password_confirmation']

        if new_password == new_password_confirm:
            user.set_password(request.POST['password'])
            user.save()
            django_logout(request)
            return render(request, 'password_sucess.html')
        else:
            mensagem = 'Senhas incorretas!'
            return render(request, 'change_password.html', {
                'mensagem': mensagem
            })
        return render(request, 'password_sucess.html')
    return render(request, 'change_password.html')


def reset_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        passwordtmp = ''
        caracters = '0123456789abcdefghijlmnopqrstuwvxz'
        try:
            mensagem1 = 'Solicitação realizada com sucesso!'
            mensagem2 = 'Uma nova senha foi enviada para o email:'
            mensagem = mensagem1 + mensagem2
            usuario = Advisor.objects.get(email=email)
            user = User.objects.get(username=usuario.name)
            for char in range(6):
                passwordtmp += choice(caracters)

            user.set_password(passwordtmp)
            user.save()
            content1 = 'Essa e sua senha temporaria'
            content2 = 'para acessar seu perfil ' + passwordtmp
            content = content1 + content2
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('fiscaeinfo@gmail.com', 'fiscae2017')
            mail.sendmail('fiscaeinfo@gmail.com', email, content)
            return render(request, 'sucess_reset_password.html', {
                'usuario': usuario,
                'mensagem': mensagem
            })
        except:
            mensagem = 'O email digitado não está cadastrado!'
            return render(request, 'sucess_reset_password.html', {
                'mensagem': mensagem
            })
    return render(request, 'reset_password.html')


def login(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password'])
        if user is not None:
            if user.is_active:
                django_login(request, user)
                return HttpResponseRedirect(reverse('index'))
        else:
            error = 'Login inválido!'
            context = {'error': error}
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')


def logout(request):
    if request.user.is_authenticated:
        django_logout(request)
        return HttpResponseRedirect(reverse('index'))


def setAdvisorPerm(user):
    content_type = ContentType.objects.get_for_model(Advisor)
    fill_checklist_perm = Permission.objects.get(codename='fill_checklist',
                                                 content_type=content_type)
    user.user_permissions.add(fill_checklist_perm)


def setPresidentPerm(user):
    content_type = ContentType.objects.get_for_model(President)
    add_advisor_perm = Permission.objects.get(codename='add_advisor',
                                              content_type=content_type)
    remove_advisor_perm = Permission.objects.get(codename='remove_advisor',
                                                 content_type=content_type)
    user.user_permissions.add(add_advisor_perm)
    user.user_permissions.add(remove_advisor_perm)


def setAdministratorPerm(user):
    content_type = ContentType.objects.get_for_model(Administrator)
    add_president_perm = Permission.objects.get(codename='add_president',
                                                content_type=content_type)
    remove_president_perm = Permission.objects.get(codename='remove_president',
                                                   content_type=content_type)
    add_advisor_perm = Permission.objects.get(codename='add_advisor',
                                              content_type=content_type)
    remove_advisor_perm = Permission.objects.get(codename='remove_advisor',
                                                 content_type=content_type)
    user.user_permissions.add(add_president_perm)
    user.user_permissions.add(remove_president_perm)
    user.user_permissions.add(add_advisor_perm)
    user.user_permissions.add(remove_advisor_perm)


def user_type(request, user):
    user_type = request.POST['user_type']
    if(user_type == "advisor"):
        person = Advisor()
        setAdvisorPerm(user)
        User.objects.filter(pk=user.id).update(is_active=False)
    elif(user_type == "president"):
        person = President()
        setPresidentPerm(user)
    elif(user_type == "administrator"):
        person = Administrator()
        setAdministratorPerm(user)
    person.user = user
    return person


def register(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = User.objects.create_user(username=username,
                                            password=password)
            person = user_type(request, user)
        except:
            error = 'Registro inválido!'
            context = {'error': error}
            user.delete()
            return render(request, 'registro.html', context)
        person.name = request.POST['name']
        person.email = request.POST['email']
        person.cpf = request.POST['cpf']
        person.cep = request.POST['cep']
        person.bairro = request.POST['bairro']
        person.municipio = request.POST['municipio']
        person.uf = request.POST['uf']
        cep = re.sub(u'[- A-Z a-z]', '', person.cep)
        person.cep = cep
        if(person.tipo_cae == 'Municipal'):
            person.nome_cae = 'CAE'+' '+person.tipo_cae+' '+person.municipio
        else:
            person.nome_cae = 'CAE'+' '+person.tipo_cae+' '+person.uf
        person.save()
        # Deixar comentado
        """response = postUser(
                        advisor.cep,
                        advisor.email,
                        advisor.name,
                        username,
                        password
                    )
        print(response.status_code, response.reason)"""
        return render(request, 'login.html')
    else:
        return render(request, 'registro.html')


@login_required
@permission_required('user.remove_advisor')
def userDelete(request, pk):
    if request.method == 'POST':
        Advisor.objects.filter(id=pk).delete()
        User.objects.filter(id=pk).delete()
        django_logout(request)
        return render(request, 'index.html')
    return render(request, 'userDelete.html')


@login_required
def index(request):
    advisor = Advisor.objects.get(user=request.user)
    return render(request, 'checklist/templates/index.html', {
        'advisor': advisor
    })


@login_required
def userEdit(request, pk):
    id = pk
    user = get_object_or_404(Advisor, pk=pk)
    form = AdvisorForm(request.POST or None, instance=user)
    if request.method == 'POST':
        if pk == user.id:
            form.save()
            return redirect('../../')
    return render(request, 'userEdit.html', {'form': form, 'id': id})


@login_required
@permission_required('user.president')
def listRequests(request):
    presidents = President.objects.all()
    presidents_ids = presidents.values_list('advisor_ptr_id', flat=True)
    advisors = Advisor.objects.all().exclude(person_ptr_id__in=presidents_ids)
    advisors_id = advisors.values_list('user_id', flat=True)
    users = User.objects.filter(id__in=advisors_id, is_active=False)

    if users is None:
        context = {'avisors': 'None'}
        return render(request, 'listRequests.html', context)

    else:
        UserFormSet = modelformset_factory(User, form=ConfirmUserForm, extra=0)
        if request.method == 'POST':
            formset = UserFormSet(request.POST, queryset=users)
            if formset.is_valid():
                print('\n', 'aaaaaaaah', '\n')
                formset.save()
                return HttpResponseRedirect(reverse('index'))

        else:
            formset = UserFormSet(queryset=users)

        context = {'formset': formset}
    return render(request, 'listRequests.html', context)


def addAdmin(request):
    if request.method == 'POST':
        form = AdministratorForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
    else:
        form = AdministratorForm()
    return render(request, 'addAdmin.html', {'form': form})


def addPresident(request):
    if request.method == 'POST':
        form = PresidentForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
    else:
        form = PresidentForm()
    return render(request, 'addPresident.html', {'form': form})