from pwdlib import PasswordHash


# =========================================================
# CONFIGURAÇÃO DE SENHAS
# =========================================================

password_hash = PasswordHash.recommended()


# =========================================================
# GERAR HASH DA SENHA
# =========================================================

def gerar_hash_senha(senha: str) -> str:
    return password_hash.hash(senha)


# =========================================================
# VERIFICAR SENHA
# =========================================================

def verificar_senha(senha: str, senha_hash: str) -> bool:
    return password_hash.verify(senha, senha_hash)