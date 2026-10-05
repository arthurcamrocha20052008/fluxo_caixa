from fastapi import FastAPI

from rotas_api import usuario
from rotas_api import categoria
from rotas_api import fluxomensal
from rotas_api import contasfixas
from rotas_api import contasvariaveis
from rotas_api import investimento
from rotas_api import movimentação
from rotas_api import CategoriaInvestimento
from rotas_api import ContaBancaria
from rotas_api import lancamento


app = FastAPI(
    title="API - Fluxo de Caixa",
    description="API para gerenciamento de finanças domésticas",
    version="1.0.0"
)


# =========================================================
# REGISTRO DAS ROTAS
# =========================================================

app.include_router(usuario.router)
app.include_router(categoria.router)
app.include_router(fluxomensal.router)
app.include_router(contasfixas.router)
app.include_router(contasvariaveis.router)
app.include_router(investimento.router)
app.include_router(movimentação.router)
app.include_router(CategoriaInvestimento.router)
app.include_router(ContaBancaria.router)
app.include_router(lancamento.router)