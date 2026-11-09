"""Izvori podataka: lako zamjenjivi zahvaljujući Protocol interfejsu."""
import csv
import json
from pathlib import Path
from typing import Protocol

from .errors import ReservationError


class ReservationSource(Protocol):
    def read(self) -> list[dict[str, object]]:
        """Učitaj redove bez poslovne obrade."""
        ...


class JsonReservationSource:
    def __init__(self, path: Path) -> None:
        self.path = path

    def read(self) -> list[dict[str, object]]:
        try:
            content = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ReservationError(f"Neuspješno čitanje JSON datoteke: {exc}") from exc
        if not isinstance(content, list) or not all(isinstance(row, dict) for row in content):
            raise ReservationError("JSON mora biti lista objekata (rezervacija).")
        return content


class CsvReservationSource:
    def __init__(self, path: Path) -> None:
        self.path = path

    def read(self) -> list[dict[str, object]]:
        try:
            with self.path.open(encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
        except (OSError, csv.Error) as exc:
            raise ReservationError(f"Neuspješno čitanje CSV datoteke: {exc}") from exc
        if not rows:
            raise ReservationError("CSV mora sadržati makar jednu rezervaciju.")
        return rows
