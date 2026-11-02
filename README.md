# Calculadora de Notas e Faltas

Programa de terminal, em Python, para acompanhar o semestre da faculdade: guarda as
matérias, soma as notas, calcula quanto falta para passar e avisa quando as faltas
estão perto do limite.

Feito como projeto de aprendizado, seguindo as regras da minha própria faculdade.

## Regras usadas

- **Aprovação por soma**, não por média: a matéria é aprovada com **60 pontos ou mais**
  somando as provas, sem pesos.
- Cada matéria tem um **número máximo de faltas**. Passou do máximo, reprova por falta.
- **Cada aula faltada conta como 2 faltas** (as aulas têm sempre 2 horários).

Se a regra da sua faculdade for diferente, mude as constantes no topo do `resumo.py`:

```python
NOTA_APROVACAO = 60.0
FALTAS_POR_AULA = 2
```

## O que o programa faz

- Cadastra matérias (nome, máximo de faltas, faltas atuais, quantidade de provas e notas).
- Mostra um resumo do semestre em tabela colorida, com a situação das notas e o aviso de faltas.
- Remove matérias cadastradas por engano.
- **Salva tudo em `materias.json`** a cada mudança, então os dados continuam lá quando você
  fecha e abre o programa.
- Se o `materias.json` estiver com defeito, o programa avisa e guarda uma cópia em
  `materias.json.bak` antes de continuar.

Exemplo do resumo:

```text
┌───────────────────┬───────┬────────┬────────────────────────┬────────────────────────────────────────────┐
│ Matéria           │  Nota │ Faltas │ Situação               │ Aviso                                      │
├───────────────────┼───────┼────────┼────────────────────────┼────────────────────────────────────────────┤
│ Estatística       │ 25,75 │   0/18 │ precisa de 34,25 na P2 │                                            │
│ Física I          │    81 │  17/18 │ APROVADO               │ CUIDADO: não pode faltar mais nenhuma aula │
│ Química           │    30 │  20/18 │ REPROVADO              │ REPROVADO POR FALTA                        │
└───────────────────┴───────┴────────┴────────────────────────┴────────────────────────────────────────────┘
```

## Como usar

Precisa do Python 3 (testado no 3.14). Na pasta do projeto:

```bash
pip install -r requirements.txt
python main.py
```

O menu tem três opções: adicionar matéria, ver o resumo e remover matéria.
Os dados ficam no `materias.json`, criado na primeira vez que você salva uma matéria.

## Testes

```bash
python -m pytest -v
```

Os testes cobrem as contas e os avisos do `resumo.py`: soma de 60 pontos, o cálculo de
aulas restantes (cada uma custa 2 faltas), o limite exato de faltas e a formatação com vírgula.

## Estrutura

| Arquivo | Para que serve |
|---|---|
| `main.py` | Menu, perguntas ao usuário e leitura/gravação do JSON |
| `resumo.py` | Regras de aprovação e faltas, e a tabela do resumo |
| `test_resumo.py` | Testes automáticos das regras |
| `materias.json` | Seus dados (fica só no seu computador, não vai para o GitHub) |

## Limitações conhecidas

- Notas decimais precisam ser digitadas com **ponto** (`7.5`). Com vírgula, o programa
  pede o número de novo.
- Um `materias.json` que seja um JSON válido, mas não uma lista, ainda derruba o programa.
- Não é possível editar uma matéria: para corrigir algo, remova e cadastre de novo.
