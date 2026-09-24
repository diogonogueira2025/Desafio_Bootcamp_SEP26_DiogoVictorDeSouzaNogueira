from pathlib import Path

import pandas as pd


def carregar_metadados(pasta_insumos: Path) -> pd.DataFrame:
    """Lê os metadados dos documentos em um DataFrame."""
    return pd.read_csv(pasta_insumos / "metadados.csv")


def ler_documento(caminho_arquivo: Path) -> str:
    """Lê o texto completo de um documento em UTF-8."""
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


def carregar_textos(metadados_df: pd.DataFrame, pasta_corpus: Path) -> pd.DataFrame:
    """Adiciona os textos a uma cópia dos metadados."""
    textos = []

    for _, documento in metadados_df.iterrows():
        caminho_arquivo = pasta_corpus / documento["arquivo"]
        textos.append(ler_documento(caminho_arquivo))

    documentos_df = metadados_df.copy()
    documentos_df["texto"] = textos

    return documentos_df


def gerar_evidencia(metadados_df: pd.DataFrame) -> pd.DataFrame:
    """Reúne status e número de palavras, com doc_id como índice."""
    evidencia = metadados_df.copy()
    evidencia["numero_palavras"] = evidencia["texto"].str.split().str.len()

    return evidencia[["doc_id", "status", "numero_palavras"]].set_index("doc_id")


if __name__ == "__main__":
    pasta_insumos = Path("../insumos_Desafio_Bootcamp_SEP26")
    pasta_corpus = pasta_insumos / "corpus"

    df = carregar_metadados(pasta_insumos)
    df = carregar_textos(df, pasta_corpus)

    evidencia = gerar_evidencia(df)

    print(df["status"].value_counts())
    print(evidencia)
