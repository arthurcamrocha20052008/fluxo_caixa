import hashlib
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from secrets import token_urlsafe

from database import get_db
from models import TentativaLogin, Usuario
from esquema import UsuarioCreate, UsuarioResponse
from seguranca.seguranca import gerar_hash_senha, verificar_senha
from autenticacao import criar_token, obter_usuario_logado


router = APIRouter(
    tags=["Usuários"]
)

_HASH_SENHA_INEXISTENTE = gerar_hash_senha(token_urlsafe(32))
LIMITE_FALHAS_LOGIN = 5
JANELA_FALHAS_LOGIN = timedelta(minutes=15)
RETENCAO_TENTATIVA_LOGIN = timedelta(days=1)


def _agora_utc_sem_fuso() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _chave_cliente_login(request: Request) -> str:
    endereco = request.client.host if request.client else "desconhecido"
    return hashlib.sha256(endereco.encode("utf-8")).hexdigest()


def _obter_tentativa_login(
    db: Session,
    chave_cliente: str,
) -> TentativaLogin | None:
    return (
        db.query(TentativaLogin)
        .filter(TentativaLogin.chave_cliente == chave_cliente)
        .with_for_update()
        .first()
    )


def _verificar_limite_login(db: Session, chave_cliente: str) -> None:
    agora = _agora_utc_sem_fuso()
    db.query(TentativaLogin).filter(
        TentativaLogin.inicio_janela < agora - RETENCAO_TENTATIVA_LOGIN
    ).delete(synchronize_session=False)
    db.commit()

    tentativa = _obter_tentativa_login(db, chave_cliente)
    if tentativa is None:
        return

    if tentativa.bloqueado_ate and tentativa.bloqueado_ate > agora:
        segundos = max(
            1,
            int((tentativa.bloqueado_ate - agora).total_seconds()),
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Muitas tentativas de login. Tente novamente mais tarde.",
            headers={"Retry-After": str(segundos)},
        )

    if agora - tentativa.inicio_janela >= JANELA_FALHAS_LOGIN:
        tentativa.tentativas = 0
        tentativa.inicio_janela = agora
        tentativa.bloqueado_ate = None
        db.commit()


def _registrar_falha_login(db: Session, chave_cliente: str) -> bool:
    agora = _agora_utc_sem_fuso()
    tentativa = _obter_tentativa_login(db, chave_cliente)
    if tentativa is None:
        try:
            with db.begin_nested():
                tentativa = TentativaLogin(
                    chave_cliente=chave_cliente,
                    tentativas=1,
                    inicio_janela=agora,
                )
                db.add(tentativa)
                db.flush()
            db.commit()
            return False
        except IntegrityError:
            tentativa = _obter_tentativa_login(db, chave_cliente)
            if tentativa is None:
                raise

    if agora - tentativa.inicio_janela >= JANELA_FALHAS_LOGIN:
        tentativa.tentativas = 0
        tentativa.inicio_janela = agora
        tentativa.bloqueado_ate = None

    tentativa.tentativas += 1
    if tentativa.tentativas >= LIMITE_FALHAS_LOGIN:
        tentativa.bloqueado_ate = agora + JANELA_FALHAS_LOGIN
    bloqueado = tentativa.bloqueado_ate is not None
    db.commit()
    return bloqueado


def _limpar_falhas_login(db: Session, chave_cliente: str) -> None:
    tentativa = _obter_tentativa_login(db, chave_cliente)
    if tentativa is not None:
        db.delete(tentativa)
        db.commit()


# =========================================================
# CRIAR USUÁRIO
# =========================================================

@router.post(
    "/usuarios/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):

    usuario_existente = (
        db.query(Usuario)
        .filter(
            (Usuario.email == usuario.email) |
            (Usuario.cpf == usuario.cpf)
        )
        .first()
    )

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="E-mail ou CPF já cadastrado."
        )

    novo_usuario = Usuario(
        nome_completo=usuario.nome_completo,
        cpf=usuario.cpf,
        email=usuario.email,
        senha_hash=gerar_hash_senha(usuario.senha)
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario


# =========================================================
# LOGIN
# =========================================================

@router.post("/login")
def login(
    request: Request,
    dados: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    chave_cliente = _chave_cliente_login(request)
    _verificar_limite_login(db, chave_cliente)

    usuario = (
        db.query(Usuario)
        .filter(
            Usuario.email == dados.username.strip().lower()
        )
        .first()
    )

    if not usuario:
        verificar_senha(
            dados.password,
            _HASH_SENHA_INEXISTENTE,
        )
        bloqueado = _registrar_falha_login(db, chave_cliente)
        if bloqueado:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Muitas tentativas de login. Tente novamente mais tarde.",
                headers={"Retry-After": str(int(JANELA_FALHAS_LOGIN.total_seconds()))},
            )
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos."
        )

    senha_correta = verificar_senha(
        dados.password,
        usuario.senha_hash
    )

    if not senha_correta:
        bloqueado = _registrar_falha_login(db, chave_cliente)
        if bloqueado:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Muitas tentativas de login. Tente novamente mais tarde.",
                headers={"Retry-After": str(int(JANELA_FALHAS_LOGIN.total_seconds()))},
            )
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos."
        )

    _limpar_falhas_login(db, chave_cliente)
    token = criar_token(usuario.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =========================================================
# LISTAR USUÁRIO LOGADO
# =========================================================

@router.get(
    "/usuarios/me",
    response_model=UsuarioResponse
)
def usuario_logado(
    usuario: Usuario = Depends(obter_usuario_logado)
):

    return usuario


# =========================================================
# LISTAR USUÁRIOS
# =========================================================

@router.get(
    "/usuarios/",
    response_model=list[UsuarioResponse]
)
def listar_usuarios(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_logado)
):

    return (
        db.query(Usuario)
        .filter(Usuario.id == usuario.id)
        .offset(offset)
        .limit(limit)
        .all()
    )


# =========================================================
# BUSCAR USUÁRIO
# =========================================================

@router.get(
    "/usuarios/{usuario_id}",
    response_model=UsuarioResponse
)
def buscar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_logado)
):

    if usuario_id != usuario.id:
        raise HTTPException(
            status_code=403,
            detail="Você não pode acessar outro usuário."
        )

    usuario_encontrado = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )

    if not usuario_encontrado:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    return usuario_encontrado


# =========================================================
# EXCLUIR USUÁRIO
# =========================================================

@router.delete(
    "/usuarios/{usuario_id}"
)
def excluir_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_logado)
):

    if usuario_id != usuario.id:
        raise HTTPException(
            status_code=403,
            detail="Você não pode excluir outro usuário."
        )

    usuario_encontrado = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )

    if not usuario_encontrado:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    db.delete(usuario_encontrado)
    db.commit()

    return {
        "mensagem": "Usuário excluído com sucesso."
    }