"""
Şema Modelleri (Schema Models)
------------------------------
Veritabanı şemasını temsil eden veri sınıfları.
TableSchema, ColumnDefinition ve ForeignKey nesneleri,
JSON analizinden SQL oluşturmaya kadar tüm katmanlar arasında
veri taşıyıcı (data carrier) olarak kullanılır.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ForeignKey:
    """İki tablo arasındaki Yabancı Anahtar (Foreign Key) ilişkisini tanımlar."""
    column: str           # Bu tablodaki FK sütun adı
    ref_table: str        # Referans verilen (parent) tablo adı
    ref_column: str       # Referans verilen sütun (genellikle 'id')

    def __repr__(self) -> str:
        return f"FK({self.column} -> {self.ref_table}.{self.ref_column})"


@dataclass
class ColumnDefinition:
    """Bir SQL sütununun tanımını tutar."""
    name: str                           # Sütun adı
    sql_type: str = "TEXT"              # SQL veri tipi (TEXT, INTEGER, REAL, BOOLEAN)
    nullable: bool = True               # NULL olabilir mi?
    is_primary_key: bool = False        # Primary Key mi?
    is_foreign_key: bool = False        # Foreign Key mi?
    references: Optional[str] = None    # FK ise referans tablo.sütun

    def __repr__(self) -> str:
        flags = []
        if self.is_primary_key:
            flags.append("PK")
        if self.is_foreign_key:
            flags.append(f"FK->{self.references}")
        flag_str = f" [{', '.join(flags)}]" if flags else ""
        return f"Column({self.name} {self.sql_type}{flag_str})"


@dataclass
class TableSchema:
    """
    Bir SQL tablosunun tam şemasını temsil eder.
    Sütun tanımları, Primary Key, Foreign Key ilişkileri ve
    tabloya yazılacak kayıtları (records) içerir.
    """
    name: str                                          # Tablo adı
    columns: List[ColumnDefinition] = field(default_factory=list)
    primary_key: str = "id"                            # PK sütun adı
    foreign_keys: List[ForeignKey] = field(default_factory=list)
    records: List[dict] = field(default_factory=list)  # INSERT edilecek veriler

    def add_column(self, col: ColumnDefinition) -> None:
        """Tabloya yeni bir sütun ekler (aynı isimde yoksa)."""
        existing_names = {c.name for c in self.columns}
        if col.name not in existing_names:
            self.columns.append(col)

    def add_foreign_key(self, fk: ForeignKey) -> None:
        """Tabloya yeni bir Foreign Key ilişkisi ekler."""
        self.foreign_keys.append(fk)
        # FK sütununu da columns'a ekle (yoksa)
        self.add_column(ColumnDefinition(
            name=fk.column,
            sql_type="INTEGER",
            nullable=False,
            is_foreign_key=True,
            references=f"{fk.ref_table}.{fk.ref_column}"
        ))

    def add_record(self, record: dict) -> None:
        """Tabloya bir veri kaydı ekler."""
        self.records.append(record)

    def get_column_names(self) -> List[str]:
        """Tüm sütun adlarını döndürür (PK hariç)."""
        return [c.name for c in self.columns if not c.is_primary_key]

    def has_column(self, name: str) -> bool:
        """Belirtilen isimde sütun var mı kontrol eder."""
        return any(c.name == name for c in self.columns)

    def update_column_type(self, col_name: str, new_type: str) -> None:
        """Mevcut bir sütunun tipini günceller (daha geniş tipe yükseltme)."""
        for col in self.columns:
            if col.name == col_name:
                col.sql_type = new_type
                break

    def __repr__(self) -> str:
        col_str = ", ".join(str(c) for c in self.columns)
        fk_str = ", ".join(str(fk) for fk in self.foreign_keys)
        return (f"Table({self.name}: [{col_str}]"
                f"{' | ' + fk_str if fk_str else ''}"
                f" | {len(self.records)} records)")
