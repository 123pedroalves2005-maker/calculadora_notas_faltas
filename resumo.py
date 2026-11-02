from rich.console import Console
from rich.markup import escape
from rich.table import Table

NOTA_APROVACAO = 60.0
FALTAS_POR_AULA = 2


# ---------- Lógica (sem print, para poder ser testada) ----------

def formatar_numero(valor):
    """68.0 -> '68'   7.5 -> '7,5'"""
    return f"{valor:g}".replace(".", ",")


def reprovado_por_falta(max_faltas, faltas):
    return faltas > max_faltas


def aulas_restantes(max_faltas, faltas):
    """Quantas aulas ainda dá para faltar (cada aula custa FALTAS_POR_AULA faltas)."""
    if reprovado_por_falta(max_faltas, faltas):
        return 0
    return (max_faltas - faltas) // FALTAS_POR_AULA


def situacao_notas(notas, total_provas):
    """Devolve (tipo, texto): tipo é 'ok', 'ruim' ou 'falta'."""
    soma = sum(notas)
    if soma >= NOTA_APROVACAO:
        return "ok", "APROVADO"
    if len(notas) >= total_provas:
        return "ruim", "REPROVADO"
    faltam = formatar_numero(NOTA_APROVACAO - soma)
    return "falta", f"precisa de {faltam} na P{len(notas) + 1}"


def aviso_faltas(max_faltas, faltas):
    """Devolve o texto do aviso, ou '' se não há nada a avisar."""
    if reprovado_por_falta(max_faltas, faltas):
        return "REPROVADO POR FALTA"
    aulas = aulas_restantes(max_faltas, faltas)
    if aulas == 0:
        return "CUIDADO: não pode faltar mais nenhuma aula"
    if aulas == 1:
        return "CUIDADO: só pode faltar mais 1 aula"
    return ""


# ---------- Apresentação (cores com rich) ----------

COR_SITUACAO = {"ok": "green", "ruim": "red", "falta": "yellow"}


def imprimir_resumo(materias, console=None):
    # highlight=False: sem isso o rich pinta todo número sozinho (ciano/amarelo)
    console = console or Console(highlight=False)

    tabela = Table(title="RESUMO DO SEMESTRE", title_style="bold", header_style="bold")
    tabela.add_column("Matéria")
    tabela.add_column("Nota", justify="right")
    tabela.add_column("Faltas", justify="right")
    tabela.add_column("Situação")
    tabela.add_column("Aviso")

    for m in materias:
        tipo, situacao = situacao_notas(m["notas"], m["total_provas"])
        cor = COR_SITUACAO[tipo]
        aviso = aviso_faltas(m["max_faltas"], m["faltas"])

        tabela.add_row(
            escape(m["nome"]),  # escape: um "[" no nome não vira marcação do rich
            formatar_numero(sum(m["notas"])),
            f"{m['faltas']}/{m['max_faltas']}",
            f"[{cor}]{situacao}[/{cor}]",
            f"[bold red]{aviso}[/bold red]" if aviso else "",
        )

    console.print(tabela)


if __name__ == "__main__":
    materias = [
        {"nome": "Cálculo I",  "max_faltas": 18, "faltas": 4,  "total_provas": 3, "notas": [30.0, 38.0]},
        {"nome": "Algoritmos", "max_faltas": 18, "faltas": 9,  "total_provas": 3, "notas": [25.0, 27.0]},
        {"nome": "Física I",   "max_faltas": 18, "faltas": 17, "total_provas": 3, "notas": [40.0, 41.0]},
    ]
    imprimir_resumo(materias)