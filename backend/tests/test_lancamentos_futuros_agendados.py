from datetime import date, timedelta
from decimal import Decimal
from uuid import uuid4
from fastapi.testclient import TestClient


def _cpf_valido() -> str:
    from random import randint
    corpo = [randint(0, 9) for _ in range(9)]
    d1 = sum(a * b for a, b in zip(corpo, range(10, 1, -1))) % 11
    corpo.append(0 if d1 < 2 else 11 - d1)
    d2 = sum(a * b for a, b in zip(corpo, range(11, 1, -1))) % 11
    corpo.append(0 if d2 < 2 else 11 - d2)
    return "".join(map(str, corpo))


def _autenticar_e_criar_conta(client: TestClient) -> tuple[dict, dict]:
    identificador = uuid4().hex
    email = f"futuro-{identificador}@example.com"
    senha = "TesteSeguro2026!"
    cadastro = client.post(
        "/usuarios/",
        json={
            "nome_completo": "Investidor Futuro",
            "cpf": _cpf_valido(),
            "email": email,
            "senha": senha,
        },
    )
    assert cadastro.status_code == 201, cadastro.text

    login = client.post(
        "/login",
        data={"username": email, "password": senha},
    )
    assert login.status_code == 200, login.text
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    conta = client.post(
        "/contas-bancarias/",
        headers=headers,
        json={
            "nome_banco": "Banco Futuro",
            "tipo_conta": "corrente",
            "valor_conta_atual": "1000.00",
            "ativa": True,
        },
    )
    assert conta.status_code == 201, conta.text
    return headers, conta.json()


def test_saida_futura_mantem_saldo_e_aparece_em_alertas(client: TestClient) -> None:
    headers, conta = _autenticar_e_criar_conta(client)
    hoje = date.today()
    proximo_mes_dia_7 = (
        hoje.replace(month=hoje.month + 1, day=7)
        if hoje.month < 12
        else hoje.replace(year=hoje.year + 1, month=1, day=7)
    )

    # 1. Cadastra saida futura (conta fixa agendada)
    res_saida = client.post(
        "/fluxo-dinheiro/",
        headers=headers,
        json={
            "conta_bancaria_id": conta["id"],
            "descricao": "Aluguel Programado",
            "valor": "690.90",
            "tipo": "saida",
            "categoria": "moradia",
            "natureza_conta": "fixa",
            "data_movimentacao": proximo_mes_dia_7.isoformat(),
        },
    )
    assert res_saida.status_code == 201, res_saida.text
    dados_saida = res_saida.json()
    assert dados_saida["efetivada"] is False
    assert dados_saida["data_movimentacao"] == proximo_mes_dia_7.isoformat()

    # 2. Saldo da conta bancaria DEVE PERMANECER INTACTO (1000.00)
    res_conta = client.get(f"/contas-bancarias/{conta['id']}", headers=headers)
    assert res_conta.status_code == 200
    assert Decimal(res_conta.json()["valor_conta_atual"]) == Decimal("1000.00")

    # 3. Item DEVE APARECER no endpoint de alertas
    res_alertas = client.get("/alertas", headers=headers)
    assert res_alertas.status_code == 200
    alertas = res_alertas.json()
    assert len(alertas) >= 1
    alerta_saida = next(
        (a for a in alertas if "690.90" in a["mensagem"] or "Aluguel Programado" in a["mensagem"]),
        None,
    )
    assert alerta_saida is not None
    assert alerta_saida["tipo"] == "vencimento"
    assert "Gasto previsto para" in alerta_saida["mensagem"]
    assert "Saldo mantido original" in alerta_saida["mensagem"]


def test_entrada_futura_mantem_saldo_e_aparece_em_alertas(client: TestClient) -> None:
    headers, conta = _autenticar_e_criar_conta(client)
    amanha = date.today() + timedelta(days=5)

    # 1. Cadastra entrada futura (ex: ganho fixo ou salario agendado)
    res_entrada = client.post(
        "/fluxo-dinheiro/",
        headers=headers,
        json={
            "conta_bancaria_id": conta["id"],
            "descricao": "Salário Mensal Agendado",
            "valor": "3500.00",
            "tipo": "entrada",
            "categoria": "salario",
            "natureza_conta": "fixa",
            "data_movimentacao": amanha.isoformat(),
        },
    )
    assert res_entrada.status_code == 201, res_entrada.text
    dados_entrada = res_entrada.json()
    assert dados_entrada["efetivada"] is False

    # 2. Saldo da conta bancaria DEVE PERMANECER INTACTO (1000.00)
    res_conta = client.get(f"/contas-bancarias/{conta['id']}", headers=headers)
    assert res_conta.status_code == 200
    assert Decimal(res_conta.json()["valor_conta_atual"]) == Decimal("1000.00")

    # 3. Item DEVE APARECER no endpoint de alertas como entrada
    res_alertas = client.get("/alertas", headers=headers)
    assert res_alertas.status_code == 200
    alertas = res_alertas.json()
    alerta_entrada = next(
        (a for a in alertas if "Salário Mensal Agendado" in a["mensagem"]),
        None,
    )
    assert alerta_entrada is not None
    assert alerta_entrada["tipo"] == "entrada"
    assert "Ganho previsto para" in alerta_entrada["mensagem"]
    assert "Saldo mantido original" in alerta_entrada["mensagem"]


def test_exclusao_de_lancamento_futuro_nao_altera_saldo(client: TestClient) -> None:
    headers, conta = _autenticar_e_criar_conta(client)
    futuro = date.today() + timedelta(days=15)

    # Cadastra saida futura
    res_saida = client.post(
        "/fluxo-dinheiro/",
        headers=headers,
        json={
            "conta_bancaria_id": conta["id"],
            "descricao": "Assinatura Anual Futura",
            "valor": "450.00",
            "tipo": "saida",
            "categoria": "outros",
            "data_movimentacao": futuro.isoformat(),
        },
    )
    assert res_saida.status_code == 201, res_saida.text
    movimento_id = res_saida.json()["id"]

    # Saldo continua 1000.00
    res_conta = client.get(f"/contas-bancarias/{conta['id']}", headers=headers)
    assert Decimal(res_conta.json()["valor_conta_atual"]) == Decimal("1000.00")

    # Exclui o lancamento futuro (efetivada == False)
    res_del = client.delete(f"/fluxo-dinheiro/{movimento_id}", headers=headers)
    assert res_del.status_code == 200

    # Saldo NAO PODE SER ESTORNADO (não pode virar 1450.00 nem distorcer)
    res_conta_pos = client.get(f"/contas-bancarias/{conta['id']}", headers=headers)
    assert Decimal(res_conta_pos.json()["valor_conta_atual"]) == Decimal("1000.00")


def test_lancamento_para_hoje_debita_e_credita_normalmente(client: TestClient) -> None:
    headers, conta = _autenticar_e_criar_conta(client)
    hoje = date.today()

    # 1. Entrada de hoje credita no saldo
    res_in = client.post(
        "/fluxo-dinheiro/",
        headers=headers,
        json={
            "conta_bancaria_id": conta["id"],
            "descricao": "Venda de Item Hoje",
            "valor": "200.00",
            "tipo": "entrada",
            "categoria": "vendas",
            "data_movimentacao": hoje.isoformat(),
        },
    )
    assert res_in.status_code == 201
    assert res_in.json()["efetivada"] is True

    res_conta = client.get(f"/contas-bancarias/{conta['id']}", headers=headers)
    assert Decimal(res_conta.json()["valor_conta_atual"]) == Decimal("1200.00")

    # 2. Saida de hoje debita do saldo
    res_out = client.post(
        "/fluxo-dinheiro/",
        headers=headers,
        json={
            "conta_bancaria_id": conta["id"],
            "descricao": "Mercado Hoje",
            "valor": "50.00",
            "tipo": "saida",
            "categoria": "alimentacao",
            "data_movimentacao": hoje.isoformat(),
        },
    )
    assert res_out.status_code == 201
    assert res_out.json()["efetivada"] is True

    res_conta2 = client.get(f"/contas-bancarias/{conta['id']}", headers=headers)
    assert Decimal(res_conta2.json()["valor_conta_atual"]) == Decimal("1150.00")
