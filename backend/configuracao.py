import os
from pathlib import Path

from dotenv import load_dotenv


def carregar_configuracao() -> None:
    local_app_data = os.getenv("LOCALAPPDATA")
    if local_app_data:
        arquivo_segredos = (
            Path(local_app_data) / "fluxo_caixa" / "secrets.env"
        )
        if arquivo_segredos.is_file():
            load_dotenv(arquivo_segredos, override=False)

    load_dotenv(override=False)
