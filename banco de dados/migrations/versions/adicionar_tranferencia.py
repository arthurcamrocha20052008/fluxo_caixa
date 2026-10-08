"""Adiciona campos para relacionar as duas pontas das transferências."""
from alembic import op
import sqlalchemy as sa


revision = "transferencias"
down_revision = "esquema_inicial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "fluxo_dinheiro",
        sa.Column("transferencia_id", sa.String(length=36), nullable=True),
    )
    op.add_column(
        "fluxo_dinheiro",
        sa.Column(
            "transferencia_direcao",
            sa.Enum("origem", "destino"),
            nullable=True,
        ),
    )
    op.add_column(
        "fluxo_dinheiro",
        sa.Column("conta_destino_id", sa.Integer(), nullable=True),
    )
    op.create_index(
        "ix_fluxo_dinheiro_transferencia_id",
        "fluxo_dinheiro",
        ["transferencia_id"],
    )
    with op.batch_alter_table("fluxo_dinheiro") as batch_op:
        batch_op.create_foreign_key(
            "fk_fluxo_conta_destino",
            "contas_bancarias",
            ["conta_destino_id"],
            ["id"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
        )


def downgrade() -> None:
    with op.batch_alter_table("fluxo_dinheiro") as batch_op:
        batch_op.drop_constraint(
            "fk_fluxo_conta_destino",
            type_="foreignkey",
        )
    op.drop_index(
        "ix_fluxo_dinheiro_transferencia_id",
        table_name="fluxo_dinheiro",
    )
    op.drop_column("fluxo_dinheiro", "conta_destino_id")
    op.drop_column("fluxo_dinheiro", "transferencia_direcao")
    op.drop_column("fluxo_dinheiro", "transferencia_id")