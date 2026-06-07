"""
Sorgu Üretici (Query Generator)
--------------------------------
TableSchema nesnelerinden dinamik SQL sorguları üretir.
"""

from typing import List, Tuple
from modules.schema_models import TableSchema


class QueryGenerator:
    """SQL sorgularını dinamik olarak üreten sınıf."""

    @staticmethod
    def generate_create_table(schema: TableSchema) -> str:
        """CREATE TABLE sorgusu üretir (AUTOINCREMENT PK, FK REFERENCES)."""
        lines = []
        for col in schema.columns:
            col_def = f'    "{col.name}" {col.sql_type}'
            if col.is_primary_key:
                col_def += " PRIMARY KEY AUTOINCREMENT"
            elif not col.nullable:
                col_def += " NOT NULL"
            lines.append(col_def)

        for fk in schema.foreign_keys:
            lines.append(
                f'    FOREIGN KEY ("{fk.column}") '
                f'REFERENCES "{fk.ref_table}" ("{fk.ref_column}")'
            )
        columns_sql = ",\n".join(lines)
        return f'CREATE TABLE IF NOT EXISTS "{schema.name}" (\n{columns_sql}\n);'

    @staticmethod
    def generate_insert(schema: TableSchema, record: dict, record_id: int) -> Tuple[str, tuple]:
        """Parametrik INSERT INTO sorgusu ve değerleri üretir."""
        col_names = ['"id"']
        placeholders = ["?"]
        values = [record_id]

        for col in schema.columns:
            if col.is_primary_key:
                continue
            col_names.append(f'"{col.name}"')
            placeholders.append("?")
            values.append(record.get(col.name))

        sql = (
            f'INSERT INTO "{schema.name}" '
            f'({", ".join(col_names)}) '
            f'VALUES ({", ".join(placeholders)})'
        )
        return sql, tuple(values)

    @staticmethod
    def generate_drop_table(table_name: str) -> str:
        """DROP TABLE sorgusu üretir."""
        return f'DROP TABLE IF EXISTS "{table_name}";'

    @staticmethod
    def generate_drop_all(table_names: List[str]) -> List[str]:
        """Tüm tabloları silen DROP sorgularını ters sırada üretir."""
        return [f'DROP TABLE IF EXISTS "{name}";' for name in reversed(table_names)]

    @staticmethod
    def generate_select_all(table_name: str) -> str:
        """SELECT * sorgusu üretir."""
        return f'SELECT * FROM "{table_name}";'
