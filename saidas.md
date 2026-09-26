# Evidências

Este arquivo contém as evidências das Partes 0 a 5.

## Parte 0

Tabela com doc_id, status e número de palavras de cada documento:
```text
           status  numero_palavras
doc_id                            
POL-001   vigente              164
POL-002   vigente              136
POL-003   vigente              128
POL-004  revogada               90
POL-005   vigente              119
POL-006   vigente              117
POL-007   vigente              114
POL-008   vigente              119
POL-009   vigente              142
POL-010   vigente               92
POL-011   vigente              102
FAQ-001   vigente              145
```

## Parte 1

Número total de chunks, número de chunks por documento e um exemplo completo de chunk (todos os
campos):
```text
Total de chunks: 46

Chunks por documento:
doc_id
FAQ-001    6
POL-001    3
POL-002    4
POL-003    4
POL-004    3
POL-005    3
POL-006    4
POL-007    4
POL-008    4
POL-009    4
POL-010    3
POL-011    4

Exemplo completo de chunk:
doc_id: POL-001
titulo: Política de Onboarding
secao: Objetivo
status: vigente
texto: Esta política define as etapas dos primeiros 30 dias de um novo colaborador na Horizonte Tech.
```

## Parte 2

Converto os textos para minúsculas para uniformizar palavras com diferentes capitalizações e mantenho acentos e stopwords para avaliar uma configuração inicial simples antes de testar outras opções.

```text
Forma da matriz (linhas, colunas): (46, 350)
Número de chunks: 46
Tamanho do vocabulário: 350
```

## Parte 3

Lista dos 3 chunks retornados com doc_id, seção e score (duas casas decimais):
```text
P01: Com quantos dias de antecedência devo solicitar minhas férias?
 doc_id            secao  status score
POL-002   Como solicitar vigente  0.41
POL-002    Venda de dias vigente  0.41
POL-002 Direito a férias vigente  0.25

P02: Quantos dias por semana posso trabalhar de forma remota?
 doc_id                                 secao  status score
POL-005              Regra de trabalho remoto vigente  0.53
FAQ-001 Posso trabalhar remoto todos os dias? vigente  0.20
POL-008                   Entrevista de saída vigente  0.17
Verificação: POL-004 não aparece nos resultados da P02.

P10: Qual é a política de estacionamento da empresa?
 doc_id                        secao  status score
POL-003 Auxílio para trabalho remoto vigente  0.27
POL-008                        Aviso vigente  0.21
POL-001                     Objetivo vigente  0.18
```

## Parte 4

O threshold escolhido foi de `0.30` porque a pergunta sem resposta (P10) teve score de `0.27`, enquanto P01 e P02, com resposta, tiveram `0.41` e `0.53`. Assim, o assistente rejeita a P10 e mantém as respostas de P01 e P02.

```text
PERGUNTA: Quantos dias por semana posso trabalhar de forma remota?
RESPOSTA: O colaborador pode trabalhar de forma remota em até 3 dias por semana. Os dias presenciais obrigatórios são terça-feira e quinta-feira.
FONTE: POL-005 | Política de Trabalho Híbrido (versão 2) | Seção: Regra de trabalho remoto
SCORE: 0.53
STATUS: encontrado

PERGUNTA: Qual é a política de estacionamento da empresa?
RESPOSTA: Não encontrei essa informação nas políticas vigentes. Procure a área de Pessoas e Cultura.
FONTE: nenhuma
SCORE: 0.27
STATUS: nao_encontrado
```
