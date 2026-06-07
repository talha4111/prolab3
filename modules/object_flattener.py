"""
Obje Düzleştirici (Object Flattener)
--------------------------------------
İç içe geçmiş (nested) JSON objelerini, 'ebeveyn_cocuk'
formatında düzleştirerek tek bir satır düzlemine indirir.

Örnek:
    Girdi:  {"adres": {"sehir": "Kocaeli", "ilce": "İzmit"}}
    Çıktı:  {"adres_sehir": "Kocaeli", "adres_ilce": "İzmit"}
"""

from typing import Any, Dict, List, Tuple


class ObjectFlattener:
    """
    Nested dict yapılarını düzleştirir.
    Array alanlarını düzleştirmez, bunları ayrı tutar (ArrayHandler'a bırakır).
    """

    def __init__(self, separator: str = "_"):
        """
        Args:
            separator: Ebeveyn ve çocuk anahtar adlarını birleştiren ayırıcı karakter.
                       Varsayılan: '_' (ebeveyn_cocuk)
        """
        self._separator = separator

    def flatten(self, obj: dict, prefix: str = "") -> Tuple[Dict[str, Any], List[Tuple[str, list]]]:
        """
        Bir dict objesini düzleştirir.
        
        Primitif değerler düzleştirilmiş anahtarlarla döner.
        Array değerler ayrı bir listede toplanır (child table olacaklar).
        
        Args:
            obj: Düzleştirilecek dict objesi
            prefix: Anahtar öneki (recursive çağrılarda ebeveyn adı)
            
        Returns:
            Tuple:
                - flat_data: Düzleştirilmiş {anahtar: değer} dict'i
                - arrays: [(array_adı, array_verisi)] listesi
        """
        flat_data = {}
        arrays = []
        self._recursive_flatten(obj, prefix, flat_data, arrays)
        return flat_data, arrays

    def _recursive_flatten(
        self,
        obj: dict,
        prefix: str,
        flat_result: Dict[str, Any],
        array_result: List[Tuple[str, list]]
    ) -> None:
        """
        Rekürsif düzleştirme algoritması.
        
        - Primitif değerler: flat_result'a eklenir
        - Dict değerler: rekürsif olarak tekrar düzleştirilir
        - List değerler: array_result'a eklenir (ayrı tablo olacak)
        
        Args:
            obj: İşlenecek dict
            prefix: Mevcut anahtar öneki
            flat_result: Düzleştirilmiş sonuçların toplandığı dict
            array_result: Array'lerin toplandığı liste
        """
        for key, value in obj.items():
            # Yeni anahtar adı: prefix varsa ebeveyn_cocuk, yoksa sadece anahtar
            full_key = f"{prefix}{self._separator}{key}" if prefix else key

            if isinstance(value, dict):
                # İç içe obje: rekürsif düzleştir
                self._recursive_flatten(value, full_key, flat_result, array_result)

            elif isinstance(value, list):
                # Dizi: düzleştirme, ayrı tabloya yönlendir
                array_result.append((full_key, value))

            else:
                # Primitif değer (str, int, float, bool, None): doğrudan ekle
                flat_result[full_key] = value

    def flatten_simple(self, obj: dict, prefix: str = "") -> dict:
        """
        Basitleştirilmiş düzleştirme — sadece primitif değerleri döner,
        array'leri yok sayar. Test ve hata ayıklama için kullanışlıdır.
        
        Args:
            obj: Düzleştirilecek dict objesi
            prefix: Anahtar öneki
            
        Returns:
            Düzleştirilmiş {anahtar: değer} dict'i (sadece primitifler)
        """
        flat_data, _ = self.flatten(obj, prefix)
        return flat_data
