from fastapi import FastAPI

from rotasdeapi import (
    usuario,
    conta_bancaria,
    fluxo_dinheiro,
    calculo_financeiro,
    meta_financeira
)


app = FastAPI(
    title="Sistema de Fluxo de Caixa",
    description="API para controle de finanças domésticas",
    version="1.0.0"
)


app.include_router(usuario.router)
app.include_router(conta_bancaria.router)
app.include_router(fluxo_dinheiro.router)
app.include_router(calculo_financeiro.router)
app.include_router(meta_financeira.router)


@app.get("/")
def inicio():

    return {
        "mensagem": "API do Fluxo de Caixa funcionando!"
    }