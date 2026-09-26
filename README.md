# Assistente de Perguntas e Respostas sobre Políticas Internas

Projeto desenvolvido por Diogo Victor de Souza Nogueira para o Desafio Bootcamp SEP26, do programa AI/R Fellowship.

O assistente responde perguntas em português sobre as políticas internas da empresa fictícia Horizonte Tech. A solução usa recuperação local com TF-IDF e similaridade do cosseno, sem LLM ou chave de API.

## Funcionamento

1. Carrega os metadados e os textos dos 12 documentos do corpus.
2. Divide os documentos em 46 chunks, seguindo as seções em Markdown.
3. Indexa os textos com TF-IDF, convertendo para minúsculas e mantendo acentos e stopwords.
4. Recupera os chunks mais semelhantes à pergunta, considerando apenas documentos vigentes.
5. Retorna o texto original do melhor chunk e cita documento, título e seção. Se o score for menor que `0.30`, informa que não encontrou a resposta.

As respostas seguem os campos `PERGUNTA`, `RESPOSTA`, `FONTE`, `SCORE` e `STATUS`, em texto puro. O processamento das perguntas acontece localmente após a preparação do ambiente.

## Requisitos e ambiente

O projeto declara Python **3.14 ou superior**, `pandas>=3.0.6` e `scikit-learn>=1.9.1` no arquivo `pyproject.toml`.

O `uv` gerencia as dependências e o ambiente virtual. Caso ainda não esteja instalado, siga as [instruções oficiais de instalação](https://docs.astral.sh/uv/getting-started/installation/).

Abra um terminal na raiz do projeto, onde estão `pyproject.toml` e `uv.lock`, e execute:

```bash
uv sync
```

Esse comando prepara a pasta `.venv`, que mantém as bibliotecas isoladas do restante do sistema. O `pyproject.toml` declara os requisitos e o `uv.lock` registra as versões resolvidas das dependências. Com `uv run`, não é necessário ativar o ambiente manualmente. Consulte a [documentação de projetos do uv](https://docs.astral.sh/uv/guides/projects/).

## Insumos

Os documentos e CSVs originais não fazem parte do ZIP de entrega. Antes de executar, extraia o pacote fornecido pelo bootcamp para manter esta estrutura na raiz do projeto:

```text
insumos_Desafio_Bootcamp_SEP26/
    corpus/
        ... 12 arquivos Markdown
    metadados.csv
    perguntas_gabarito.csv
src/
pyproject.toml
uv.lock
README.md
saidas.md
```

O caminho dos insumos é definido pela constante `PASTA_INSUMOS` em `src/carregar_corpus.py`. Preserve os nomes e o conteúdo dos arquivos originais.

## Execução

Para executar o fluxo completo de avaliação das dez perguntas do gabarito, a partir da raiz do projeto:

```bash
uv run python src/avaliacao.py
```

O script carrega o corpus, cria os chunks, prepara o índice e chama `buscar` e `responder` para cada pergunta. Ao final, imprime a tabela de avaliação, Hit@1, Hit@3 e a verificação da P10.

Para conferir as evidências de cada etapa separadamente:

```bash
# Parte 0: leitura, status e contagem de palavras
uv run python src/carregar_corpus.py

# Parte 1: contagem de chunks e exemplo completo
uv run python src/chunking.py

# Parte 2: forma da matriz e tamanho do vocabulário
uv run python src/indexacao.py

# Parte 3: top-3 de P01, P02 e P10
uv run python src/recuperacao.py

# Parte 4: respostas completas de P02 e P10
uv run python src/resposta.py

# Parte 5: avaliação das dez perguntas
uv run python src/avaliacao.py
```

Cada script prepara os dados de que precisa; não é necessário executar os anteriores primeiro. As saídas são impressas no terminal, sem atualização automática de `saidas.md`.

## Organização

| Arquivo | Responsabilidade |
|---|---|
| `src/carregar_corpus.py` | Define o caminho dos insumos e carrega metadados e textos. |
| `src/chunking.py` | Divide os documentos em seções e preserva seus metadados. |
| `src/indexacao.py` | Cria o vetorizador e a matriz TF-IDF. |
| `src/recuperacao.py` | Implementa `buscar(pergunta, k=3)` com filtro de vigência. |
| `src/resposta.py` | Implementa `responder(pergunta)`, o threshold e o formato acessível. |
| `src/avaliacao.py` | Avalia as perguntas e calcula as métricas. |
| `saidas.md` | Reúne as evidências das Partes 0 a 5 e a análise de erro. |
| `pyproject.toml` | Declara os requisitos do projeto. |
| `uv.lock` | Registra as versões resolvidas das dependências. |

A reflexão será apresentada em `reflexao.md`, ainda pendente de elaboração.

## Resultados e limitações

Resultados registrados em `saidas.md` para o gabarito fornecido:

| Medida | Resultado |
|---|---|
| Hit@1 nas 9 perguntas com resposta | 100% |
| Hit@3 nas 9 perguntas com resposta | 100% |
| P10, sem resposta no corpus | Acerto: `nao_encontrado` |
| Threshold | `0.30` |

Hit@1 e Hit@3 verificam a presença do documento esperado nos resultados de recuperação, independentemente do threshold. Na tabela de avaliação, `acerto` exige documento correto no primeiro resultado e status `encontrado`; para P10, exige status `nao_encontrado`.

Esses resultados se referem às dez perguntas do gabarito e não garantem o mesmo desempenho em novas perguntas. A recuperação depende das palavras compartilhadas entre pergunta e texto. A P04, por exemplo, teve score de `0.31`, próximo do threshold; a análise desse caso e uma proposta de melhoria estão em `saidas.md`.

## Entrega

O ZIP de entrega deve incluir `src/`, `saidas.md`, `reflexao.md` quando concluído, este README, `pyproject.toml` e `uv.lock`. Não inclua o corpus, os CSVs originais, `.venv`, `.git`, `.idea` ou `__pycache__`.

Nome do arquivo: `Desafio_Bootcamp_SEP26_DiogoVictorDeSouzaNogueira.zip`.
