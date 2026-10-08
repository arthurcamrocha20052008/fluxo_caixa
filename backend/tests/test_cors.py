def test_cors_permite_frontend_local_com_autorizacao(client):
    resposta = client.options(
        "/contas-bancarias/",
        headers={
            "Origin": "http://fluxocaixa",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "authorization,content-type",
        },
    )

    assert resposta.status_code == 200
    assert resposta.headers["access-control-allow-origin"] == (
        "http://fluxocaixa"
    )
    assert "access-control-allow-credentials" not in resposta.headers
    assert "POST" in resposta.headers["access-control-allow-methods"]
    assert "authorization" in resposta.headers[
        "access-control-allow-headers"
    ].lower()


def test_cors_rejeita_origem_nao_autorizada(client):
    resposta = client.options(
        "/contas-bancarias/",
        headers={
            "Origin": "http://origem-nao-autorizada",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert resposta.status_code == 400
    assert "access-control-allow-origin" not in resposta.headers
