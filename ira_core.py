from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

NOTA_APROVACAO = 6.0
FREQUENCIA_MINIMA = 75.0


@dataclass(frozen=True)
class Componente:
    nome: str
    nota: float
    carga_horaria: float
    frequencia: float | None = None


def validar_nota(nota: float) -> None:
    if not 0 <= nota <= 10:
        raise ValueError("A nota deve estar entre 0 e 10.")


def validar_carga_horaria(carga_horaria: float) -> None:
    if carga_horaria <= 0:
        raise ValueError("A carga horária deve ser maior que zero.")


def validar_frequencia(frequencia: float | None) -> None:
    if frequencia is not None and not 0 <= frequencia <= 100:
        raise ValueError("A frequência deve estar entre 0% e 100%.")


def situacao(nota: float, frequencia: float | None = None) -> str:
    validar_nota(nota)
    validar_frequencia(frequencia)

    if frequencia is not None and frequencia < FREQUENCIA_MINIMA:
        return "Reprovado por frequência"
    if nota < NOTA_APROVACAO:
        return "Reprovado por nota"
    if frequencia is None:
        return "Nota suficiente; frequência não informada"
    return "Aprovado"


def pontos_acumulados(componentes: Iterable[Componente]) -> tuple[float, float]:
    soma_ponderada = 0.0
    carga_total = 0.0

    for componente in componentes:
        validar_nota(componente.nota)
        validar_carga_horaria(componente.carga_horaria)
        validar_frequencia(componente.frequencia)
        soma_ponderada += componente.nota * componente.carga_horaria
        carga_total += componente.carga_horaria

    return soma_ponderada, carga_total


def calcular_ira(componentes: Iterable[Componente]) -> float | None:
    soma_ponderada, carga_total = pontos_acumulados(componentes)
    if carga_total == 0:
        return None
    return soma_ponderada / carga_total


def pontos_da_base(ira_atual: float, carga_horaria_atual: float) -> float:
    validar_nota(ira_atual)
    if carga_horaria_atual < 0:
        raise ValueError("A carga horária acumulada não pode ser negativa.")
    return ira_atual * carga_horaria_atual


def calcular_novo_ira(
    ira_atual: float,
    carga_horaria_atual: float,
    nota_nova: float,
    carga_horaria_nova: float,
) -> float:
    validar_nota(nota_nova)
    validar_carga_horaria(carga_horaria_nova)
    pontos = pontos_da_base(ira_atual, carga_horaria_atual)
    nova_carga = carga_horaria_atual + carga_horaria_nova
    return (pontos + nota_nova * carga_horaria_nova) / nova_carga


def calcular_nota_necessaria(
    ira_atual: float,
    carga_horaria_atual: float,
    carga_horaria_nova: float,
    ira_alvo: float,
) -> float:
    validar_nota(ira_alvo)
    validar_carga_horaria(carga_horaria_nova)
    pontos = pontos_da_base(ira_atual, carga_horaria_atual)
    carga_final = carga_horaria_atual + carga_horaria_nova
    return (ira_alvo * carga_final - pontos) / carga_horaria_nova


def calcular_media_necessaria(
    ira_atual: float,
    carga_horaria_atual: float,
    carga_horaria_futura: float,
    ira_alvo: float,
) -> float:
    return calcular_nota_necessaria(
        ira_atual=ira_atual,
        carga_horaria_atual=carga_horaria_atual,
        carga_horaria_nova=carga_horaria_futura,
        ira_alvo=ira_alvo,
    )
