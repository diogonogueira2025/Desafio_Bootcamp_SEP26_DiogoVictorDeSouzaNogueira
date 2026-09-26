from functools import lru_cache

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from carregar_corpus import PASTA_INSUMOS, carregar_metadados, carregar_textos
from chunking import dividir_por_secao
from indexacao import criar_indice

@lru_cache(maxsize=1)
def preparar_busca():
    """Carrega e indexa todos os chunks uma vez, reutilizando-os nas buscas."""
    metadados_df = carregar_metadados(PASTA_INSUMOS)
    documentos_df = carregar_textos(metadados_df, PASTA_INSUMOS / "corpus")
    df_chunks = dividir_por_secao(documentos_df)
    vetorizador, matriz_chunks = criar_indice(df_chunks)
    return df_chunks, vetorizador, matriz_chunks


def calcular_scores(pergunta: str, vetorizador, matriz_chunks):
    """Calcula a similaridade da pergunta com cada chunk do índice."""
    vetor_pergunta = vetorizador.transform([pergunta])
    return cosine_similarity(vetor_pergunta, matriz_chunks).ravel()


def selecionar_top_k_vigentes(
    df_chunks: pd.DataFrame, scores, k: int
) -> pd.DataFrame:
    """Associa os scores e seleciona os melhores chunks após filtrar a vigência."""
    resultados = df_chunks.copy()
    resultados["score"] = scores
    resultados_vigentes = resultados.loc[resultados["status"] == "vigente"]

    return (
        resultados_vigentes
        .sort_values("score", ascending=False, kind="stable")
        .head(k)
        .reset_index(drop=True)
    )


def buscar(pergunta: str, k: int = 3) -> pd.DataFrame:
    """Retorna os k chunks vigentes com maior similaridade com a pergunta."""
    if not isinstance(k, int) or isinstance(k, bool) or k < 1:
        raise ValueError("k deve ser um número inteiro positivo.")

    df_chunks, vetorizador, matriz_chunks = preparar_busca()
    scores = calcular_scores(pergunta, vetorizador, matriz_chunks)
    return selecionar_top_k_vigentes(df_chunks, scores, k)


if __name__ == "__main__":
    perguntas_df = pd.read_csv(PASTA_INSUMOS / "perguntas_gabarito.csv")
    perguntas_teste = perguntas_df.loc[
        perguntas_df["pergunta_id"].isin(["P01", "P02", "P10"])
    ]

    for _, pergunta in perguntas_teste.iterrows():
        resultados = buscar(pergunta["pergunta"], k=3)

        print(f"\n{pergunta['pergunta_id']}: {pergunta['pergunta']}")
        print(resultados[["doc_id", "secao", "status", "score"]].to_string(
            index=False,
            formatters={"score": "{:.2f}".format},
        ))

        if pergunta["pergunta_id"] == "P02":
            assert not resultados["doc_id"].eq("POL-004").any()
            print("Verificação: POL-004 não aparece nos resultados da P02.")
