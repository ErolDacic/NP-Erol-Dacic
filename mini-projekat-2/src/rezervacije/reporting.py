"""Izvještavanje odvojeno od izračunavanja i izvora podataka."""
import json
from pathlib import Path
from typing import Protocol

from .models import BookingReport


class ReportWriter(Protocol):
    def write(self, report: BookingReport, destination: Path) -> None:
        """Sačuvaj izvještaj u zadatom formatu."""
        ...


class JsonReportWriter:
    def write(self, report: BookingReport, destination: Path) -> None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(report.to_dict(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
