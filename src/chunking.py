import pandas as pd

from carregar_corpus import PASTA_INSUMOS, carregar_metadados, carregar_textos


def extrair_secao(parte: str) -> tuple[str, str]:
    """Separa o nome da seção do seu texto completo."""
    nome_secao, texto_secao = parte.strip().split("\n", 1)
    return nome_secao, texto_secao.strip()


def criar_chunks_documento(documento: pd.Series) -> list[dict[str, str]]:
    """Cria os chunks de um documento, ignorando seu cabeçalho."""
    chunks = []
    partes = documento["texto"].split("##")

    for parte in partes[1:]:
        nome_secao, texto_secao = extrair_secao(parte)
        chunks.append({
            "doc_id": documento["doc_id"],
            "titulo": documento["titulo"],
            "secao": nome_secao,
            "status": documento["status"],
            "texto": texto_secao,
        })

    return chunks


def dividir_por_secao(documentos_df: pd.DataFrame) -> pd.DataFrame:
    """Reúne os chunks de todos os documentos em um DataFrame."""
    chunks = []
    for _, documento in documentos_df.iterrows():
        chunks.extend(criar_chunks_documento(documento))

    return pd.DataFrame(chunks, columns=["doc_id", "titulo", "secao", "status", "texto"])


if __name__ == "__main__":
    pasta_corpus = PASTA_INSUMOS / "corpus"
    df = carregar_textos(carregar_metadados(PASTA_INSUMOS), pasta_corpus)

    df_chunks = dividir_por_secao(documentos_df=df)
    print(df_chunks)

    print("\nTotal de chunks:", len(df_chunks))
    print("\nChunks por documento:")
    print(df_chunks.groupby("doc_id").size().rename("numero_chunks").to_string())

    print("\nExemplo completo de chunk:")
    for campo, valor in df_chunks.iloc[0].items():
        print(f"{campo}: {valor}")
