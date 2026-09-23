# Insumos do Desafio Bootcamp SEP26: corpus sintético "Jornada do Colaborador"

Conteúdo 100% fictício, criado para fins didáticos. A empresa "Horizonte Tech Ltda." não existe. Não há dados pessoais reais.

## Arquivos
- `corpus/` : 12 documentos em Markdown (11 políticas + 1 FAQ). Cada arquivo tem um cabeçalho com doc_id, área, vigência, versão e status, seguido de seções marcadas com `##`.
- `metadados.csv` : uma linha por documento (doc_id, titulo, area_responsavel, vigencia_inicio, versao, status, arquivo). Codificação UTF-8, separador vírgula.
- `perguntas_gabarito.csv` : 10 perguntas de avaliação. 9 têm documento esperado; 1 (P10) não tem resposta no corpus e testa a regra de "não encontrado".

## Armadilhas intencionais
1. POL-004 (revogada) e POL-005 (vigente) tratam do mesmo tema com regras diferentes. O assistente deve responder com a política vigente.
2. FAQ-001 repete informações de outras políticas de forma resumida. Recuperar a FAQ é aceitável se a citação apontar também a política de origem.
3. P10 não tem resposta no corpus.
