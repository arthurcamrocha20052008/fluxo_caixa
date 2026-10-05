from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db

# Importa os 10 modelos do banco
from models import (
    Usuario,
    Categoria,
    FluxoMensal,
    ContaFixa,
    ContaVariavel,
    Investimento,
    Movimentacao,
    CategoriaInvestimento,
    ContaBancaria,
    Lancamento
)

# Importa os schemas usados pelo FastAPI
from esquema import (
    UsuarioCreate,
    UsuarioResponse,

    CategoriaCreate,
    CategoriaResponse,

    FluxoMensalCreate,
    FluxoMensalResponse,

    ContaFixaCreate,
    ContaFixaResponse,

    ContaVariavelCreate,
    ContaVariavelResponse,

    InvestimentoCreate,
    InvestimentoResponse,

    MovimentacaoCreate,
    MovimentacaoResponse,

    CategoriaInvestimentoCreate,
    CategoriaInvestimentoResponse,

    ContaBancariaCreate,
    ContaBancariaResponse,

    LancamentoCreate,
    LancamentoResponse
)


# =========================================================
# CRIAÇÃO DAS TABELAS
# =========================================================
# O SQLAlchemy verifica os modelos registrados e cria
# tabelas que ainda não existirem.
#
# Como o seu banco já existe, normalmente ele apenas
# utiliza as tabelas existentes.
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# CONFIGURAÇÃO DA API
# =========================================================

app = FastAPI(
    title="Sistema de Fluxo de Caixa",
    description="API para controle de finanças domésticas",
    version="1.0.0"
)

# =========================================================
# 1. CRUD DE USUÁRIOS
# =========================================================

# ---------------------------------------------------------
# CREATE - Criar usuário
# ---------------------------------------------------------

@app.post(
    "/usuarios",
    response_model=UsuarioResponse
)
def criar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):

    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=usuario.senha
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario


# ---------------------------------------------------------
# READ - Listar usuários
# ---------------------------------------------------------

@app.get(
    "/usuarios",
    response_model=list[UsuarioResponse]
)
def listar_usuarios(
    db: Session = Depends(get_db)
):

    return db.query(Usuario).all()


# ---------------------------------------------------------
# READ - Buscar usuário por ID
# ---------------------------------------------------------

@app.get(
    "/usuarios/{usuario_id}",
    response_model=UsuarioResponse
)
def buscar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):

    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return usuario


# ---------------------------------------------------------
# UPDATE - Atualizar usuário
# ---------------------------------------------------------

@app.put(
    "/usuarios/{usuario_id}",
    response_model=UsuarioResponse
)
def atualizar_usuario(
    usuario_id: int,
    usuario_atualizado: UsuarioCreate,
    db: Session = Depends(get_db)
):

    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    usuario.nome = usuario_atualizado.nome
    usuario.email = usuario_atualizado.email
    usuario.senha = usuario_atualizado.senha

    db.commit()
    db.refresh(usuario)

    return usuario


# ---------------------------------------------------------
# DELETE - Excluir usuário
# ---------------------------------------------------------

@app.delete("/usuarios/{usuario_id}")
def excluir_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):

    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    db.delete(usuario)
    db.commit()

    return {
        "mensagem": "Usuário excluído com sucesso"
    }


# =========================================================
# 2. CRUD DE CATEGORIAS
# =========================================================


@app.post(
    "/categorias",
    response_model=CategoriaResponse
)
def criar_categoria(
    categoria: CategoriaCreate,
    db: Session = Depends(get_db)
):

    nova_categoria = Categoria(
        nome=categoria.nome,
        tipo=categoria.tipo
    )

    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)

    return nova_categoria


@app.get(
    "/categorias",
    response_model=list[CategoriaResponse]
)
def listar_categorias(
    db: Session = Depends(get_db)
):

    return db.query(Categoria).all()


@app.get(
    "/categorias/{categoria_id}",
    response_model=CategoriaResponse
)
def buscar_categoria(
    categoria_id: int,
    db: Session = Depends(get_db)
):

    categoria = (
        db.query(Categoria)
        .filter(Categoria.id == categoria_id)
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    return categoria


@app.put(
    "/categorias/{categoria_id}",
    response_model=CategoriaResponse
)
def atualizar_categoria(
    categoria_id: int,
    categoria_atualizada: CategoriaCreate,
    db: Session = Depends(get_db)
):

    categoria = (
        db.query(Categoria)
        .filter(Categoria.id == categoria_id)
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    categoria.nome = categoria_atualizada.nome
    categoria.tipo = categoria_atualizada.tipo

    db.commit()
    db.refresh(categoria)

    return categoria


@app.delete("/categorias/{categoria_id}")
def excluir_categoria(
    categoria_id: int,
    db: Session = Depends(get_db)
):

    categoria = (
        db.query(Categoria)
        .filter(Categoria.id == categoria_id)
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    db.delete(categoria)
    db.commit()

    return {
        "mensagem": "Categoria excluída com sucesso"
    }


# =========================================================
# 3. CRUD DE FLUXO MENSAL
# =========================================================


@app.post(
    "/fluxo-mensal",
    response_model=FluxoMensalResponse
)
def criar_fluxo_mensal(
    fluxo: FluxoMensalCreate,
    db: Session = Depends(get_db)
):

    novo_fluxo = FluxoMensal(
        mes=fluxo.mes,
        ano=fluxo.ano,
        valor_original=fluxo.valor_original,
        total_entradas=fluxo.total_entradas,
        total_contas_fixas=fluxo.total_contas_fixas,
        total_contas_variaveis=fluxo.total_contas_variaveis,
        total_investimentos=fluxo.total_investimentos,
        valor_final=fluxo.valor_final
    )

    db.add(novo_fluxo)
    db.commit()
    db.refresh(novo_fluxo)

    return novo_fluxo


@app.get(
    "/fluxo-mensal",
    response_model=list[FluxoMensalResponse]
)
def listar_fluxos_mensais(
    db: Session = Depends(get_db)
):

    return db.query(FluxoMensal).all()


@app.get(
    "/fluxo-mensal/{fluxo_id}",
    response_model=FluxoMensalResponse
)
def buscar_fluxo_mensal(
    fluxo_id: int,
    db: Session = Depends(get_db)
):

    fluxo = (
        db.query(FluxoMensal)
        .filter(FluxoMensal.id == fluxo_id)
        .first()
    )

    if not fluxo:
        raise HTTPException(
            status_code=404,
            detail="Fluxo mensal não encontrado"
        )

    return fluxo


@app.put(
    "/fluxo-mensal/{fluxo_id}",
    response_model=FluxoMensalResponse
)
def atualizar_fluxo_mensal(
    fluxo_id: int,
    fluxo_atualizado: FluxoMensalCreate,
    db: Session = Depends(get_db)
):

    fluxo = (
        db.query(FluxoMensal)
        .filter(FluxoMensal.id == fluxo_id)
        .first()
    )

    if not fluxo:
        raise HTTPException(
            status_code=404,
            detail="Fluxo mensal não encontrado"
        )

    fluxo.mes = fluxo_atualizado.mes
    fluxo.ano = fluxo_atualizado.ano
    fluxo.valor_original = fluxo_atualizado.valor_original
    fluxo.total_entradas = fluxo_atualizado.total_entradas
    fluxo.total_contas_fixas = fluxo_atualizado.total_contas_fixas
    fluxo.total_contas_variaveis = fluxo_atualizado.total_contas_variaveis
    fluxo.total_investimentos = fluxo_atualizado.total_investimentos
    fluxo.valor_final = fluxo_atualizado.valor_final

    db.commit()
    db.refresh(fluxo)

    return fluxo


@app.delete("/fluxo-mensal/{fluxo_id}")
def excluir_fluxo_mensal(
    fluxo_id: int,
    db: Session = Depends(get_db)
):

    fluxo = (
        db.query(FluxoMensal)
        .filter(FluxoMensal.id == fluxo_id)
        .first()
    )

    if not fluxo:
        raise HTTPException(
            status_code=404,
            detail="Fluxo mensal não encontrado"
        )

    db.delete(fluxo)
    db.commit()

    return {
        "mensagem": "Fluxo mensal excluído com sucesso"
    }


# =========================================================
# 4. CRUD DE CONTAS FIXAS
# =========================================================


@app.post(
    "/contas-fixas",
    response_model=ContaFixaResponse
)
def criar_conta_fixa(
    conta: ContaFixaCreate,
    db: Session = Depends(get_db)
):

    nova_conta = ContaFixa(
        nome=conta.nome,
        valor=conta.valor,
        dia_vencimento=conta.dia_vencimento,
        categoria_id=conta.categoria_id,
        status=conta.status,
        observacao=conta.observacao
    )

    db.add(nova_conta)
    db.commit()
    db.refresh(nova_conta)

    return nova_conta


@app.get(
    "/contas-fixas",
    response_model=list[ContaFixaResponse]
)
def listar_contas_fixas(
    db: Session = Depends(get_db)
):

    return db.query(ContaFixa).all()


@app.get(
    "/contas-fixas/{conta_id}",
    response_model=ContaFixaResponse
)
def buscar_conta_fixa(
    conta_id: int,
    db: Session = Depends(get_db)
):

    conta = (
        db.query(ContaFixa)
        .filter(ContaFixa.id == conta_id)
        .first()
    )

    if not conta:
        raise HTTPException(
            status_code=404,
            detail="Conta fixa não encontrada"
        )

    return conta


@app.put(
    "/contas-fixas/{conta_id}",
    response_model=ContaFixaResponse
)
def atualizar_conta_fixa(
    conta_id: int,
    conta_atualizada: ContaFixaCreate,
    db: Session = Depends(get_db)
):

    conta = (
        db.query(ContaFixa)
        .filter(ContaFixa.id == conta_id)
        .first()
    )

    if not conta:
        raise HTTPException(
            status_code=404,
            detail="Conta fixa não encontrada"
        )

    conta.nome = conta_atualizada.nome
    conta.valor = conta_atualizada.valor
    conta.dia_vencimento = conta_atualizada.dia_vencimento
    conta.categoria_id = conta_atualizada.categoria_id
    conta.status = conta_atualizada.status
    conta.observacao = conta_atualizada.observacao

    db.commit()
    db.refresh(conta)

    return conta


@app.delete("/contas-fixas/{conta_id}")
def excluir_conta_fixa(
    conta_id: int,
    db: Session = Depends(get_db)
):

    conta = (
        db.query(ContaFixa)
        .filter(ContaFixa.id == conta_id)
        .first()
    )

    if not conta:
        raise HTTPException(
            status_code=404,
            detail="Conta fixa não encontrada"
        )

    db.delete(conta)
    db.commit()

    return {
        "mensagem": "Conta fixa excluída com sucesso"
    }


# =========================================================
# 5. CRUD DE CONTAS VARIÁVEIS
# =========================================================


@app.post(
    "/contas-variaveis",
    response_model=ContaVariavelResponse
)
def criar_conta_variavel(
    conta: ContaVariavelCreate,
    db: Session = Depends(get_db)
):

    nova_conta = ContaVariavel(
        nome=conta.nome,
        valor=conta.valor,
        data_conta=conta.data_conta,
        categoria_id=conta.categoria_id,
        observacao=conta.observacao
    )

    db.add(nova_conta)
    db.commit()
    db.refresh(nova_conta)

    return nova_conta


@app.get(
    "/contas-variaveis",
    response_model=list[ContaVariavelResponse]
)
def listar_contas_variaveis(
    db: Session = Depends(get_db)
):

    return db.query(ContaVariavel).all()


@app.get(
    "/contas-variaveis/{conta_id}",
    response_model=ContaVariavelResponse
)
def buscar_conta_variavel(
    conta_id: int,
    db: Session = Depends(get_db)
):

    conta = (
        db.query(ContaVariavel)
        .filter(ContaVariavel.id == conta_id)
        .first()
    )

    if not conta:
        raise HTTPException(
            status_code=404,
            detail="Conta variável não encontrada"
        )

    return conta


@app.put(
    "/contas-variaveis/{conta_id}",
    response_model=ContaVariavelResponse
)
def atualizar_conta_variavel(
    conta_id: int,
    conta_atualizada: ContaVariavelCreate,
    db: Session = Depends(get_db)
):

    conta = (
        db.query(ContaVariavel)
        .filter(ContaVariavel.id == conta_id)
        .first()
    )

    if not conta:
        raise HTTPException(
            status_code=404,
            detail="Conta variável não encontrada"
        )

    conta.nome = conta_atualizada.nome
    conta.valor = conta_atualizada.valor
    conta.data_conta = conta_atualizada.data_conta
    conta.categoria_id = conta_atualizada.categoria_id
    conta.observacao = conta_atualizada.observacao

    db.commit()
    db.refresh(conta)

    return conta


@app.delete("/contas-variaveis/{conta_id}")
def excluir_conta_variavel(
    conta_id: int,
    db: Session = Depends(get_db)
):

    conta = (
        db.query(ContaVariavel)
        .filter(ContaVariavel.id == conta_id)
        .first()
    )

    if not conta:
        raise HTTPException(
            status_code=404,
            detail="Conta variável não encontrada"
        )

    db.delete(conta)
    db.commit()

    return {
        "mensagem": "Conta variável excluída com sucesso"
    }


# =========================================================
# 6. CRUD DE INVESTIMENTOS
# =========================================================


@app.post(
    "/investimentos",
    response_model=InvestimentoResponse
)
def criar_investimento(
    investimento: InvestimentoCreate,
    db: Session = Depends(get_db)
):

    novo_investimento = Investimento(
        nome=investimento.nome,
        tipo=investimento.tipo,
        valor=investimento.valor,
        data_investimento=investimento.data_investimento,
        descricao=investimento.descricao,
        status=investimento.status
    )

    db.add(novo_investimento)
    db.commit()
    db.refresh(novo_investimento)

    return novo_investimento


@app.get(
    "/investimentos",
    response_model=list[InvestimentoResponse]
)
def listar_investimentos(
    db: Session = Depends(get_db)
):

    return db.query(Investimento).all()


@app.get(
    "/investimentos/{investimento_id}",
    response_model=InvestimentoResponse
)
def buscar_investimento(
    investimento_id: int,
    db: Session = Depends(get_db)
):

    investimento = (
        db.query(Investimento)
        .filter(Investimento.id == investimento_id)
        .first()
    )

    if not investimento:
        raise HTTPException(
            status_code=404,
            detail="Investimento não encontrado"
        )

    return investimento


@app.put(
    "/investimentos/{investimento_id}",
    response_model=InvestimentoResponse
)
def atualizar_investimento(
    investimento_id: int,
    investimento_atualizado: InvestimentoCreate,
    db: Session = Depends(get_db)
):

    investimento = (
        db.query(Investimento)
        .filter(Investimento.id == investimento_id)
        .first()
    )

    if not investimento:
        raise HTTPException(
            status_code=404,
            detail="Investimento não encontrado"
        )

    investimento.nome = investimento_atualizado.nome
    investimento.tipo = investimento_atualizado.tipo
    investimento.valor = investimento_atualizado.valor
    investimento.data_investimento = investimento_atualizado.data_investimento
    investimento.descricao = investimento_atualizado.descricao
    investimento.status = investimento_atualizado.status

    db.commit()
    db.refresh(investimento)

    return investimento


@app.delete("/investimentos/{investimento_id}")
def excluir_investimento(
    investimento_id: int,
    db: Session = Depends(get_db)
):

    investimento = (
        db.query(Investimento)
        .filter(Investimento.id == investimento_id)
        .first()
    )

    if not investimento:
        raise HTTPException(
            status_code=404,
            detail="Investimento não encontrado"
        )

    db.delete(investimento)
    db.commit()

    return {
        "mensagem": "Investimento excluído com sucesso"
    }


# =========================================================
# 7. CRUD DE MOVIMENTAÇÕES
# =========================================================


@app.post(
    "/movimentacoes",
    response_model=MovimentacaoResponse
)
def criar_movimentacao(
    movimentacao: MovimentacaoCreate,
    db: Session = Depends(get_db)
):

    nova_movimentacao = Movimentacao(
        descricao=movimentacao.descricao,
        valor=movimentacao.valor,
        tipo=movimentacao.tipo,
        data_movimentacao=movimentacao.data_movimentacao,
        categoria_id=movimentacao.categoria_id,
        observacao=movimentacao.observacao,
        conta_bancaria_id=movimentacao.conta_bancaria_id
    )

    db.add(nova_movimentacao)
    db.commit()
    db.refresh(nova_movimentacao)

    return nova_movimentacao


@app.get(
    "/movimentacoes",
    response_model=list[MovimentacaoResponse]
)
def listar_movimentacoes(
    db: Session = Depends(get_db)
):

    return db.query(Movimentacao).all()


@app.get(
    "/movimentacoes/{movimentacao_id}",
    response_model=MovimentacaoResponse
)
def buscar_movimentacao(
    movimentacao_id: int,
    db: Session = Depends(get_db)
):

    movimentacao = (
        db.query(Movimentacao)
        .filter(Movimentacao.id == movimentacao_id)
        .first()
    )

    if not movimentacao:
        raise HTTPException(
            status_code=404,
            detail="Movimentação não encontrada"
        )

    return movimentacao


@app.put(
    "/movimentacoes/{movimentacao_id}",
    response_model=MovimentacaoResponse
)
def atualizar_movimentacao(
    movimentacao_id: int,
    movimentacao_atualizada: MovimentacaoCreate,
    db: Session = Depends(get_db)
):

    movimentacao = (
        db.query(Movimentacao)
        .filter(Movimentacao.id == movimentacao_id)
        .first()
    )

    if not movimentacao:
        raise HTTPException(
            status_code=404,
            detail="Movimentação não encontrada"
        )

    movimentacao.descricao = movimentacao_atualizada.descricao
    movimentacao.valor = movimentacao_atualizada.valor
    movimentacao.tipo = movimentacao_atualizada.tipo
    movimentacao.data_movimentacao = movimentacao_atualizada.data_movimentacao
    movimentacao.categoria_id = movimentacao_atualizada.categoria_id
    movimentacao.observacao = movimentacao_atualizada.observacao
    movimentacao.conta_bancaria_id = movimentacao_atualizada.conta_bancaria_id

    db.commit()
    db.refresh(movimentacao)

    return movimentacao


@app.delete("/movimentacoes/{movimentacao_id}")
def excluir_movimentacao(
    movimentacao_id: int,
    db: Session = Depends(get_db)
):

    movimentacao = (
        db.query(Movimentacao)
        .filter(Movimentacao.id == movimentacao_id)
        .first()
    )

    if not movimentacao:
        raise HTTPException(
            status_code=404,
            detail="Movimentação não encontrada"
        )

    db.delete(movimentacao)
    db.commit()

    return {
        "mensagem": "Movimentação excluída com sucesso"
    }


# =========================================================
# 8. CRUD DE CATEGORIAS DE INVESTIMENTO
# =========================================================


@app.post(
    "/categorias-investimento",
    response_model=CategoriaInvestimentoResponse
)
def criar_categoria_investimento(
    categoria: CategoriaInvestimentoCreate,
    db: Session = Depends(get_db)
):

    nova_categoria = CategoriaInvestimento(
        nome=categoria.nome,
        descricao=categoria.descricao
    )

    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)

    return nova_categoria


@app.get(
    "/categorias-investimento",
    response_model=list[CategoriaInvestimentoResponse]
)
def listar_categorias_investimento(
    db: Session = Depends(get_db)
):

    return db.query(CategoriaInvestimento).all()


@app.get(
    "/categorias-investimento/{categoria_id}",
    response_model=CategoriaInvestimentoResponse
)
def buscar_categoria_investimento(
    categoria_id: int,
    db: Session = Depends(get_db)
):

    categoria = (
        db.query(CategoriaInvestimento)
        .filter(CategoriaInvestimento.id == categoria_id)
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria de investimento não encontrada"
        )

    return categoria


@app.put(
    "/categorias-investimento/{categoria_id}",
    response_model=CategoriaInvestimentoResponse
)
def atualizar_categoria_investimento(
    categoria_id: int,
    categoria_atualizada: CategoriaInvestimentoCreate,
    db: Session = Depends(get_db)
):

    categoria = (
        db.query(CategoriaInvestimento)
        .filter(CategoriaInvestimento.id == categoria_id)
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria de investimento não encontrada"
        )

    categoria.nome = categoria_atualizada.nome
    categoria.descricao = categoria_atualizada.descricao

    db.commit()
    db.refresh(categoria)

    return categoria


@app.delete("/categorias-investimento/{categoria_id}")
def excluir_categoria_investimento(
    categoria_id: int,
    db: Session = Depends(get_db)
):

    categoria = (
        db.query(CategoriaInvestimento)
        .filter(CategoriaInvestimento.id == categoria_id)
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria de investimento não encontrada"
        )

    db.delete(categoria)
    db.commit()

    return {
        "mensagem": "Categoria de investimento excluída com sucesso"
    }


# =========================================================
# 9. CRUD DE CONTAS BANCÁRIAS
# =========================================================


@app.post(
    "/contas-bancarias",
    response_model=ContaBancariaResponse
)
def criar_conta_bancaria(
    conta: ContaBancariaCreate,
    db: Session = Depends(get_db)
):

    nova_conta = ContaBancaria(
        nome_banco=conta.nome_banco,
        nome_conta=conta.nome_conta,
        tipo_conta=conta.tipo_conta,
        saldo_atual=conta.saldo_atual,
        ativa=conta.ativa
    )

    db.add(nova_conta)
    db.commit()
    db.refresh(nova_conta)

    return nova_conta


@app.get(
    "/contas-bancarias",
    response_model=list[ContaBancariaResponse]
)
def listar_contas_bancarias(
    db: Session = Depends(get_db)
):

    return db.query(ContaBancaria).all()


@app.get(
    "/contas-bancarias/{conta_id}",
    response_model=ContaBancariaResponse
)
def buscar_conta_bancaria(
    conta_id: int,
    db: Session = Depends(get_db)
):

    conta = (
        db.query(ContaBancaria)
        .filter(ContaBancaria.id == conta_id)
        .first()
    )

    if not conta:
        raise HTTPException(
            status_code=404,
            detail="Conta bancária não encontrada"
        )

    return conta


@app.put(
    "/contas-bancarias/{conta_id}",
    response_model=ContaBancariaResponse
)
def atualizar_conta_bancaria(
    conta_id: int,
    conta_atualizada: ContaBancariaCreate,
    db: Session = Depends(get_db)
):

    conta = (
        db.query(ContaBancaria)
        .filter(ContaBancaria.id == conta_id)
        .first()
    )

    if not conta:
        raise HTTPException(
            status_code=404,
            detail="Conta bancária não encontrada"
        )

    conta.nome_banco = conta_atualizada.nome_banco
    conta.nome_conta = conta_atualizada.nome_conta
    conta.tipo_conta = conta_atualizada.tipo_conta
    conta.saldo_atual = conta_atualizada.saldo_atual
    conta.ativa = conta_atualizada.ativa

    db.commit()
    db.refresh(conta)

    return conta


@app.delete("/contas-bancarias/{conta_id}")
def excluir_conta_bancaria(
    conta_id: int,
    db: Session = Depends(get_db)
):

    conta = (
        db.query(ContaBancaria)
        .filter(ContaBancaria.id == conta_id)
        .first()
    )

    if not conta:
        raise HTTPException(
            status_code=404,
            detail="Conta bancária não encontrada"
        )

    db.delete(conta)
    db.commit()

    return {
        "mensagem": "Conta bancária excluída com sucesso"
    }


# =========================================================
# 10. CRUD DE LANÇAMENTOS
# =========================================================


@app.post(
    "/lancamentos",
    response_model=LancamentoResponse
)
def criar_lancamento(
    lancamento: LancamentoCreate,
    db: Session = Depends(get_db)
):

    novo_lancamento = Lancamento(
        descricao=lancamento.descricao,
        tipo=lancamento.tipo,
        categoria=lancamento.categoria,
        valor=lancamento.valor,
        data=lancamento.data
    )

    db.add(novo_lancamento)
    db.commit()
    db.refresh(novo_lancamento)

    return novo_lancamento


@app.get(
    "/lancamentos",
    response_model=list[LancamentoResponse]
)
def listar_lancamentos(
    db: Session = Depends(get_db)
):

    return db.query(Lancamento).all()


@app.get(
    "/lancamentos/{lancamento_id}",
    response_model=LancamentoResponse
)
def buscar_lancamento(
    lancamento_id: int,
    db: Session = Depends(get_db)
):

    lancamento = (
        db.query(Lancamento)
        .filter(Lancamento.id == lancamento_id)
        .first()
    )

    if not lancamento:
        raise HTTPException(
            status_code=404,
            detail="Lançamento não encontrado"
        )

    return lancamento


@app.put(
    "/lancamentos/{lancamento_id}",
    response_model=LancamentoResponse
)
def atualizar_lancamento(
    lancamento_id: int,
    lancamento_atualizado: LancamentoCreate,
    db: Session = Depends(get_db)
):

    lancamento = (
        db.query(Lancamento)
        .filter(Lancamento.id == lancamento_id)
        .first()
    )

    if not lancamento:
        raise HTTPException(
            status_code=404,
            detail="Lançamento não encontrado"
        )

    lancamento.descricao = lancamento_atualizado.descricao
    lancamento.tipo = lancamento_atualizado.tipo
    lancamento.categoria = lancamento_atualizado.categoria
    lancamento.valor = lancamento_atualizado.valor
    lancamento.data = lancamento_atualizado.data

    db.commit()
    db.refresh(lancamento)

    return lancamento


@app.delete("/lancamentos/{lancamento_id}")
def excluir_lancamento(
    lancamento_id: int,
    db: Session = Depends(get_db)
):

    lancamento = (
        db.query(Lancamento)
        .filter(Lancamento.id == lancamento_id)
        .first()
    )

    if not lancamento:
        raise HTTPException(
            status_code=404,
            detail="Lançamento não encontrado"
        )

    db.delete(lancamento)
    db.commit()

    return {
        "mensagem": "Lançamento excluído com sucesso"
    }