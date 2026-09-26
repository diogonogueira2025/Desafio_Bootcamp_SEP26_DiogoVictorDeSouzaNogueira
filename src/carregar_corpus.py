from pathlib import Path

import pandas as pd

PASTA_INSUMOS = (
    Path(__file__).resolve().parent.parent
    / "insumos_Desafio_Bootcamp_SEP26"
)


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


def carregar_documentos() -> pd.DataFrame:
    """Carrega os metadados e os textos completos do corpus."""
    metadados_df = carregar_metadados(PASTA_INSUMOS)
    return carregar_textos(metadados_df, PASTA_INSUMOS / "corpus")


def gerar_evidencia(documentos_df: pd.DataFrame) -> pd.DataFrame:
    """Reúne status e número de palavras, com doc_id como índice."""
    evidencia_df = documentos_df.copy()
    evidencia_df["numero_palavras"] = evidencia_df["texto"].str.split().str.len()

    return evidencia_df[["doc_id", "status", "numero_palavras"]].set_index("doc_id")


if __name__ == "__main__":
    documentos_df = carregar_documentos()
    evidencia_df = gerar_evidencia(documentos_df)

    print(documentos_df["status"].value_counts())
    print(evidencia_df)
