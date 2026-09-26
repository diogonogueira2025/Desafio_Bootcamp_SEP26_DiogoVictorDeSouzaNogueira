import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from carregar_corpus import PASTA_INSUMOS, carregar_metadados, carregar_textos
from chunking import dividir_por_secao

def criar_indice(df_chunks: pd.DataFrame):
    """Retorna o vetorizador ajustado e a matriz TF-IDF de todos os chunks."""
    vetorizador = TfidfVectorizer(
        lowercase=True,
        strip_accents=None,
        stop_words=None,
    )
    matriz_chunks = vetorizador.fit_transform(df_chunks["texto"])

    return vetorizador, matriz_chunks


if __name__ == "__main__":
    metadados_df = carregar_metadados(PASTA_INSUMOS)
    documentos_df = carregar_textos(metadados_df, PASTA_INSUMOS / "corpus")
    df_chunks = dividir_por_secao(documentos_df)

    vetorizador, matriz_chunks = criar_indice(df_chunks)
    numero_chunks, tamanho_vocabulario = matriz_chunks.shape

    print(f"Forma da matriz (linhas, colunas): {matriz_chunks.shape}")
    print(f"Número de chunks: {numero_chunks}")
    print(f"Tamanho do vocabulário: {tamanho_vocabulario}")
