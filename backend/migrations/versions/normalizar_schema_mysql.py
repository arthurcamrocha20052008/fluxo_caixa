"""Normalizes legacy MySQL column types and indexes to the mapped schema."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


revision = "normalizar_schema"
down_revision = "limite_login"
branch_labels = None
depends_on = None


TIMESTAMP_COLUMNS = (
    "usuarios",
    "contas_bancarias",
    "calculos_financeiros",
    "metas_financeiras",
)

FOREIGN_KEY_INDEXES = (
    ("calculos_financeiros", "idx_calculo_conta", ["conta_bancaria_id"]),
    ("metas_financeiras", "idx_metas_usuario", ["usuario_id"]),
)

OBSOLETE_INDEXES = (
    (
        "calculos_financeiros",
        "idx_calculo_periodo",
        ["data_inicio", "data_fim"],
    ),
)


def _change_created_at_type(
    table_name: str,
    source_type: type,
    target_type: type,
) -> None:
    bind = op.get_bind()
    column = next(
        item
        for item in sa.inspect(bind).get_columns(table_name)
        if item["name"] == "criado_em"
    )
    if not isinstance(column["type"], source_type):
        return

    default = column["default"]
    server_default = sa.text(default) if default else None
    op.alter_column(
        table_name,
        "criado_em",
        existing_type=column["type"],
        type_=target_type(),
        existing_nullable=column["nullable"],
        existing_server_default=server_default,
        server_default=server_default,
    )


def _index_exists(table_name: str, index_name: str) -> bool:
    return any(
        index["name"] == index_name
        for index in sa.inspect(op.get_bind()).get_indexes(table_name)
    )


def _ensure_foreign_key_index(
    table_name: str,
    index_name: str,
    columns: list[str],
) -> None:
    indexes = sa.inspect(op.get_bind()).get_indexes(table_name)
    if any(index["name"] == index_name for index in indexes):
        return

    matching_index = next(
        (
            index
            for index in indexes
            if index["column_names"] == columns and not index["unique"]
        ),
        None,
    )
    if matching_index is None:
        op.create_index(index_name, table_name, columns)
    elif op.get_bind().dialect.name == "mysql":
        op.execute(
            sa.text(
                f"ALTER TABLE `{table_name}` RENAME INDEX "
                f"`{matching_index['name']}` TO `{index_name}`"
            )
        )


def upgrade() -> None:
    for table_name in TIMESTAMP_COLUMNS:
        _change_created_at_type(
            table_name,
            mysql.TIMESTAMP,
            sa.DateTime,
        )

    for table_name, index_name, columns in FOREIGN_KEY_INDEXES:
        _ensure_foreign_key_index(table_name, index_name, columns)

    for table_name, index_name, _ in OBSOLETE_INDEXES:
        if _index_exists(table_name, index_name):
            op.drop_index(index_name, table_name=table_name)


def downgrade() -> None:
    for table_name, index_name, columns in OBSOLETE_INDEXES:
        if not _index_exists(table_name, index_name):
            op.create_index(index_name, table_name, columns)

    for table_name in TIMESTAMP_COLUMNS:
        _change_created_at_type(
            table_name,
            sa.DateTime,
            mysql.TIMESTAMP,
        )
