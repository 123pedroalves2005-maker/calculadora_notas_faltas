import pytest

from resumo import (
    aulas_restantes,
    aviso_faltas,
    formatar_numero,
    reprovado_por_falta,
    situacao_notas,
)


# ---------- formatar_numero ----------

def test_inteiro_perde_o_ponto_zero():
    assert formatar_numero(68.0) == "68"


def test_decimal_usa_virgula():
    assert formatar_numero(7.5) == "7,5"


# ---------- faltas ----------

def test_cada_aula_custa_duas_faltas():
    assert aulas_restantes(18, 4) == 7     # (18 - 4) // 2


def test_sobrando_uma_falta_nao_da_para_faltar_aula():
    assert aulas_restantes(18, 17) == 0    # 1 falta sobrando, aula custa 2


def test_exatamente_no_limite_ainda_nao_reprovou():
    assert not reprovado_por_falta(18, 18)
    assert aulas_restantes(18, 18) == 0


def test_passou_do_limite_reprova_por_falta():
    assert reprovado_por_falta(18, 19)
    assert aulas_restantes(18, 19) == 0    # nunca negativo


@pytest.mark.parametrize(
    "max_faltas, faltas, esperado",
    [
        (18, 4, ""),
        (18, 14, ""),                                          # 2 aulas sobrando
        (18, 15, "CUIDADO: só pode faltar mais 1 aula"),
        (18, 17, "CUIDADO: não pode faltar mais nenhuma aula"),
        (18, 18, "CUIDADO: não pode faltar mais nenhuma aula"),
        (18, 19, "REPROVADO POR FALTA"),
    ],
)
def test_aviso_faltas(max_faltas, faltas, esperado):
    assert aviso_faltas(max_faltas, faltas) == esperado


# ---------- notas (regra: SOMA >= 60, sem pesos) ----------

def test_soma_60_exata_aprova():
    assert situacao_notas([30.0, 30.0], 3) == ("ok", "APROVADO")


def test_soma_acima_de_60_aprova_mesmo_com_prova_pendente():
    assert situacao_notas([30.0, 38.0], 3) == ("ok", "APROVADO")


def test_falta_pontos_na_proxima_prova():
    assert situacao_notas([25.0, 27.0], 3) == ("falta", "precisa de 8 na P3")


def test_pontos_quebrados_usam_virgula():
    assert situacao_notas([25.0, 26.5], 3) == ("falta", "precisa de 8,5 na P3")


def test_sem_nenhuma_nota_ainda():
    assert situacao_notas([], 3) == ("falta", "precisa de 60 na P1")


def test_todas_as_provas_feitas_abaixo_de_60_reprova():
    assert situacao_notas([20.0, 20.0, 19.0], 3) == ("ruim", "REPROVADO")