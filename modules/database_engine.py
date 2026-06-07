"""
Veritabanı Motoru (Database Engine)
------------------------------------
SQLite veritabanı ile tüm etkileşimi yönetir.
Tablo oluşturma, veri yazma, sorgulama ve temizleme
işlemlerini gerçekleştirir.
"""

import sqlite3
import os
from typing import List, Optional, Tuple

from modules.schema_models import TableSchema
from modules.query_generator import QueryGenerator


class DatabaseEngine:
    """SQLite veritabanı yönetim motoru."""

    def __init__(self):
        self._db_path: Optional[str] = None
        self._connection: Optional[sqlite3.Connection] = None
        self._query_gen = QueryGenerator()

    @property
    def db_path(self) -> Optional[str]:
        return self._db_path

    @property
    def is_connected(self) -> bool:
        return self._connection is not None

    def connect(self, path: str = "database.db") -> None:
        """SQLite veritabanına bağlanır. FK desteğini aktifleştirir."""
        self.close()
        self._db_path = path
        self._connection = sqlite3.connect(path)
        self._connection.execute("PRAGMA foreign_keys = ON;")
        self._connection.row_factory = sqlite3.Row

    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        """Tek bir SQL sorgusunu çalıştırır."""
        if not self._connection:
            raise ConnectionError("Veritabanı bağlantısı yok. connect() çağırın.")
        try:
            cursor = self._connection.cursor()
            cursor.execute(sql, params)
            self._connection.commit()
            return cursor
        except sqlite3.Error as e:
            self._connection.rollback()
            raise RuntimeError(f"SQL hatası: {e}\nSorgu: {sql}") from e

    def create_tables(self, schemas: List[TableSchema]) -> List[str]:
        """
        Şema listesinden tabloları oluşturur.
        Returns: Oluşturulan tablo adları listesi
        """
        created = []
        for schema in schemas:
            sql = self._query_gen.generate_create_table(schema)
            self.execute(sql)
            created.append(schema.name)
        return created

    def insert_data(self, schemas: List[TableSchema]) -> int:
        """
        Şemalardaki kayıtları tablolara yazar.
        Returns: Toplam eklenen kayıt sayısı
        """
        total = 0
        for schema in schemas:
            for idx, record in enumerate(schema.records, start=1):
                sql, params = self._query_gen.generate_insert(schema, record, idx)
                self.execute(sql, params)
                total += 1
        return total

    def drop_all_tables(self) -> List[str]:
        """Veritabanındaki tüm tabloları siler."""
        table_names = self.get_table_names()
        if not table_names:
            return []

        # FK'ları geçici olarak devre dışı bırak
        self.execute("PRAGMA foreign_keys = OFF;")
        dropped = []
        for name in table_names:
            sql = self._query_gen.generate_drop_table(name)
            self.execute(sql)
            dropped.append(name)
        self.execute("PRAGMA foreign_keys = ON;")
        return dropped

    def get_table_names(self) -> List[str]:
        """Veritabanındaki tüm tablo adlarını döndürür."""
        cursor = self.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%' ORDER BY name;"
        )
        return [row[0] for row in cursor.fetchall()]

    def fetch_table_data(self, table_name: str) -> Tuple[List[str], List[tuple]]:
        """
        Bir tablonun sütun adlarını ve tüm verilerini döndürür.
        Returns: (sütun_adları, satırlar)
        """
        cursor = self.execute(f'SELECT * FROM "{table_name}";')
        columns = [desc[0] for desc in cursor.description]
        rows = [tuple(row) for row in cursor.fetchall()]
        return columns, rows

    def get_table_info(self, table_name: str) -> List[dict]:
        """Tablo sütun bilgilerini döndürür."""
        cursor = self.execute(f'PRAGMA table_info("{table_name}");')
        return [
            {
                "cid": row[0], "name": row[1], "type": row[2],
                "notnull": row[3], "default": row[4], "pk": row[5]
            }
            for row in cursor.fetchall()
        ]

    def get_foreign_keys(self, table_name: str) -> List[dict]:
        """Tablonun FK ilişkilerini döndürür."""
        cursor = self.execute(f'PRAGMA foreign_key_list("{table_name}");')
        return [
            {"from": row[3], "table": row[2], "to": row[4]}
            for row in cursor.fetchall()
        ]

    def close(self) -> None:
        """Veritabanı bağlantısını kapatır."""
        if self._connection:
            self._connection.close()
            self._connection = None
