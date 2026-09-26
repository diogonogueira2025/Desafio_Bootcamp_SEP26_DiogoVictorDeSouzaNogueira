import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from carregar_corpus import carregar_documentos
from chunking import dividir_por_secao

def criar_indice(chunks_df: pd.DataFrame):
    """Retorna o vetorizador ajustado e a matriz TF-IDF de todos os chunks."""
    vetorizador = TfidfVectorizer(
        lowercase=True,
        strip_accents=None,
        stop_words=None,
    )
    matriz_chunks = vetorizador.fit_transform(chunks_df["texto"])

    return vetorizador, matriz_chunks


if __name__ == "__main__":
    documentos_df = carregar_documentos()
    chunks_df = dividir_por_secao(documentos_df)

    vetorizador, matriz_chunks = criar_indice(chunks_df)
    numero_chunks, tamanho_vocabulario = matriz_chunks.shape

    print(f"Forma da matriz (linhas, colunas): {matriz_chunks.shape}")
    print(f"Número de chunks: {numero_chunks}")
    print(f"Tamanho do vocabulário: {tamanho_vocabulario}")
