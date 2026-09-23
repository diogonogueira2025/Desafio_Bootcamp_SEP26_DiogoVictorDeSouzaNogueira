import pandas as pd
from pathlib import Path

#pastas
pasta_insumos = Path("insumos_Desafio_Bootcamp_SEP26")
pasta_corpus = pasta_insumos / "corpus"

# Lendo metadados.csv com pandas
df = pd.read_csv(pasta_insumos / "metadados.csv")

textos = []

for _, linha in df.iterrows():
    caminho_arquivo = pasta_corpus / linha['arquivo']
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        textos.append(arquivo.read())

df["texto"] = textos

# Evidência da parte 0
df["numero_palavras"] = df["texto"].str.split().str.len()
evidencia = df[["doc_id", "status", "numero_palavras"]]

if __name__ == "__main__":
    print(df['status'].value_counts())
    print(evidencia)