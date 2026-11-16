import calendar
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, TypedDict

from sqlalchemy import func
from sqlalchemy.orm import Session

from models import CalculoFinanceiro, ContaBancaria, FluxoDinheiro


ZERO = Decimal("0.00")


class ResumoFinanceiro(TypedDict):
    conta_bancaria_id: int
    data_inicio: date
    data_fim: date
    saldo_inicial: Decimal
    total_entradas: Decimal
    total_saidas: Decimal
    total_investimentos: Decimal
    total_transferencias_recebidas: Decimal
    total_transferencias_enviadas: Decimal
    total_ajustes: Decimal
    saldo_final: Decimal


def _soma_movimentacoes(db: Session, *filtros) -> Decimal:
    resultado = (
        db.query(func.coalesce(func.sum(FluxoDinheiro.valor), 0))
        .filter(*filtros)
        .scalar()
    )
    return Decimal(str(resultado or ZERO))


def _filtro_entradas():
    return FluxoDinheiro.tipo == "entrada"


def _filtro_saidas():
    return FluxoDinheiro.tipo.in_(["saida", "investimento"])


def _filtro_transferencias(direcao: str):
    return (
        (FluxoDinheiro.tipo == "transferencia")
        & (FluxoDinheiro.transferencia_direcao == direcao)
    )


def obter_saldo_conta(db: Session, conta_bancaria_id: int) -> Decimal:
    conta = (
        db.query(ContaBancaria)
        .filter(ContaBancaria.id == conta_bancaria_id)
        .first()
    )
    if conta is None:
        raise ValueError("Conta bancária não encontrada.")
    return Decimal(str(conta.valor_conta_atual))


def calcular_movimentacoes_apos_data(
    db: Session,
    conta_bancaria_id: int,
    data_inicio: date,
) -> Decimal:
    filtros = (
        FluxoDinheiro.conta_bancaria_id == conta_bancaria_id,
        FluxoDinheiro.data_movimentacao >= data_inicio,
    )
    entradas = _soma_movimentacoes(db, *filtros, _filtro_entradas())
    saidas = _soma_movimentacoes(db, *filtros, FluxoDinheiro.tipo.in_(["saida", "investimento"]))
    recebidas = _soma_movimentacoes(
        db, *filtros, _filtro_transferencias("destino")
    )
    enviadas = _soma_movimentacoes(
        db, *filtros, _filtro_transferencias("origem")
    )
    ajustes = _soma_movimentacoes(
        db, *filtros, FluxoDinheiro.tipo == "ajuste"
    )
    return entradas + recebidas - saidas - enviadas + ajustes


def calcular_saldo_inicial(
    db: Session,
    conta_bancaria_id: int,
    data_inicio: date,
) -> Decimal:
    saldo_atual = obter_saldo_conta(db, conta_bancaria_id)
    variacao_apos_data = calcular_movimentacoes_apos_data(
        db,
        conta_bancaria_id,
        data_inicio,
    )
    return saldo_atual - variacao_apos_data


def calcular_entradas(
    db: Session,
    conta_bancaria_id: int,
    data_inicio: date,
    data_fim: date,
) -> Decimal:
    return _soma_movimentacoes(
        db,
        FluxoDinheiro.conta_bancaria_id == conta_bancaria_id,
        _filtro_entradas(),
        FluxoDinheiro.data_movimentacao >= data_inicio,
        FluxoDinheiro.data_movimentacao <= data_fim,
    )


def calcular_saidas(
    db: Session,
    conta_bancaria_id: int,
    data_inicio: date,
    data_fim: date,
) -> Decimal:
    return _soma_movimentacoes(
        db,
        FluxoDinheiro.conta_bancaria_id == conta_bancaria_id,
        _filtro_saidas(),
        FluxoDinheiro.data_movimentacao >= data_inicio,
        FluxoDinheiro.data_movimentacao <= data_fim,
    )


def calcular_investimentos(
    db: Session,
    conta_bancaria_id: int,
    data_inicio: date,
    data_fim: date,
) -> Decimal:
    return _soma_movimentacoes(
        db,
        FluxoDinheiro.conta_bancaria_id == conta_bancaria_id,
        FluxoDinheiro.tipo.in_(["saida", "investimento"]),
        (FluxoDinheiro.categoria == "investimento") | (FluxoDinheiro.tipo_investimento.isnot(None)),
        FluxoDinheiro.data_movimentacao >= data_inicio,
        FluxoDinheiro.data_movimentacao <= data_fim,
    )


def calcular_transferencias(
    db: Session,
    conta_bancaria_id: int,
    data_inicio: date,
    data_fim: date,
    direcao: str,
) -> Decimal:
    return _soma_movimentacoes(
        db,
        FluxoDinheiro.conta_bancaria_id == conta_bancaria_id,
        _filtro_transferencias(direcao),
        FluxoDinheiro.data_movimentacao >= data_inicio,
        FluxoDinheiro.data_movimentacao <= data_fim,
    )


def calcular_ajustes(
    db: Session,
    conta_bancaria_id: int,
    data_inicio: date,
    data_fim: date,
) -> Decimal:
    return _soma_movimentacoes(
        db,
        FluxoDinheiro.conta_bancaria_id == conta_bancaria_id,
        FluxoDinheiro.tipo == "ajuste",
        FluxoDinheiro.data_movimentacao >= data_inicio,
        FluxoDinheiro.data_movimentacao <= data_fim,
    )


def calcular_resumo_periodo(
    db: Session,
    conta_bancaria_id: int,
    data_inicio: date,
    data_fim: date,
) -> ResumoFinanceiro:
    if data_fim < data_inicio:
        raise ValueError("A data final não pode ser anterior à data inicial.")
    if data_inicio > date.today():
        raise ValueError("A data inicial não pode estar no futuro.")

    saldo_inicial = calcular_saldo_inicial(
        db,
        conta_bancaria_id,
        data_inicio,
    )
    total_entradas = calcular_entradas(
        db,
        conta_bancaria_id,
        data_inicio,
        data_fim,
    )
    total_saidas = calcular_saidas(
        db,
        conta_bancaria_id,
        data_inicio,
        data_fim,
    )
    total_investimentos = calcular_investimentos(
        db,
        conta_bancaria_id,
        data_inicio,
        data_fim,
    )
    total_transferencias_recebidas = calcular_transferencias(
        db, conta_bancaria_id, data_inicio, data_fim, "destino"
    )
    total_transferencias_enviadas = calcular_transferencias(
        db, conta_bancaria_id, data_inicio, data_fim, "origem"
    )
    total_ajustes = calcular_ajustes(
        db, conta_bancaria_id, data_inicio, data_fim
    )

    return {
        "conta_bancaria_id": conta_bancaria_id,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "saldo_inicial": saldo_inicial,
        "total_entradas": total_entradas,
        "total_saidas": total_saidas,
        "total_investimentos": total_investimentos,
        "total_transferencias_recebidas": total_transferencias_recebidas,
        "total_transferencias_enviadas": total_transferencias_enviadas,
        "total_ajustes": total_ajustes,
        "saldo_final": (
            saldo_inicial
            + total_entradas
            - total_saidas
            + total_transferencias_recebidas
            - total_transferencias_enviadas
            + total_ajustes
        ),
    }


def calcular_resumo_mensal(
    db: Session,
    conta_bancaria_id: int,
    mes: int,
    ano: int,
) -> ResumoFinanceiro:
    if mes < 1 or mes > 12:
        raise ValueError("O mês deve estar entre 1 e 12.")
    data_inicio = date(ano, mes, 1)
    data_fim = date(ano, mes, calendar.monthrange(ano, mes)[1])
    return calcular_resumo_periodo(
        db,
        conta_bancaria_id,
        data_inicio,
        data_fim,
    )


def calcular_resumo_anual(
    db: Session,
    conta_bancaria_id: int,
    ano: int,
) -> ResumoFinanceiro:
    return calcular_resumo_periodo(
        db,
        conta_bancaria_id,
        date(ano, 1, 1),
        date(ano, 12, 31),
    )


def salvar_calculo_financeiro(
    db: Session,
    conta_bancaria_id: int,
    tipo_calculo: str,
    data_inicio: date,
    data_fim: date,
    valor_original: Decimal,
    total_entradas: Decimal,
    total_saidas: Decimal,
    total_investimentos: Decimal,
    total_transferencias_recebidas: Decimal,
    total_transferencias_enviadas: Decimal,
    total_ajustes: Decimal,
    valor_final: Decimal,
) -> CalculoFinanceiro:
    calculo = CalculoFinanceiro(
        conta_bancaria_id=conta_bancaria_id,
        tipo_calculo=tipo_calculo,
        data_inicio=data_inicio,
        data_fim=data_fim,
        valor_original=valor_original,
        total_entradas=total_entradas,
        total_saidas=total_saidas,
        total_investimentos=total_investimentos,
        total_transferencias_recebidas=total_transferencias_recebidas,
        total_transferencias_enviadas=total_transferencias_enviadas,
        total_ajustes=total_ajustes,
        valor_final=valor_final,
    )
    db.add(calculo)
    db.commit()
    db.refresh(calculo)
    return calculo


# =========================================================
# MOTOR DO SIMULADOR DE INVESTIMENTOS (JUROS COMPOSTOS + IR)
# =========================================================

TAXA_CDI_BASE_PADRAO = Decimal("10.65")
TAXA_IPCA_BASE_PADRAO = Decimal("4.50")

ATIVOS_ISENTOS_IR = {
    "Poupança",
    "LCI / LCA",
}

ATIVOS_RENDA_VARIAVEL = {
    "Ação",
    "Fundos de Índice (ETFs)",
    "Fundos Imobiliários (FIIs)",
    "Subscrição",
}


def _arredondar_moeda(valor: Decimal | float) -> Decimal:
    return Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def converter_taxa_anual_para_mensal(taxa_anual_percentual: Decimal | float) -> float:
    """Converte a taxa anual (%) para a taxa mensal equivalente (fração decimal):
    i_mensal = (1 + i_anual)^(1/12) - 1
    """
    i_anual = float(taxa_anual_percentual) / 100.0
    if i_anual <= 0.0:
        return 0.0
    return (1.0 + i_anual) ** (1.0 / 12.0) - 1.0


def obter_aliquota_ir_investimento(tipo_ativo: str, prazo_meses: int) -> Decimal:
    """Retorna a alíquota percentual de Imposto de Renda no resgate conforme o ativo e prazo."""
    if tipo_ativo in ATIVOS_ISENTOS_IR:
        return Decimal("0.00")

    if tipo_ativo == "Fundos Imobiliários (FIIs)":
        # Dividendos de FIIs são isentos; ganho de capital em cota possui alíquota de 20%
        return Decimal("20.00")

    if tipo_ativo in ("Ação", "Fundos de Índice (ETFs)", "Subscrição"):
        return Decimal("15.00")

    # Tabela Regressiva de IR para Renda Fixa (CDB, Tesouro Direto, Fundos de Investimento)
    # Até 180 dias (<= 6 meses): 22,5%
    # 181 a 360 dias (7 a 12 meses): 20,0%
    # 361 a 720 dias (13 a 24 meses): 17,5%
    # Acima de 720 dias (> 24 meses): 15,0%
    if prazo_meses <= 6:
        return Decimal("22.50")
    if prazo_meses <= 12:
        return Decimal("20.00")
    if prazo_meses <= 24:
        return Decimal("17.50")
    return Decimal("15.00")


def calcular_valor_futuro_composto(
    capital_inicial: Decimal | float,
    aporte_mensal: Decimal | float,
    taxa_mensal: float,
    meses: int,
) -> float:
    """Fórmula exata de Valor Futuro com aportes mensais:
    M = C * (1 + i)^t + A * (((1 + i)^t - 1) / i)
    """
    c = float(capital_inicial)
    a = float(aporte_mensal)
    t = int(meses)
    if t <= 0:
        return c
    if taxa_mensal <= 0.0:
        return c + (a * t)
    fator = (1.0 + taxa_mensal) ** t
    return (c * fator) + (a * ((fator - 1.0) / taxa_mensal))


def simular_investimento(
    tipo_ativo: str,
    valor_inicial: Decimal,
    aporte_mensal: Decimal,
    prazo_meses: int,
    taxa_anual: Decimal,
    indexador: str = "Pré-fixado",
    percentual_cdi: Decimal | None = None,
    taxa_cdi_anual: Decimal | None = None,
    inflacao_ipca_anual: Decimal | None = None,
    dividend_yield_anual: Decimal | None = None,
) -> dict[str, Any]:
    """Executa a simulação completa de evolução patrimonial, juros compostos e tributação."""
    c_dec = Decimal(str(valor_inicial))
    a_dec = Decimal(str(aporte_mensal))
    taxa_informada = Decimal(str(taxa_anual))
    dy_anual = Decimal(str(dividend_yield_anual or Decimal("0.00")))

    # 1. Cálculo da Taxa Anual Efetiva conforme o Indexador
    if indexador == "CDI":
        if percentual_cdi is not None:
            base_cdi = Decimal(str(taxa_cdi_anual)) if taxa_cdi_anual is not None else taxa_informada
            taxa_base_anual = base_cdi * (Decimal(str(percentual_cdi)) / Decimal("100"))
        elif taxa_informada > Decimal("35"):
            # Quando taxa_anual é informada como percentual do CDI (ex: 110 para 110% do CDI)
            base_cdi = Decimal(str(taxa_cdi_anual)) if taxa_cdi_anual is not None else TAXA_CDI_BASE_PADRAO
            taxa_base_anual = base_cdi * (taxa_informada / Decimal("100"))
        elif taxa_cdi_anual is not None:
            taxa_base_anual = Decimal(str(taxa_cdi_anual)) * (taxa_informada / Decimal("100"))
        else:
            taxa_base_anual = taxa_informada
    elif indexador == "IPCA":
        inflacao = (
            Decimal(str(inflacao_ipca_anual))
            if inflacao_ipca_anual is not None
            else TAXA_IPCA_BASE_PADRAO
        )
        taxa_base_anual = taxa_informada + inflacao
    else:
        taxa_base_anual = taxa_informada

    # Para Renda Variável / FIIs: soma expectativa de Ganho de Capital + reinvestimento de Dividend Yield (DY)
    taxa_efetiva_anual = taxa_base_anual + dy_anual

    # 2. Conversão de Taxa Anual (a.a.) para Taxa Mensal Equivalente (a.m.)
    i_mensal = converter_taxa_anual_para_mensal(taxa_efetiva_anual)
    taxa_mensal_pct = Decimal(str(i_mensal * 100.0)).quantize(
        Decimal("0.0001"), rounding=ROUND_HALF_UP
    )

    # 3. Tributação (Tabela Regressiva de IR vs Isenção LCI/LCA e Poupança)
    isento_ir = tipo_ativo in ATIVOS_ISENTOS_IR
    aliquota_ir = obter_aliquota_ir_investimento(tipo_ativo, prazo_meses)

    # Em Renda Variável / FIIs, dividendos reinvestidos (DY) são isentos de IR;
    # o imposto incide apenas sobre a parcela de ganho de capital
    proporcao_tributavel = Decimal("1.00")
    if (
        not isento_ir
        and tipo_ativo in ATIVOS_RENDA_VARIAVEL
        and dy_anual > Decimal("0.00")
        and taxa_efetiva_anual > Decimal("0.00")
    ):
        proporcao_tributavel = max(
            Decimal("0.00"),
            min(Decimal("1.00"), taxa_base_anual / taxa_efetiva_anual),
        )

    # 4. Série de Evolução Patrimonial Mês a Mês (0 até prazo_meses)
    evolucao_mensal: list[dict[str, Any]] = []
    for mes in range(0, prazo_meses + 1):
        investido_mes = _arredondar_moeda(c_dec + (a_dec * Decimal(mes)))
        bruto_mes_float = calcular_valor_futuro_composto(c_dec, a_dec, i_mensal, mes)
        acumulado_bruto_mes = _arredondar_moeda(bruto_mes_float)
        rendimento_mes = max(ZERO, acumulado_bruto_mes - investido_mes)

        aliquota_mes = obter_aliquota_ir_investimento(tipo_ativo, max(1, mes))
        imposto_mes = (
            ZERO
            if isento_ir
            else _arredondar_moeda(
                rendimento_mes * proporcao_tributavel * (aliquota_mes / Decimal("100"))
            )
        )
        liquido_mes = acumulado_bruto_mes - imposto_mes

        evolucao_mensal.append(
            {
                "mes": mes,
                "total_investido": investido_mes,
                "total_acumulado": acumulado_bruto_mes,
                "total_liquido": liquido_mes,
                "rendimento_acumulado": rendimento_mes,
            }
        )

    ultimo = evolucao_mensal[-1]
    valor_total_investido = ultimo["total_investido"]
    valor_total_bruto = ultimo["total_acumulado"]
    rendimento_bruto = max(ZERO, valor_total_bruto - valor_total_investido)

    imposto_descontado = (
        ZERO
        if isento_ir
        else _arredondar_moeda(
            rendimento_bruto * proporcao_tributavel * (aliquota_ir / Decimal("100"))
        )
    )
    rendimento_liquido = max(ZERO, rendimento_bruto - imposto_descontado)
    valor_liquido_projetado = valor_total_bruto - imposto_descontado

    return {
        "tipo_ativo": tipo_ativo,
        "indexador": indexador,
        "valor_inicial": _arredondar_moeda(c_dec),
        "aporte_mensal": _arredondar_moeda(a_dec),
        "prazo_meses": prazo_meses,
        "taxa_anual_informada": _arredondar_moeda(taxa_informada),
        "taxa_efetiva_anual": _arredondar_moeda(taxa_efetiva_anual),
        "taxa_mensal": i_mensal,
        "taxa_mensal_equivalente": i_mensal,
        "taxa_mensal_percentual": taxa_mensal_pct,
        "valor_total_investido": valor_total_investido,
        "total_investido": valor_total_investido,
        "valor_total_bruto": valor_total_bruto,
        "total_acumulado": valor_total_bruto,
        "rendimento_bruto": rendimento_bruto,
        "aliquota_ir": aliquota_ir if not isento_ir else Decimal("0.00"),
        "isento_ir": isento_ir,
        "imposto_descontado": imposto_descontado,
        "rendimento_liquido": rendimento_liquido,
        "valor_liquido_projetado": valor_liquido_projetado,
        "evolucao_mensal": evolucao_mensal,
    }
