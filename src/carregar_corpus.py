import pandas as pd
from pathlib import Path

# Retorna um dataframe de metadados.csv
def carregar_metadados(pasta_insumos: Path) -> pd.DataFrame:
    return pd.read_csv(pasta_insumos / "metadados.csv")

# Retorna um dataframe de metadados.csv com a coluna 'texto' contendo o texto de cada arquivo
def carregar_textos(metadados_df: pd.DataFrame, pasta_corpus: Path) -> pd.DataFrame:
    textos = []

    for _, linha in metadados_df.iterrows():
        caminho_arquivo = pasta_corpus / linha["arquivo"]
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            textos.append(arquivo.read())

    metadados_df = metadados_df.copy()
    metadados_df["texto"] = textos

    return metadados_df

# Retorna status e número de palavras por documento, com doc_id como índice.
def gerar_evidencia(metadados_df: pd.DataFrame) -> pd.DataFrame:
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