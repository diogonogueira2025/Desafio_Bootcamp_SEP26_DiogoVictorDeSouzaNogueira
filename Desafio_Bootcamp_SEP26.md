# Desafio Bootcamp

## Assistente de Perguntas e Respostas sobre Políticas Internas

**Tema:** Jornada do Colaborador · RAG (Retrieval-Augmented Generation) com recuperação local, sem chave de API

**Programa:** AI/R Fellowship SEP26 · Bootcamp (Fase 1)  
**Encontros:** 22/09/2026 — apresentação · 24/09/2026 — tira-dúvidas, 10:00 às 11:30  
**Entrega:** Até 29/09/2026, 23h59 · prazo único  
**Modalidade:** Individual · envio único via AI/R Learning

---

## 01. Antes de começar

Este desafio usa o que você estudou na Sprint 1 (Python e Pandas) e na Semana 3 (conceitos de LLM, embeddings e RAG). Você vai construir um assistente que responde perguntas de novos colaboradores usando um conjunto de políticas internas de uma empresa fictícia.

Você precisa ter:

- Python 3.10 ou superior instalado.
- As bibliotecas `pandas` e `scikit-learn`. Opcional: `rank_bm25`.
- O pacote de insumos `insumos_Desafio_Bootcamp_SEP26.zip`, disponível na AI/R Learning junto com este documento.

**Tempo estimado de trabalho:** entre 8 e 10 horas ao longo da semana.

### Acessibilidade neste desafio

Toda evidência deve ser apresentada em texto, mesmo que sejam enviadas imagens, vídeos ou capturas de tela.

A saída do seu assistente segue um modelo textual fixo (seção "Modelo de saída acessível"). Esse modelo funciona com leitores de tela e não usa cor para transmitir informação.

Se você precisar de formato alternativo dos insumos (por exemplo, arquivo `.txt` em vez de `.md`) ou de qualquer outro apoio, fale com o SM até 24/09. O pedido não altera o prazo de entrega.

Os documentos do corpus usam títulos reais em Markdown (uma cerquilha para o título e duas cerquilhas para as seções), o que facilita a navegação por leitor de tela e também o chunking.

---

## 02. Glossário rápido

Termos em inglês aparecem em negrito. A explicação está em português.

| Termo | Explicação |
|---|---|
| **RAG (Retrieval-Augmented Generation)** | Técnica em que o sistema primeiro recupera trechos relevantes de documentos e depois monta a resposta com base nesses trechos. Neste desafio, a parte de recuperação é obrigatória e a parte de geração com modelo de linguagem é opcional (Stretch). |
| **Retrieval** | Recuperação. Etapa que busca, em uma coleção de textos, os trechos mais parecidos com a pergunta. |
| **Corpus** | Conjunto de documentos usados como fonte de respostas. Aqui, 12 arquivos de políticas internas. |
| **Chunk / chunking** | Chunk é um pedaço de texto. Chunking é o processo de dividir cada documento em pedaços menores para indexação. |
| **Índice / indexação** | Estrutura que representa cada chunk de forma numérica para permitir busca rápida por similaridade. |
| **TF-IDF (Term Frequency, Inverse Document Frequency)** | Método clássico que representa cada texto por um vetor de pesos de palavras. Palavras frequentes em um chunk e raras no corpus recebem peso alto. |
| **BM25** | Método de ranqueamento por palavras, alternativo ao TF-IDF, muito usado em motores de busca. Opcional neste desafio. |
| **Top-k** | Os `k` resultados mais bem ranqueados. Exemplo: top-3 são os três chunks mais parecidos com a pergunta. |
| **Score de similaridade** | Número que indica quão parecidos são a pergunta e um chunk. Quanto maior, mais parecido. Aqui usamos similaridade do cosseno, que varia de 0 (nada em comum) a 1 (idêntico). |
| **Threshold** | Limiar. Valor mínimo de score abaixo do qual o assistente responde que não encontrou a informação. |
| **Resposta extrativa** | Resposta formada por trechos copiados do próprio documento, sem reescrever. É o modo obrigatório deste desafio. |
| **Ground truth** | Gabarito. Conjunto de perguntas com o documento e a resposta esperados, usado para medir o assistente. |
| **Hit@k** | Métrica que vale 1 quando o documento esperado aparece entre os `k` primeiros resultados, e 0 caso contrário. |
| **Embedding** | Representação numérica de um texto produzida por um modelo de linguagem. Estudado na Semana 3. Não é obrigatório neste desafio; pode ser usado no Stretch. |
| **LLM (Large Language Model)** | Modelo de linguagem de grande porte. Não é obrigatório neste desafio; pode ser usado no Stretch com um modelo local. |

---

## 03. Contexto

A Horizonte Tech Ltda. é uma empresa fictícia. Todo mês ela recebe novos colaboradores. A área de Pessoas e Cultura recebe as mesmas perguntas repetidas vezes: quantos dias posso trabalhar remoto, qual o valor do vale-refeição, como pedir reembolso.

A empresa tem 12 documentos de políticas internas em Markdown. Um deles está revogado e foi substituído por uma versão nova. As duas versões continuam no corpus, como acontece em empresas reais.

Sua tarefa é construir um assistente que recebe uma pergunta em português, encontra o trecho da política que responde à pergunta, devolve esse trecho como resposta e cita o documento e a seção de origem. Quando a informação não existe no corpus, o assistente deve dizer isso de forma clara, em vez de inventar.

Todo o conteúdo do corpus é sintético. Nenhuma regra ali descrita corresponde a uma empresa real.

---

## 04. Onde desenvolver

Você pode usar um notebook Jupyter ou scripts Python (`.py`). Tudo roda na sua máquina. Não é necessária conexão com nenhum serviço externo depois de instalar as bibliotecas.

```bash
pip install pandas scikit-learn

# opcional, apenas se quiser comparar com BM25:
pip install rank_bm25
```

### Modelo de saída acessível

Toda resposta do seu assistente deve ser impressa em texto puro, com exatamente estes cinco campos, nesta ordem e com estes rótulos:

```text
PERGUNTA: Quantos dias por semana posso trabalhar de forma remota?
RESPOSTA: O colaborador pode trabalhar de forma remota em até 3 dias por semana.
Os dias presenciais obrigatórios são terça-feira e quinta-feira.
FONTE: POL-005 | Política de Trabalho Híbrido (versão 2) | Seção: Regra de trabalho remoto
SCORE: 0.61
STATUS: encontrado
```

Quando não houver resposta no corpus:

```text
PERGUNTA: Qual é a política de estacionamento da empresa?
RESPOSTA: Não encontrei essa informação nas políticas vigentes. Procure a área de Pessoas e Cultura.
FONTE: nenhuma
SCORE: 0.07
STATUS: nao_encontrado
```

Os valores de `SCORE` dos exemplos acima são ilustrativos. Os seus dependerão do pré-processamento escolhido.

### Regras do modelo de saída

Os rótulos ficam em maiúsculas; o campo `STATUS` aceita apenas os valores `encontrado` e `nao_encontrado`; não use cores, emojis ou símbolos gráficos para indicar sucesso ou falha.

---

## 05. Atividades

Faça as Partes 0 a 5 em ordem. Cada Parte tem uma evidência textual obrigatória, que deve aparecer no arquivo `saidas.md` da sua entrega.

### P0 — Setup e leitura do corpus

1. Descompacte o pacote de insumos. Confira que existem 12 arquivos na pasta `corpus`, além de `metadados.csv` e `perguntas_gabarito.csv`.
2. Leia `metadados.csv` com pandas. Para cada linha, leia o arquivo Markdown correspondente e guarde o texto completo em uma coluna `texto`.
3. Confirme que a coluna `status` tem exatamente 11 documentos vigentes e 1 revogado.

#### Evidência da Parte 0

Tabela com `doc_id`, `status` e número de palavras de cada documento.

### P1 — Chunking por seção

1. Divida cada documento em chunks usando as seções marcadas com duas cerquilhas (`##`). Cada chunk recebe: `doc_id`, título do documento, nome da seção, `status` e texto da seção.
2. O cabeçalho de cada documento (linha que começa com `Empresa:`) não vira chunk. Ele já está representado em `metadados.csv`.
3. Guarde os chunks em um DataFrame. Conte quantos chunks foram gerados no total e por documento.

#### Evidência da Parte 1

Número total de chunks, número de chunks por documento e um exemplo completo de chunk (todos os campos).

### P2 — Indexação com TF-IDF

1. Use `TfidfVectorizer` do scikit-learn para transformar o texto de todos os chunks em vetores.
2. Decida e documente o pré-processamento: converter para minúsculas é obrigatório; remover acentos e remover stopwords em português são opcionais. Registre a decisão e o motivo em uma frase.
3. Registre o tamanho do vocabulário resultante (número de colunas da matriz).

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vetorizador = TfidfVectorizer(lowercase=True)
matriz_chunks = vetorizador.fit_transform(df_chunks["texto"])
print(matriz_chunks.shape)  # (numero_de_chunks, tamanho_do_vocabulario)
```

#### Evidência da Parte 2

Forma da matriz (linhas por colunas) e a frase que documenta o pré-processamento escolhido.

### P3 — Recuperação top-k com regra de vigência

1. Escreva a função `buscar(pergunta, k=3)`. Ela transforma a pergunta com o mesmo vetorizador, calcula a similaridade do cosseno com todos os chunks e devolve os `k` chunks de maior score, com `doc_id`, seção, `status` e score.
2. Aplique a regra de vigência: por padrão, a função só considera chunks de documentos com `status` igual a `"vigente"`. Documentos revogados ficam fora do ranqueamento.
3. Teste a função com as perguntas P01, P02 e P10 do gabarito e observe o resultado. Na P02, confirme que a POL-004 não aparece.

#### Evidência da Parte 3

Para P01, P02 e P10, a lista dos 3 chunks retornados com `doc_id`, seção e score (duas casas decimais).

### P4 — Resposta extrativa e regra de não encontrado

1. Escreva a função `responder(pergunta)` que chama `buscar`, pega o chunk de maior score e monta a saída no Modelo de saída acessível.
2. A `RESPOSTA` é o texto do chunk de maior score, copiado sem alteração. Não reescreva o texto da política.
3. Defina um threshold. Se o maior score for menor que o threshold, a saída usa `STATUS nao_encontrado` e a mensagem padrão. Documente o valor escolhido e como você chegou nele (por exemplo, olhando os scores das perguntas com e sem resposta).

#### Evidência da Parte 4

O valor do threshold com a justificativa em uma ou duas frases, e a saída completa (cinco campos) para P02 e P10.

### P5 — Avaliação com o gabarito

1. Leia `perguntas_gabarito.csv`. Para cada uma das 10 perguntas, rode `buscar(pergunta, k=3)` e `responder(pergunta)`.
2. Calcule Hit@1 e Hit@3: para cada pergunta com `doc_esperado` diferente de `nao_encontrado`, verifique se o `doc_esperado` é o primeiro resultado (Hit@1) e se está entre os 3 primeiros (Hit@3).
3. Reporte a média das duas métricas sobre as 9 perguntas com resposta.
4. Para a P10, verifique se o `STATUS` devolvido foi `nao_encontrado`. Reporte acerto ou erro.
5. Escolha uma pergunta em que o assistente errou ou ficou perto do threshold e explique, em até 5 linhas, por que isso aconteceu e o que você tentaria para corrigir.

#### Evidência da Parte 5

Tabela com `pergunta_id`, `doc_esperado`, `doc_retornado_1`, `score`, `STATUS` e `acerto` (sim ou não); os valores de Hit@1 e Hit@3; e a análise de erro.

---

## Stretch opcional — Geração com modelo local

Esta parte é opcional. Ela não entra na média. Quem não fizer não perde pontos. Quem não puder instalar um modelo local não é prejudicado.

### Opção A

Substitua a resposta extrativa da Parte 4 por uma resposta gerada por um modelo de linguagem que rode na sua máquina (por exemplo, via Ollama com um modelo aberto de pequeno porte).

O prompt deve receber apenas os chunks recuperados e deve instruir o modelo a responder somente com base neles e a manter a citação da `FONTE`. Nenhuma chave de API é usada.

### Opção B

Compare TF-IDF com BM25 (`rank_bm25`) nas mesmas 10 perguntas e reporte Hit@1 e Hit@3 para os dois métodos, com uma conclusão de até 5 linhas.

**Evidência do Stretch:** mesma estrutura da Parte 5, indicando qual opção foi feita.

---

## 06. Acesso à API Key

Não há chave de API neste desafio. O programa não fornece chave e nenhuma etapa obrigatória exige acesso a serviço de nuvem, plataforma de modelos ou conta em site de terceiros. Todo o processamento obrigatório (Partes 0 a 5) acontece com pandas e scikit-learn na sua máquina.

O Stretch com modelo local também não usa chave. Ele exige apenas instalar um programa e baixar um modelo aberto. Se sua máquina não suportar, escolha a Opção B do Stretch ou não faça o Stretch.

---

## 07. Sugestão de organização

| Dia | O que fazer |
|---|---|
| 22/09 (terça) | Participar da apresentação. Baixar os insumos. Fazer a Parte 0. |
| 23/09 (quarta) | Fazer a Parte 1. Anotar dúvidas para o tira-dúvidas. |
| 24/09 (quinta) | Participar do tira-dúvidas, das 10:00 às 11:30. Fazer a Parte 2. |
| 25/09 (sexta) | Fazer a Parte 3. |
| 26/09 e 27/09 (fim de semana) | Descanso. Se quiser adiantar, fazer a Parte 4. |
| 28/09 (segunda) | Fazer as Partes 4 e 5. Montar o arquivo `saidas.md`. |
| 29/09 (terça) | Escrever a reflexão. Revisar a entrega. Enviar na AI/R Learning antes das 23h59. |

---

## 08. O que entregar

Um único arquivo `.zip` enviado na AI/R Learning, nomeado:

```text
Desafio_Bootcamp_SEP26_SeuNome.zip
```

Contendo:

1. **Código:** um notebook `.ipynb` ou um ou mais arquivos `.py` com as funções `buscar` e `responder`. O código deve rodar do início ao fim sem intervenção.
2. **`saidas.md`:** arquivo de texto com as evidências das Partes 0 a 5, na ordem, com o título de cada Parte. Se fez o Stretch, adicione a seção correspondente no fim.
3. **`reflexao.md`:** arquivo de texto com a reflexão por escrito (veja abaixo).

Não inclua a pasta `corpus` nem os arquivos CSV originais no zip. A banca já tem os insumos.

### Reflexão por escrito

Escreva entre **150 e 300 palavras** respondendo às três perguntas abaixo, em português, em texto corrido ou em tópicos:

1. Por que o assistente precisa citar a `FONTE` e o que aconteceria em uma empresa real se ele respondesse sem citar?
2. Qual foi a decisão mais difícil entre chunking, pré-processamento e threshold, e como você a tomou?
3. Se você tivesse acesso a um LLM, o que mudaria na Parte 4 e que novo risco apareceria?

---

## 09. Regras

- O desafio é individual. Você pode conversar com colegas sobre conceitos, mas o código e os textos entregues devem ser seus.
- Use IA com responsabilidade e de modo assistivo, para um melhor aproveitamento do nosso programa.
- O prazo é único: **29/09/2026, 23h59**. Não há segundo prazo. Envios parciais são aceitos e avaliados pelo que contêm.
- A `RESPOSTA` nas Partes 0 a 5 deve ser extrativa. Reescrever o texto da política com suas palavras nessas Partes conta como não cumprimento da Parte 4.
- Não altere os arquivos do corpus nem o gabarito. Se encontrar um erro nos insumos, registre no `saidas.md` e continue.
- Bibliotecas permitidas nas Partes obrigatórias: pandas, scikit-learn, rank_bm25 e biblioteca padrão do Python. Outras bibliotecas só no Stretch.

---

## 10. Resumo da rubrica

Seis dimensões, cada uma de 1 a 5. A média das seis dimensões é a Nota Técnica do desafio. O Stretch é avaliado à parte.

| Dimensão | 1 (Insuficiente) | 3 (Adequado) | 5 (Exemplar) |
|---|---|---|---|
| **1. Setup e organização do código** | Código não roda ou não lê o corpus completo. | Código roda do início ao fim; leitura dos 12 documentos correta; Evidência da Parte 0 presente. | Além do 3: funções separadas e nomeadas, comentários curtos, nenhuma repetição desnecessária. |
| **2. Chunking** | Chunks não seguem as seções ou perdem campos (`doc_id`, seção, status). | Um chunk por seção, com todos os campos; contagem correta. | Além do 3: cabeçalho excluído dos chunks; exemplo de chunk completo e legível; observação sobre tamanhos. |
| **3. Indexação e recuperação** | `buscar` não funciona ou ignora a regra de vigência. | TF-IDF aplicado; `buscar` devolve top-k com scores; POL-004 excluída do ranqueamento. | Além do 3: pré-processamento documentado com motivo; evidências de P01, P02 e P10 completas e coerentes. |
| **4. Resposta e citação de fonte** | Saída fora do modelo acessível, sem `FONTE` ou com texto reescrito. | Cinco campos corretos; resposta extrativa; `FONTE` com `doc_id` e seção; threshold definido. | Além do 3: threshold justificado com base nos scores observados; P10 tratada corretamente como `nao_encontrado`. |
| **5. Avaliação e métricas** | Sem tabela de avaliação ou métricas incorretas. | Tabela das 10 perguntas; Hit@1 e Hit@3 calculados sobre as 9 perguntas com resposta; P10 verificada. | Além do 3: análise de erro específica, com causa plausível e proposta de correção testável. |
| **6. Reflexão por escrito** | Ausente ou fora do tema. | Responde às três perguntas dentro do limite de palavras. | Além do 3: conecta as decisões técnicas a riscos reais de uso do assistente em uma empresa. |

### Bônus Stretch

Avaliado de 0 a 5, sem somar à média, mas com feedback qualitativo sobre a entrega.

---

## 11. Onde está a maior dificuldade

A parte mais difícil deste desafio não é o código. É definir o threshold. Um valor alto demais faz o assistente dizer que não encontrou informações que existem. Um valor baixo demais faz o assistente responder com um trecho errado quando a pergunta não tem resposta, como na P10. Não existe valor certo de antemão: você precisa olhar os scores das 10 perguntas e escolher com base neles.

A segunda dificuldade é o pré-processamento em português. Palavras como `"quantos"`, `"posso"` e `"qual"` aparecem em quase toda pergunta e podem puxar chunks errados. Testar com e sem stopwords ajuda a entender o efeito.

A terceira é a regra de vigência. Ela parece simples, mas é o que separa um assistente útil de um assistente que dá informação desatualizada com confiança. Em uma empresa real, esse erro tem consequências.

---

## Prazo final

**Entrega até 29/09/2026, 23h59, na AI/R Learning.**

**Prazo único para toda a turma · upload individual**
