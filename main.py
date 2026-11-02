import json
import shutil
from pathlib import Path

from resumo import imprimir_resumo

# O arquivo fica na mesma pasta deste script, não importa de onde você o execute
ARQUIVO = Path(__file__).parent / "materias.json"


def carregar_materias():
    if not ARQUIVO.exists():
        return []
    try:
        with open(ARQUIVO, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        backup = ARQUIVO.with_name(ARQUIVO.name + ".bak")
        shutil.copy(ARQUIVO, backup)
        print(f"O arquivo {ARQUIVO.name} está com defeito. Cópia guardada em {backup.name}.")
        return []


def salvar_materias(materias):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(materias, f, ensure_ascii=False, indent=2)


def ler_numero(pergunta, erro, minimo, maximo=None, tipo=int):
    while True:
        try:
            valor = tipo(input(pergunta))
        except ValueError:
            print("Digite apenas números.")
            continue
        if minimo <= valor and (maximo is None or valor <= maximo):
            return valor
        print(erro)


def ler_materia():
    """Pergunta os dados de uma matéria e devolve um dicionário."""
    nome = input("Qual é a matéria? ")
    max_faltas = ler_numero("Pode ter no máximo quantas faltas? ",
                            "O número máximo de faltas não pode ser negativo.", 0)
    faltas = ler_numero("Quantas faltas você já tem? ",
                        "O número de faltas não pode ser negativo.", 0)
    total_provas = ler_numero("Quantidade de provas da matéria: ",
                              "A matéria precisa ter pelo menos 1 prova.", 1)
    provas_feitas = ler_numero("Quantas provas você já fez? ",
                               f"Digite um número de 0 a {total_provas}.", 0, total_provas)

    notas = []
    for i in range(provas_feitas):
        nota = ler_numero(f"Nota da P{i + 1}: ",
                          "A nota não pode ser negativa.", 0, tipo=float)
        notas.append(nota)

    return {
        "nome": nome,
        "max_faltas": max_faltas,
        "faltas": faltas,
        "total_provas": total_provas,
        "notas": notas,
    }


def remover_materia(materias):
    print()
    for i, m in enumerate(materias, start=1):
        print(f"{i} - {m['nome']}")
    escolha = ler_numero("Qual remover? (0 cancela) ",
                         f"Digite um número de 0 a {len(materias)}.", 0, len(materias))
    if escolha == 0:
        return False
    removida = materias.pop(escolha - 1)
    print(f"{removida['nome']} removida.")
    return True


def main():
    materias = carregar_materias()

    print("=== Calculadora de Notas e Faltas ===")
    if materias:
        print(f"{len(materias)} matéria(s) carregada(s) de {ARQUIVO.name}.")

    while True:
        print("\n1 - Adicionar matéria")
        print("2 - Ver resumo do semestre")
        print("3 - Remover matéria")
        print("0 - Sair")
        opcao = ler_numero("Escolha: ", "Digite 0, 1, 2 ou 3.", 0, 3)

        if opcao == 1:
            materias.append(ler_materia())
            salvar_materias(materias)
            print("Matéria adicionada e salva!")
        elif opcao == 2:
            if materias:
                print()
                imprimir_resumo(materias)
            else:
                print("Nenhuma matéria cadastrada ainda.")
        elif opcao == 3:
            if not materias:
                print("Nenhuma matéria para remover.")
            elif remover_materia(materias):
                salvar_materias(materias)
        else:
            break


if __name__ == "__main__":
    main()