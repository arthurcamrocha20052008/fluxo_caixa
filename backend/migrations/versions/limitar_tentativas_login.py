"""Cria persistência para limitar falhas de login por cliente."""
from alembic import op
import sqlalchemy as sa


revision = "limite_login"
down_revision = "ajustes_e_resumos"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tentativas_login",
        sa.Column("chave_cliente", sa.String(length=64), primary_key=True),
        sa.Column("tentativas", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("inicio_janela", sa.DateTime(), nullable=False),
        sa.Column("bloqueado_ate", sa.DateTime(), nullable=True),
    )
    op.create_index(
        "idx_tentativas_login_janela",
        "tentativas_login",
        ["inicio_janela"],
    )


def downgrade() -> None:
    op.drop_index(
        "idx_tentativas_login_janela",
        table_name="tentativas_login",
    )
    op.drop_table("tentativas_login")
