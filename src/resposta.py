import pandas as pd

from carregar_corpus import PASTA_INSUMOS
from recuperacao import buscar

THRESHOLD = 0.30
MENSAGEM_NAO_ENCONTRADO = (
    "Não encontrei essa informação nas políticas vigentes. "
    "Procure a área de Pessoas e Cultura."
)


def formatar_saida(
    pergunta: str, resposta: str, fonte: str, score: float, status: str
) -> str:
    """Monta os cinco campos do modelo de saída acessível."""
    return (
        f"PERGUNTA: {pergunta}\n"
        f"RESPOSTA: {resposta}\n"
        f"FONTE: {fonte}\n"
        f"SCORE: {score:.2f}\n"
        f"STATUS: {status}"
    )


def responder(pergunta: str) -> str:
    """Retorna o texto do melhor chunk ou a mensagem de não encontrado."""
    resultados_df = buscar(pergunta, k=1)
    score = float(resultados_df.iloc[0]["score"]) if not resultados_df.empty else 0.0

    if resultados_df.empty or score < THRESHOLD:
        return formatar_saida(pergunta, MENSAGEM_NAO_ENCONTRADO, "nenhuma", score, "nao_encontrado")

    melhor_chunk = resultados_df.iloc[0]
    fonte = (
        f"{melhor_chunk['doc_id']} | {melhor_chunk['titulo']} | "
        f"Seção: {melhor_chunk['secao']}"
    )
    return formatar_saida(pergunta, melhor_chunk["texto"], fonte, score, "encontrado")


if __name__ == "__main__":
    perguntas_df = pd.read_csv(PASTA_INSUMOS / "perguntas_gabarito.csv")
    perguntas_teste_df = perguntas_df.loc[
        perguntas_df["pergunta_id"].isin(["P02", "P10"])
    ]

    for _, pergunta in perguntas_teste_df.iterrows():
        print(responder(pergunta["pergunta"]))
        print()
