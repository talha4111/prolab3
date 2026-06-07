"""
Tip Dedektörü (Type Detector)
-----------------------------
JSON değerlerinin Python tiplerini tespit eder ve
karşılık gelen SQL veri tipine dönüştürür.
Karma tipli dizilerde en geniş ortak tipi seçer.
"""

from typing import Any


class TypeDetector:
    """JSON değerlerinden SQL veri tiplerini otonom olarak belirler."""

    # Python tipi -> SQL tipi eşleme tablosu
    _TYPE_MAP = {
        "str": "TEXT",
        "int": "INTEGER",
        "float": "REAL",
        "bool": "INTEGER",   # SQLite'da boolean, 0/1 integer olarak saklanır
        "NoneType": "TEXT",   # None değerler TEXT olarak varsayılır
    }

    # Tip öncelik sırası (daha geniş tip daha yüksek)
    _TYPE_PRIORITY = {
        "INTEGER": 1,
        "REAL": 2,
        "TEXT": 3,
    }

    @staticmethod
    def detect_type(value: Any) -> str:
        """
        Bir Python değerinin tip adını döndürür.
        
        Args:
            value: Tip tespiti yapılacak değer
            
        Returns:
            Tip adı ('str', 'int', 'float', 'bool', 'dict', 'list', 'NoneType')
        """
        return type(value).__name__

    @classmethod
    def map_to_sql_type(cls, value: Any) -> str:
        """
        Python değerini uygun SQL veri tipine dönüştürür.
        
        Args:
            value: Dönüştürülecek Python değeri
            
        Returns:
            SQL veri tipi ('TEXT', 'INTEGER', 'REAL')
        """
        py_type = cls.detect_type(value)
        return cls._TYPE_MAP.get(py_type, "TEXT")

    @staticmethod
    def is_primitive(value: Any) -> bool:
        """Değerin primitif (basit) bir tip olup olmadığını kontrol eder."""
        return isinstance(value, (str, int, float, bool)) or value is None

    @staticmethod
    def is_object(value: Any) -> bool:
        """Değerin bir dict (obje) olup olmadığını kontrol eder."""
        return isinstance(value, dict)

    @staticmethod
    def is_array(value: Any) -> bool:
        """Değerin bir list (dizi) olup olmadığını kontrol eder."""
        return isinstance(value, list)

    @classmethod
    def merge_types(cls, type1: str, type2: str) -> str:
        """
        İki SQL tipini birleştirir: daha geniş olan tipi seçer.
        Karma veri tiplerinde veri kaybını önlemek için kullanılır.
        
        Örnek: INTEGER + REAL = REAL, REAL + TEXT = TEXT
        
        Args:
            type1: İlk SQL tipi
            type2: İkinci SQL tipi
            
        Returns:
            Birleştirilmiş (en geniş) SQL tipi
        """
        if type1 == type2:
            return type1

        p1 = cls._TYPE_PRIORITY.get(type1, 3)
        p2 = cls._TYPE_PRIORITY.get(type2, 3)

        return type1 if p1 >= p2 else type2

    @classmethod
    def infer_sql_type_from_values(cls, values: list) -> str:
        """
        Bir değer listesindeki tüm elemanları inceleyerek
        en uygun SQL tipini belirler.
        
        Args:
            values: Tip çıkarımı yapılacak değer listesi
            
        Returns:
            Tüm değerleri kapsayan SQL tipi
        """
        if not values:
            return "TEXT"

        result_type = None
        for val in values:
            if val is None:
                continue
            sql_type = cls.map_to_sql_type(val)
            if result_type is None:
                result_type = sql_type
            else:
                result_type = cls.merge_types(result_type, sql_type)

        return result_type or "TEXT"
