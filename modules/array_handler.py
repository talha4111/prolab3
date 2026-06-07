"""
Dizi Yöneticisi (Array Handler)
--------------------------------
JSON dizilerini (array) tespit eder ve SQL normalizasyon
kurallarına (1NF) uygun olarak alt tablo (child table) yapılarına
dönüştürülmek üzere hazırlar.

İki tür dizi desteklenir:
  1. Primitif Dizi: ["a", "b", "c"] → (parent_id, value) formatında alt tablo
  2. Obje Dizisi: [{...}, {...}] → her obje bir kayıt olarak alt tabloya yazılır
"""

from typing import Any, List, Tuple

from modules.type_detector import TypeDetector


class ArrayHandler:
    """JSON dizilerini analiz eder ve alt tablo oluşturma kararları verir."""

    def __init__(self):
        self._type_detector = TypeDetector()

    def should_create_child_table(self, arr: list) -> bool:
        """
        Bir dizinin alt tablo gerektirip gerektirmediğine karar verir.
        
        Boş diziler için tablo oluşturulmaz.
        Primitif ve obje dizileri için tablo oluşturulur.
        
        Args:
            arr: Kontrol edilecek dizi
            
        Returns:
            True: Alt tablo oluşturulmalı, False: Oluşturulmamalı
        """
        if not arr:
            return False
        return True

    def classify_array(self, arr: list) -> str:
        """
        Bir dizinin içerik tipini sınıflandırır.
        
        Args:
            arr: Sınıflandırılacak dizi
            
        Returns:
            'primitive': Basit değerler dizisi
            'object': Obje dizisi
            'mixed': Karışık tip dizisi
            'empty': Boş dizi
        """
        if not arr:
            return "empty"

        has_primitive = False
        has_object = False

        for item in arr:
            if isinstance(item, dict):
                has_object = True
            elif isinstance(item, list):
                # İç içe dizi — obje gibi ele alınır
                has_object = True
            else:
                has_primitive = True

        if has_primitive and has_object:
            return "mixed"
        elif has_object:
            return "object"
        else:
            return "primitive"

    def extract_primitive_records(
        self, arr: list, parent_id: int
    ) -> List[dict]:
        """
        Primitif bir diziyi alt tablo kayıtlarına dönüştürür.
        
        Örnek:
            arr = ["Matematik", "Fizik"], parent_id = 1
            Çıktı: [
                {"parent_id": 1, "value": "Matematik"},
                {"parent_id": 1, "value": "Fizik"}
            ]
        
        Args:
            arr: Primitif değerler dizisi
            parent_id: Ebeveyn kaydın ID'si
            
        Returns:
            Alt tablo kayıtları listesi
        """
        records = []
        for item in arr:
            records.append({
                "parent_id": parent_id,
                "value": item
            })
        return records

    def extract_object_records(
        self, arr: list, parent_id: int
    ) -> List[dict]:
        """
        Obje dizisini alt tablo kayıtlarına dönüştürür.
        Her objenin alanları korunur ve parent_id eklenir.
        
        Örnek:
            arr = [{"ad": "Fizik", "kredi": 4}], parent_id = 1
            Çıktı: [{"parent_id": 1, "ad": "Fizik", "kredi": 4}]
        
        Args:
            arr: Obje dizisi
            parent_id: Ebeveyn kaydın ID'si
            
        Returns:
            Alt tablo kayıtları listesi
        """
        records = []
        for item in arr:
            if isinstance(item, dict):
                record = {"parent_id": parent_id}
                record.update(item)
                records.append(record)
            else:
                # Karma/non-dict eleman — primitif gibi ele al
                records.append({
                    "parent_id": parent_id,
                    "value": item
                })
        return records

    def detect_arrays(self, data: dict) -> List[Tuple[str, list]]:
        """
        Bir dict içindeki tüm dizi (array) alanlarını tespit eder.
        Sadece birinci seviyedeki dizileri döndürür.
        
        Args:
            data: Taranacak dict
            
        Returns:
            [(anahtar_adı, dizi_verisi)] listesi
        """
        arrays = []
        for key, value in data.items():
            if isinstance(value, list):
                arrays.append((key, value))
        return arrays
