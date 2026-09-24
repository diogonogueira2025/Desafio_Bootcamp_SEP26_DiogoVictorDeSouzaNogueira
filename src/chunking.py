from carregar_corpus import carregar_metadados, carregar_textos
from pathlib import Path
import pandas as pd

def dividir_por_secao(documentos_df: pd.DataFrame) -> pd.DataFrame:
    chunks = []
    for _, linha in documentos_df.iterrows():
        partes = linha['texto'].split("##")

        for i in range(1, len(partes)):
            divisao = partes[i].strip().split("\n", 1)
            secao = divisao[0]
            texto_secao = divisao[1].strip()

            chunks.append({
                "doc_id": linha["doc_id"],
                "titulo": linha["titulo"],
                "secao": secao,
                "status": linha["status"],
                "texto": texto_secao,
            })
    return pd.DataFrame(chunks, columns=["doc_id", "titulo", "secao", "status", "texto"])


if __name__ == "__main__":
    pasta_insumos = Path("../insumos_Desafio_Bootcamp_SEP26")
    pasta_corpus = pasta_insumos / "corpus"
    df = carregar_textos(carregar_metadados(pasta_insumos), pasta_corpus)

    print(dividir_por_secao(documentos_df=df))
