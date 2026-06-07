"""
JSON Analizci (Json Analyzer) — Projenin Beyni
-----------------------------------------------
Yapısı bilinmeyen JSON verisini rekürsif olarak tarar,
tablo şemalarını dinamik olarak oluşturur.

Sorumlulukları:
  1. Kök yapıyı tanıma (dict vs list)
  2. Primitif alanları sütunlara dönüştürme
  3. Nested objeleri düzleştirme (ObjectFlattener)
  4. Dizileri tespit edip alt tablo oluşturma (ArrayHandler)
  5. Tüm tabloları PK/FK ilişkileriyle birbirine bağlama
"""

from typing import Any, Dict, List, Optional, Tuple, Union

from modules.schema_models import TableSchema, ColumnDefinition, ForeignKey
from modules.type_detector import TypeDetector
from modules.object_flattener import ObjectFlattener
from modules.array_handler import ArrayHandler


class JsonAnalyzer:
    """
    JSON verisini analiz ederek ilişkisel SQL şemasına dönüştüren
    ana orkestratör sınıf.
    """

    def __init__(self):
        self._type_detector = TypeDetector()
        self._flattener = ObjectFlattener(separator="_")
        self._array_handler = ArrayHandler()
        self._schemas: Dict[str, TableSchema] = {}
        self._id_counters: Dict[str, int] = {}

    def analyze(self, data: Union[dict, list], table_name: str = "root") -> List[TableSchema]:
        """
        JSON verisini analiz eder ve tablo şemalarını üretir.
        
        Bu metod projenin kalbidir. Gelen verinin tipine göre
        rekürsif analiz başlatır ve tüm tabloları oluşturur.
        
        Args:
            data: JSON verisi (dict veya list)
            table_name: Kök tablo adı (varsayılan: 'root')
            
        Returns:
            Oluşturulan tüm tablo şemalarının listesi
        """
        # Önceki analiz sonuçlarını temizle
        self._schemas.clear()
        self._id_counters.clear()

        if isinstance(data, dict):
            # Tek bir kayıt — dict
            self._process_single_record(data, table_name, parent_fk=None)

        elif isinstance(data, list):
            # Birden fazla kayıt — list of dicts
            if data and isinstance(data[0], dict):
                for item in data:
                    self._process_single_record(item, table_name, parent_fk=None)
            else:
                # Primitif liste kök seviyede — basit tablo
                schema = self._get_or_create_schema(table_name)
                for item in data:
                    record_id = self._next_id(table_name)
                    schema.add_column(ColumnDefinition(
                        name="value",
                        sql_type=self._type_detector.map_to_sql_type(item)
                    ))
                    schema.add_record({"value": item})

        return list(self._schemas.values())

    def _process_single_record(
        self,
        record: dict,
        table_name: str,
        parent_fk: Optional[Tuple[str, int]] = None
    ) -> int:
        """
        Tek bir JSON kaydını (dict) işler.
        
        Adımlar:
          1. Tablo şemasını oluştur/al
          2. Kaydı düzleştir (nested objeler için)
          3. Primitif alanları sütun olarak ekle
          4. Dizileri tespit et ve alt tablolar oluştur
          5. Kaydı tablonun records listesine ekle
        
        Args:
            record: İşlenecek JSON kaydı (dict)
            table_name: Bu kaydın ait olduğu tablo adı
            parent_fk: Ebeveyn FK bilgisi (sütun_adı, parent_id) — opsiyonel
            
        Returns:
            Bu kaydın atanan ID'si
        """
        schema = self._get_or_create_schema(table_name)
        record_id = self._next_id(table_name)

        # Düzleştir: nested objeler → flat alanlar, diziler → ayrı liste
        flat_data, arrays = self._flattener.flatten(record)

        # Flat veriyi kayıt olarak hazırla
        row = {}

        # Ebeveyn FK varsa ekle
        if parent_fk:
            fk_col_name, fk_value = parent_fk
            row[fk_col_name] = fk_value

        # Primitif alanları sütunlara ekle
        for key, value in flat_data.items():
            sql_type = self._type_detector.map_to_sql_type(value)
            safe_key = self._sanitize_column_name(key)

            # Sütun tipi çakışması kontrolü (farklı kayıtlarda farklı tipler)
            if schema.has_column(safe_key):
                # Mevcut sütunun tipini genişlet (gerekirse)
                existing_col = next(c for c in schema.columns if c.name == safe_key)
                merged = self._type_detector.merge_types(existing_col.sql_type, sql_type)
                if merged != existing_col.sql_type:
                    schema.update_column_type(safe_key, merged)
            else:
                schema.add_column(ColumnDefinition(
                    name=safe_key,
                    sql_type=sql_type,
                    nullable=True
                ))

            row[safe_key] = value

        # Kaydı tabloya ekle
        schema.add_record(row)

        # Dizileri işle → alt tablolar oluştur
        for array_name, array_data in arrays:
            self._process_array(
                array_data=array_data,
                array_name=array_name,
                parent_table=table_name,
                parent_id=record_id
            )

        return record_id

    def _process_array(
        self,
        array_data: list,
        array_name: str,
        parent_table: str,
        parent_id: int
    ) -> None:
        """
        Bir JSON dizisini analiz eder ve uygun alt tabloyu oluşturur.
        
        Primitif dizi: (parent_id, value) formatında basit alt tablo
        Obje dizisi: Her obje bir kayıt, rekürsif analiz (derinlik)
        
        Args:
            array_data: Dizi verisi
            array_name: Dizinin anahtar adı (tablo adı olarak kullanılır)
            parent_table: Ebeveyn tablo adı
            parent_id: Ebeveyn kaydın ID'si
        """
        if not array_data:
            return

        # Alt tablo adı: ebeveyn_dizi formatı
        child_table_name = self._sanitize_table_name(array_name)

        # Dizi tipini sınıflandır
        array_type = self._array_handler.classify_array(array_data)

        # FK sütun adı
        fk_column = f"{parent_table}_id"

        # Alt tablo şemasını oluştur ve FK ekle
        child_schema = self._get_or_create_schema(child_table_name)

        # FK ilişkisi kur (sadece bir kez)
        if not any(fk.ref_table == parent_table for fk in child_schema.foreign_keys):
            child_schema.add_foreign_key(ForeignKey(
                column=fk_column,
                ref_table=parent_table,
                ref_column="id"
            ))

        if array_type == "primitive":
            # Primitif dizi: her eleman → (parent_id, value) kaydı
            records = self._array_handler.extract_primitive_records(array_data, parent_id)
            for rec in records:
                child_id = self._next_id(child_table_name)

                # value sütununu ekle
                value = rec.get("value")
                sql_type = self._type_detector.map_to_sql_type(value)

                if child_schema.has_column("value"):
                    existing = next(c for c in child_schema.columns if c.name == "value")
                    merged = self._type_detector.merge_types(existing.sql_type, sql_type)
                    if merged != existing.sql_type:
                        child_schema.update_column_type("value", merged)
                else:
                    child_schema.add_column(ColumnDefinition(
                        name="value",
                        sql_type=sql_type,
                        nullable=True
                    ))

                child_schema.add_record({
                    fk_column: parent_id,
                    "value": value
                })

        elif array_type in ("object", "mixed"):
            # Obje dizisi: her objeyi rekürsif işle
            for item in array_data:
                if isinstance(item, dict):
                    self._process_single_record(
                        record=item,
                        table_name=child_table_name,
                        parent_fk=(fk_column, parent_id)
                    )
                else:
                    # Non-dict eleman (mixed array) — primitif gibi ele al
                    child_id = self._next_id(child_table_name)
                    sql_type = self._type_detector.map_to_sql_type(item)

                    if not child_schema.has_column("value"):
                        child_schema.add_column(ColumnDefinition(
                            name="value", sql_type=sql_type, nullable=True
                        ))

                    child_schema.add_record({
                        fk_column: parent_id,
                        "value": item
                    })

    def _get_or_create_schema(self, table_name: str) -> TableSchema:
        """Mevcut şemayı döndürür veya yeni bir tane oluşturur."""
        if table_name not in self._schemas:
            self._schemas[table_name] = TableSchema(name=table_name)
            self._id_counters[table_name] = 0
        return self._schemas[table_name]

    def _next_id(self, table_name: str) -> int:
        """Belirtilen tablo için bir sonraki ID değerini üretir."""
        if table_name not in self._id_counters:
            self._id_counters[table_name] = 0
        self._id_counters[table_name] += 1
        return self._id_counters[table_name]

    @staticmethod
    def _sanitize_column_name(name: str) -> str:
        """
        Sütun adını SQL uyumlu hale getirir.
        Özel karakterleri alt çizgi ile değiştirir.
        """
        sanitized = name.replace(" ", "_").replace("-", "_").replace(".", "_")
        sanitized = ''.join(c if c.isalnum() or c == '_' else '_' for c in sanitized)
        # Sayıyla başlıyorsa önüne _ ekle
        if sanitized and sanitized[0].isdigit():
            sanitized = f"_{sanitized}"
        return sanitized.lower()

    @staticmethod
    def _sanitize_table_name(name: str) -> str:
        """
        Tablo adını SQL uyumlu hale getirir.
        """
        sanitized = name.replace(" ", "_").replace("-", "_").replace(".", "_")
        sanitized = ''.join(c if c.isalnum() or c == '_' else '_' for c in sanitized)
        if sanitized and sanitized[0].isdigit():
            sanitized = f"tbl_{sanitized}"
        return sanitized.lower()

    def get_schemas(self) -> Dict[str, TableSchema]:
        """Tüm oluşturulan şemaları döndürür."""
        return self._schemas

    def reset(self) -> None:
        """Analizciyi sıfırlar."""
        self._schemas.clear()
        self._id_counters.clear()
