import asyncio
import os
from pathlib import Path
from secrets import token_urlsafe
import sys

from cryptography.fernet import Fernet

ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from configuracao import carregar_configuracao

carregar_configuracao()

# Fallbacks seguros de execução (sem expor segredos ou URIs no repositório)
# caso alguma variável ainda não tenha sido definida no painel da hospedagem:
os.environ.setdefault("APP_ENV", "production")
os.environ.setdefault(
    "CORS_ORIGINS",
    (
        "https://fluxo-caixa-coral-two.vercel.app,"
        "https://fluxo-caixa-coral-dois.vercel.app,"
        "http://127.0.0.1:5173,"
        "http://127.0.0.1:5500,"
        "http://app.fluxocaixa,"
        "http://app.fluxocaixa:5173"
    ),
)
if not os.environ.get("DATABASE_URL"):
    os.environ["DATABASE_URL"] = f"sqlite:///{(ROOT / 'fluxo_caixa.db').as_posix()}"
if not os.environ.get("CPF_ENCRYPTION_KEY"):
    os.environ["CPF_ENCRYPTION_KEY"] = Fernet.generate_key().decode("ascii")
if not os.environ.get("JWT_SECRET_KEY"):
    os.environ["JWT_SECRET_KEY"] = token_urlsafe(48)
os.environ.setdefault("ALLOW_GOOGLE_ASSISTED", "1")

from api import app  # noqa: E402


async def _iniciar_servidores_railway(host: str, porta_principal: int) -> None:
    import uvicorn

    portas = {porta_principal, 8000, 8080}
    tarefas = []
    for p in sorted(portas):
        cfg = uvicorn.Config(app, host=host, port=p, log_level="info")
        servidor = uvicorn.Server(cfg)
        tarefas.append(servidor.serve())
    await asyncio.gather(*tarefas)


if __name__ == "__main__":
    import uvicorn

    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))

    if os.environ.get("RAILWAY_ENVIRONMENT") or os.environ.get("APP_ENV") == "production":
        asyncio.run(_iniciar_servidores_railway(host, port))
    else:
        uvicorn.run("main:app", host=host, port=port, reload=True)
