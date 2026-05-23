"""Testes unitários para seletores de requisições."""

import pytest

from apps.accounts.models import User
from apps.requisicoes.models import EstadoRequisicao, Requisicao
from apps.requisicoes.selectors import (
    material_eh_elegivel,
    materiais_para_requisicao,
    minhas_requisicoes,
    requisicoes_visiveis_para,
)


@pytest.mark.django_db
def test_materiais_para_requisicao_inclui_disponivel(material_disponivel):
    assert material_disponivel in materiais_para_requisicao()


@pytest.mark.django_db
def test_materiais_para_requisicao_exclui_inativo(material_inativo):
    assert material_inativo not in materiais_para_requisicao()


@pytest.mark.django_db
def test_materiais_para_requisicao_exclui_sem_saldo(material_sem_saldo):
    assert material_sem_saldo not in materiais_para_requisicao()


@pytest.mark.django_db
def test_materiais_para_requisicao_exclui_divergente(material_divergente):
    assert material_divergente not in materiais_para_requisicao()


@pytest.mark.django_db
def test_material_eh_elegivel_true_se_disponivel(material_disponivel):
    assert material_eh_elegivel(material_disponivel)


@pytest.mark.django_db
def test_material_eh_elegivel_false_se_inativo(material_inativo):
    assert not material_eh_elegivel(material_inativo)


@pytest.mark.django_db
def test_material_eh_elegivel_false_se_sem_saldo(material_sem_saldo):
    assert not material_eh_elegivel(material_sem_saldo)


@pytest.mark.django_db
def test_material_eh_elegivel_false_se_divergente(material_divergente):
    assert not material_eh_elegivel(material_divergente)


# ---------------------------------------------------------------------------
# Fixtures de requisições para testes de visibilidade
# ---------------------------------------------------------------------------


@pytest.fixture
def req_solicitante_rascunho(db, solicitante, setor_obras):
    """Rascunho criado pelo solicitante para si."""
    return Requisicao.objects.create(
        estado=EstadoRequisicao.RASCUNHO,
        criador=solicitante,
        beneficiario=solicitante,
        setor_beneficiario=setor_obras,
    )


@pytest.fixture
def req_solicitante_enviada(db, solicitante, setor_obras):
    """Requisição enviada pelo solicitante para si."""
    return Requisicao.objects.create(
        estado=EstadoRequisicao.AGUARDANDO_AUTORIZACAO,
        numero_publico='REQ-2026-0001',
        criador=solicitante,
        beneficiario=solicitante,
        setor_beneficiario=setor_obras,
    )


@pytest.fixture
def req_aux_para_solicitante_rascunho(db, aux_obras, solicitante, setor_obras):
    """Rascunho criado pelo auxiliar em nome do solicitante (beneficiário)."""
    return Requisicao.objects.create(
        estado=EstadoRequisicao.RASCUNHO,
        criador=aux_obras,
        beneficiario=solicitante,
        setor_beneficiario=setor_obras,
    )


@pytest.fixture
def req_aux_para_solicitante_enviada(db, aux_obras, solicitante, setor_obras):
    """Enviada pelo aux em nome do solicitante."""
    return Requisicao.objects.create(
        estado=EstadoRequisicao.AGUARDANDO_AUTORIZACAO,
        numero_publico='REQ-2026-0002',
        criador=aux_obras,
        beneficiario=solicitante,
        setor_beneficiario=setor_obras,
    )


@pytest.fixture
def req_outro_setor(db, usuario_ti, setor_ti):
    """Requisição enviada em outro setor (TI)."""
    return Requisicao.objects.create(
        estado=EstadoRequisicao.AGUARDANDO_AUTORIZACAO,
        numero_publico='REQ-2026-0003',
        criador=usuario_ti,
        beneficiario=usuario_ti,
        setor_beneficiario=setor_ti,
    )


# ---------------------------------------------------------------------------
# requisicoes_visiveis_para — por papel
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_visiveis_solicitante_ve_proprias_como_criador(
    solicitante, req_solicitante_rascunho, req_solicitante_enviada, req_outro_setor
):
    vis = list(requisicoes_visiveis_para(solicitante.pk))
    assert req_solicitante_rascunho in vis
    assert req_solicitante_enviada in vis
    assert req_outro_setor not in vis


@pytest.mark.django_db
def test_visiveis_solicitante_nao_ve_rascunho_de_terceiro_onde_eh_beneficiario(
    solicitante, req_aux_para_solicitante_rascunho
):
    vis = list(requisicoes_visiveis_para(solicitante.pk))
    assert req_aux_para_solicitante_rascunho not in vis


@pytest.mark.django_db
def test_visiveis_solicitante_ve_enviada_onde_eh_beneficiario(
    solicitante, req_aux_para_solicitante_enviada
):
    vis = list(requisicoes_visiveis_para(solicitante.pk))
    assert req_aux_para_solicitante_enviada in vis


@pytest.mark.django_db
def test_visiveis_aux_setor_nao_ve_setor_inteiro(
    aux_obras, req_solicitante_enviada, req_outro_setor
):
    vis = list(requisicoes_visiveis_para(aux_obras.pk))
    assert req_solicitante_enviada not in vis
    assert req_outro_setor not in vis


@pytest.mark.django_db
def test_visiveis_chefe_setor_ve_setor_exceto_rascunho_de_terceiro(
    chefe_obras,
    req_solicitante_rascunho,
    req_solicitante_enviada,
    req_outro_setor,
):
    vis = list(requisicoes_visiveis_para(chefe_obras.pk))
    assert req_solicitante_enviada in vis
    assert req_solicitante_rascunho not in vis
    assert req_outro_setor not in vis


@pytest.mark.django_db
def test_visiveis_aux_almox_ve_todas_exceto_rascunho_de_terceiro(
    aux_almoxarifado,
    req_solicitante_rascunho,
    req_solicitante_enviada,
    req_outro_setor,
):
    vis = list(requisicoes_visiveis_para(aux_almoxarifado.pk))
    assert req_solicitante_enviada in vis
    assert req_outro_setor in vis
    assert req_solicitante_rascunho not in vis


@pytest.mark.django_db
def test_visiveis_chefe_almox_ve_todas_exceto_rascunho_de_terceiro(
    chefe_almoxarifado,
    req_solicitante_rascunho,
    req_solicitante_enviada,
    req_outro_setor,
):
    vis = list(requisicoes_visiveis_para(chefe_almoxarifado.pk))
    assert req_solicitante_enviada in vis
    assert req_outro_setor in vis
    assert req_solicitante_rascunho not in vis


@pytest.mark.django_db
def test_visiveis_superuser_ve_tudo(
    db,
    setor_obras,
    req_solicitante_rascunho,
    req_solicitante_enviada,
    req_outro_setor,
):
    su = User.objects.create_superuser(
        matricula='999', nome='Super', password='senha', setor=setor_obras
    )
    vis = list(requisicoes_visiveis_para(su.pk))
    assert req_solicitante_rascunho in vis
    assert req_solicitante_enviada in vis
    assert req_outro_setor in vis


@pytest.mark.django_db
def test_visiveis_inativo_vazio(usuario_inativo, req_solicitante_enviada):
    assert list(requisicoes_visiveis_para(usuario_inativo.pk)) == []


@pytest.mark.django_db
def test_visiveis_ator_inexistente_vazio(req_solicitante_enviada):
    assert list(requisicoes_visiveis_para(999999)) == []


# ---------------------------------------------------------------------------
# minhas_requisicoes
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_minhas_inclui_propria_rascunho_e_enviada(
    solicitante, req_solicitante_rascunho, req_solicitante_enviada
):
    minhas = list(minhas_requisicoes(solicitante.pk))
    assert req_solicitante_rascunho in minhas
    assert req_solicitante_enviada in minhas


@pytest.mark.django_db
def test_minhas_inclui_onde_eh_beneficiario_fora_rascunho(
    solicitante, req_aux_para_solicitante_enviada
):
    minhas = list(minhas_requisicoes(solicitante.pk))
    assert req_aux_para_solicitante_enviada in minhas


@pytest.mark.django_db
def test_minhas_exclui_rascunho_de_terceiro_onde_eh_beneficiario(
    solicitante, req_aux_para_solicitante_rascunho
):
    minhas = list(minhas_requisicoes(solicitante.pk))
    assert req_aux_para_solicitante_rascunho not in minhas


@pytest.mark.django_db
def test_minhas_chefe_setor_nao_inclui_terceiros_do_setor(
    chefe_obras, req_solicitante_enviada
):
    minhas = list(minhas_requisicoes(chefe_obras.pk))
    assert req_solicitante_enviada not in minhas


@pytest.mark.django_db
def test_minhas_ordenadas_por_criado_em_desc(
    solicitante, req_solicitante_rascunho, req_solicitante_enviada
):
    minhas = list(minhas_requisicoes(solicitante.pk))
    assert minhas[0].criado_em >= minhas[-1].criado_em
