"""Testes da fatia de autenticação por matrícula."""
import pytest
from django.urls import reverse

from apps.accounts.models import User

SENHA = 'senha-forte-123'


@pytest.fixture
def usuario(db):
    return User.objects.create_user(
        matricula='OP-001', password=SENHA, nome='Operador Teste',
    )


def test_get_tela_login(client):
    resposta = client.get(reverse('accounts:login'))
    assert resposta.status_code == 200
    assert 'accounts/login.html' in {t.name for t in resposta.templates}


def test_login_valido_por_matricula(client, usuario):
    resposta = client.post(
        reverse('accounts:login'),
        {'username': 'OP-001', 'password': SENHA},
    )
    assert resposta.status_code == 302
    assert resposta.wsgi_request.user.is_authenticated


def test_login_senha_invalida(client, usuario):
    resposta = client.post(
        reverse('accounts:login'),
        {'username': 'OP-001', 'password': 'errada'},
    )
    assert resposta.status_code == 200
    assert not resposta.wsgi_request.user.is_authenticated


def test_login_usuario_inativo(client, usuario):
    usuario.is_active = False
    usuario.save()
    resposta = client.post(
        reverse('accounts:login'),
        {'username': 'OP-001', 'password': SENHA},
    )
    assert resposta.status_code == 200
    assert not resposta.wsgi_request.user.is_authenticated


def test_logout(client, usuario):
    client.force_login(usuario)
    resposta = client.post(reverse('accounts:logout'))
    assert resposta.status_code == 302
    assert not resposta.wsgi_request.user.is_authenticated
