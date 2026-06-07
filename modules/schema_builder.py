"""
Şema Oluşturucu (Schema Builder)
----------------------------------
JsonAnalyzer'ın ürettiği ham şemaları alır,
son doğrulamaları yapar ve SQL üretimine hazır
hale getirir.
"""

from typing import Dict, List

from modules.schema_models import TableSchema, ColumnDefinition


class SchemaBuilder:
    """Analiz sonuçlarından son şema yapısını oluşturur."""

    def __init__(self):
        self._schemas: Dict[str, TableSchema] = {}

    def build(self, analysis_result: List[TableSchema]) -> List[TableSchema]:
        """
        Analiz sonuçlarını alır, doğrular ve SQL'e hazır şemaları oluşturur.
        
        İşlemler:
          1. PK sütununu ekle (yoksa)
          2. Sütun sıralamasını düzenle (PK → FK'ler → normal sütunlar)
          3. Boş tabloları temizle
        
        Args:
            analysis_result: JsonAnalyzer'dan gelen TableSchema listesi
            
        Returns:
            SQL üretimine hazır TableSchema listesi
        """
        self._schemas.clear()
        result = []

        for schema in analysis_result:
            processed = self._process_schema(schema)
            if processed:
                self._schemas[processed.name] = processed
                result.append(processed)

        # Tabloları sırala: parent tablolar önce (FK bağımlılığı)
        return self._topological_sort(result)

    def _process_schema(self, schema: TableSchema) -> TableSchema:
        """
        Tek bir tablo şemasını işler ve doğrular.
        
        Args:
            schema: İşlenecek tablo şeması
            
        Returns:
            İşlenmiş tablo şeması (veya None — boşsa)
        """
        # Boş tabloyu atla
        if not schema.records:
            return None

        # PK sütunu ekle (ilk sütun olarak)
        pk_col = ColumnDefinition(
            name="id",
            sql_type="INTEGER",
            nullable=False,
            is_primary_key=True
        )

        # Sütunları yeniden sırala: PK → FK'ler → normal
        ordered_columns = [pk_col]

        # FK sütunları
        fk_names = {fk.column for fk in schema.foreign_keys}
        for col in schema.columns:
            if col.name in fk_names and col.name != "id":
                ordered_columns.append(col)

        # Normal sütunlar
        for col in schema.columns:
            if col.name not in fk_names and col.name != "id":
                ordered_columns.append(col)

        schema.columns = ordered_columns

        return schema

    def _topological_sort(self, schemas: List[TableSchema]) -> List[TableSchema]:
        """
        Tabloları FK bağımlılık sırasına göre sıralar.
        Parent tablolar child tablolardan önce gelir.
        (CREATE TABLE sıralaması için gerekli)
        
        Args:
            schemas: Sıralanacak tablo şemaları
            
        Returns:
            Bağımlılık sırasına göre sıralanmış şemalar
        """
        schema_map = {s.name: s for s in schemas}
        visited = set()
        result = []

        def visit(name: str):
            if name in visited:
                return
            visited.add(name)

            schema = schema_map.get(name)
            if schema:
                # Önce bağımlılıkları ziyaret et
                for fk in schema.foreign_keys:
                    if fk.ref_table in schema_map:
                        visit(fk.ref_table)
                result.append(schema)

        for schema in schemas:
            visit(schema.name)

        return result

    def get_schema(self, name: str) -> TableSchema:
        """İsme göre tablo şeması döndürür."""
        return self._schemas.get(name)

    def get_all_schemas(self) -> List[TableSchema]:
        """Tüm şemaları döndürür."""
        return list(self._schemas.values())

    def reset(self) -> None:
        """Builder'ı sıfırlar."""
        self._schemas.clear()
