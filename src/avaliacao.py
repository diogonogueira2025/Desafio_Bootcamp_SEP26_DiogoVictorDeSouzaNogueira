import pandas as pd

from carregar_corpus import PASTA_INSUMOS
from recuperacao import buscar
from resposta import responder


def extrair_status(saida: str) -> str:
    """Extrai o status do último campo do modelo de resposta."""
    return saida.splitlines()[-1].removeprefix("STATUS: ")


def verificar_acerto(doc_esperado: str, status: str, hit_1: bool) -> bool:
    """Verifica o acerto considerando a presença de resposta no gabarito."""
    if doc_esperado == "nao_encontrado":
        return status == "nao_encontrado"
    return hit_1 and status == "encontrado"


def avaliar_pergunta(pergunta: pd.Series) -> dict[str, str | float | bool]:
    """Reúne os resultados de recuperação e resposta de uma pergunta."""
    resultados_df = buscar(pergunta["pergunta"], k=3)
    status = extrair_status(responder(pergunta["pergunta"]))

    documentos_retornados = resultados_df["doc_id"].tolist()
    doc_retornado_1 = documentos_retornados[0] if documentos_retornados else "nenhum"
    score = float(resultados_df.iloc[0]["score"]) if not resultados_df.empty else 0.0
    doc_esperado = pergunta["doc_esperado"]

    hit_1 = doc_retornado_1 == doc_esperado
    hit_3 = doc_esperado in documentos_retornados
    acerto = verificar_acerto(doc_esperado, status, hit_1)

    return {
        "pergunta_id": pergunta["pergunta_id"],
        "doc_esperado": doc_esperado,
        "doc_retornado_1": doc_retornado_1,
        "score": score,
        "STATUS": status,
        "acerto": "sim" if acerto else "não",
        "hit_1": hit_1,
        "hit_3": hit_3,
    }


def avaliar_perguntas() -> pd.DataFrame:
    """Lê o gabarito e reúne as avaliações em um DataFrame."""
    perguntas_df = pd.read_csv(PASTA_INSUMOS / "perguntas_gabarito.csv")
    avaliacoes = [
        avaliar_pergunta(pergunta)
        for _, pergunta in perguntas_df.iterrows()
    ]
    return pd.DataFrame(avaliacoes)


def calcular_metricas(avaliacoes_df: pd.DataFrame) -> tuple[float, float]:
    """Calcula Hit@1 e Hit@3 somente nas perguntas com resposta no corpus."""
    perguntas_com_resposta_df = avaliacoes_df.loc[
        avaliacoes_df["doc_esperado"] != "nao_encontrado"
    ]
    hit_1 = float(perguntas_com_resposta_df["hit_1"].mean())
    hit_3 = float(perguntas_com_resposta_df["hit_3"].mean())
    return hit_1, hit_3


def gerar_evidencia(avaliacoes_df: pd.DataFrame) -> pd.DataFrame:
    """Seleciona os campos exigidos para a tabela da Parte 5."""
    return avaliacoes_df[[
        "pergunta_id", "doc_esperado", "doc_retornado_1", "score", "STATUS", "acerto"
    ]].copy()


if __name__ == "__main__":
    avaliacoes_df = avaliar_perguntas()
    evidencia_df = gerar_evidencia(avaliacoes_df)
    hit_1, hit_3 = calcular_metricas(avaliacoes_df)

    print(evidencia_df.to_string(
        index=False,
        formatters={"score": "{:.2f}".format},
    ))
    print("\nAcerto: documento do primeiro resultado correto e STATUS encontrado; "
          "para P10, STATUS nao_encontrado.")
    print("\nMétricas sobre as perguntas com resposta no corpus:")
    print(f"Hit@1: {hit_1:.2%}")
    print(f"Hit@3: {hit_3:.2%}")

    avaliacao_p10 = avaliacoes_df.loc[avaliacoes_df["pergunta_id"] == "P10"].iloc[0]
    resultado_p10 = "acerto" if avaliacao_p10["STATUS"] == "nao_encontrado" else "erro"
    print(f"P10: {resultado_p10} (STATUS: {avaliacao_p10['STATUS']})")
