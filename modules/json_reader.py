"""
JSON Dosya Okuyucu (Json File Reader)
--------------------------------------
Kullanıcının seçtiği JSON dosyasını güvenli şekilde
belleğe okur ve geçerliliğini doğrular.
Encoding sorunları ve bozuk JSON yapıları için
kapsamlı hata yakalama sağlar.
"""

import json
import os
from typing import Any, Optional, Union


class JsonFileReader:
    """JSON dosyalarını okur ve doğrular."""

    def __init__(self):
        self._file_path: Optional[str] = None
        self._raw_data: Optional[Union[dict, list]] = None
        self._raw_text: Optional[str] = None

    @property
    def file_path(self) -> Optional[str]:
        """Yüklenen dosyanın yolunu döndürür."""
        return self._file_path

    @property
    def raw_data(self) -> Optional[Union[dict, list]]:
        """Çözümlenmiş JSON verisini döndürür."""
        return self._raw_data

    @property
    def raw_text(self) -> Optional[str]:
        """Ham JSON metnini döndürür."""
        return self._raw_text

    def load_file(self, path: str) -> Union[dict, list]:
        """
        Belirtilen yoldaki JSON dosyasını okur ve çözümler.
        
        Args:
            path: JSON dosyasının tam yolu
            
        Returns:
            Çözümlenmiş JSON verisi (dict veya list)
            
        Raises:
            FileNotFoundError: Dosya bulunamazsa
            ValueError: Geçersiz JSON formatı
            IOError: Dosya okunamıyorsa
        """
        # Dosya varlık kontrolü
        if not os.path.exists(path):
            raise FileNotFoundError(f"Dosya bulunamadı: {path}")

        # Uzantı kontrolü
        if not path.lower().endswith('.json'):
            raise ValueError(f"Geçersiz dosya uzantısı. Sadece .json dosyaları kabul edilir: {path}")

        # Dosyayı oku — birden fazla encoding dene
        raw_text = self._read_with_encoding(path)

        # JSON çözümleme
        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Geçersiz JSON formatı: Satır {e.lineno}, Sütun {e.colno} — {e.msg}"
            ) from e

        # Tip kontrolü: kök eleman dict veya list olmalı
        if not isinstance(data, (dict, list)):
            raise ValueError(
                f"JSON kök elemanı dict veya list olmalıdır, "
                f"ancak {type(data).__name__} bulundu."
            )

        self._file_path = path
        self._raw_data = data
        self._raw_text = raw_text

        return data

    def _read_with_encoding(self, path: str) -> str:
        """
        Dosyayı birden fazla encoding ile okumayı dener.
        
        Args:
            path: Dosya yolu
            
        Returns:
            Dosyanın metin içeriği
            
        Raises:
            IOError: Hiçbir encoding ile okunamıyorsa
        """
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1254']

        for encoding in encodings:
            try:
                with open(path, 'r', encoding=encoding) as f:
                    return f.read()
            except (UnicodeDecodeError, UnicodeError):
                continue

        raise IOError(
            f"Dosya okunamıyor. Desteklenen encodinglerden "
            f"hiçbiri ile açılamadı: {path}"
        )

    def validate_json(self) -> bool:
        """
        Yüklenen verinin geçerli bir JSON yapısı olduğunu doğrular.
        
        Returns:
            True: Geçerli, False: Geçersiz veya veri yüklenmemiş
        """
        return self._raw_data is not None

    def get_data(self) -> Optional[Union[dict, list]]:
        """Yüklenen JSON verisini döndürür."""
        return self._raw_data

    def get_file_info(self) -> dict:
        """Yüklenen dosya hakkında özet bilgi döndürür."""
        if not self._file_path:
            return {"loaded": False}

        return {
            "loaded": True,
            "path": self._file_path,
            "filename": os.path.basename(self._file_path),
            "size_bytes": os.path.getsize(self._file_path),
            "root_type": type(self._raw_data).__name__,
            "root_length": len(self._raw_data) if self._raw_data else 0,
        }

    def reset(self) -> None:
        """Okuyucuyu sıfırlar."""
        self._file_path = None
        self._raw_data = None
        self._raw_text = None
