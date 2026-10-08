from pwdlib import PasswordHash


# =========================================================
# CONFIGURAÇÃO DE SENHAS
# =========================================================

password_hash = PasswordHash.recommended()


# =========================================================
# GERAR HASH DA SENHA
# =========================================================

def gerar_hash_senha(senha: str) -> str:
    """
    Transforma a senha original em um hash seguro
    para ser armazenado no banco de dados.
    """

    return password_hash.hash(senha)


# =========================================================
# VERIFICAR SENHA
# =========================================================

def verificar_senha(senha: str, senha_hash: str) -> bool:
    """
    Verifica se a senha informada corresponde
    ao hash armazenado no banco.
    """

    return password_hash.verify(
        senha,
        senha_hash
    )