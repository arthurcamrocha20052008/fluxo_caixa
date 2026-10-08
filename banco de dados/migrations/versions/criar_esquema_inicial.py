"""Cria o esquema inicial do fluxo de caixa."""
from alembic import op
import sqlalchemy as sa


revision = "esquema_inicial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("nome_completo", sa.String(length=150), nullable=False),
        sa.Column("cpf", sa.String(length=11), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("senha_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "criado_em",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.UniqueConstraint("cpf"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "contas_bancarias",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("nome_banco", sa.String(length=100), nullable=False),
        sa.Column(
            "tipo_conta",
            sa.Enum("corrente", "poupanca", "investimento"),
            nullable=False,
        ),
        sa.Column(
            "valor_conta_atual",
            sa.Numeric(12, 2),
            nullable=False,
            server_default="0.00",
        ),
        sa.Column("ativa", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column(
            "criado_em",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(
            ["usuario_id"],
            ["usuarios.id"],
            name="fk_conta_usuario",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )
    op.create_index(
        "idx_contas_usuario",
        "contas_bancarias",
        ["usuario_id"],
    )
    op.create_table(
        "fluxo_dinheiro",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("conta_bancaria_id", sa.Integer(), nullable=False),
        sa.Column("descricao", sa.String(length=200), nullable=False),
        sa.Column("valor", sa.Numeric(12, 2), nullable=False),
        sa.Column(
            "tipo",
            sa.Enum("entrada", "saida", "transferencia"),
            nullable=False,
        ),
        sa.Column("categoria", sa.String(length=100), nullable=False),
        sa.Column("data_movimentacao", sa.Date(), nullable=False),
        sa.Column("observacao", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(
            ["conta_bancaria_id"],
            ["contas_bancarias.id"],
            name="fk_fluxo_conta",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )
    op.create_index("idx_fluxo_conta", "fluxo_dinheiro", ["conta_bancaria_id"])
    op.create_index("idx_fluxo_data", "fluxo_dinheiro", ["data_movimentacao"])
    op.create_index("idx_fluxo_tipo", "fluxo_dinheiro", ["tipo"])
    op.create_table(
        "calculos_financeiros",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("conta_bancaria_id", sa.Integer(), nullable=False),
        sa.Column(
            "tipo_calculo",
            sa.Enum("diario", "semanal", "mensal", "anual"),
            nullable=False,
        ),
        sa.Column("data_inicio", sa.Date(), nullable=False),
        sa.Column("data_fim", sa.Date(), nullable=False),
        sa.Column(
            "valor_original",
            sa.Numeric(12, 2),
            nullable=False,
            server_default="0.00",
        ),
        sa.Column(
            "total_entradas",
            sa.Numeric(12, 2),
            nullable=False,
            server_default="0.00",
        ),
        sa.Column(
            "total_saidas",
            sa.Numeric(12, 2),
            nullable=False,
            server_default="0.00",
        ),
        sa.Column(
            "total_investimentos",
            sa.Numeric(12, 2),
            nullable=False,
            server_default="0.00",
        ),
        sa.Column(
            "valor_final",
            sa.Numeric(12, 2),
            nullable=False,
            server_default="0.00",
        ),
        sa.Column(
            "criado_em",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(
            ["conta_bancaria_id"],
            ["contas_bancarias.id"],
            name="fk_calculo_conta",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )
    op.create_table(
        "metas_financeiras",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=150), nullable=False),
        sa.Column("valor_meta", sa.Numeric(12, 2), nullable=False),
        sa.Column(
            "valor_atual",
            sa.Numeric(12, 2),
            nullable=False,
            server_default="0.00",
        ),
        sa.Column("data_inicio", sa.Date(), nullable=False),
        sa.Column("data_limite", sa.Date(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("em_andamento", "concluida", "cancelada"),
            nullable=False,
            server_default="em_andamento",
        ),
        sa.Column("descricao", sa.String(length=255), nullable=True),
        sa.Column(
            "criado_em",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(
            ["usuario_id"],
            ["usuarios.id"],
            name="fk_meta_usuario",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )


def downgrade() -> None:
    op.drop_table("metas_financeiras")
    op.drop_table("calculos_financeiros")
    op.drop_index("idx_fluxo_tipo", table_name="fluxo_dinheiro")
    op.drop_index("idx_fluxo_data", table_name="fluxo_dinheiro")
    op.drop_index("idx_fluxo_conta", table_name="fluxo_dinheiro")
    op.drop_table("fluxo_dinheiro")
    op.drop_index("idx_contas_usuario", table_name="contas_bancarias")
    op.drop_table("contas_bancarias")
    op.drop_table("usuarios")