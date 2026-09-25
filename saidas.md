# Evidências

Este arquivo contém as evidências das Partes 0 a 5.

## Parte 0
Tabela com doc_id, status e número de palavras de cada documento:
```
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
```
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