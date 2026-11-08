import csv
import json
from decimal import Decimal

import pytest

from rezervacije.errors import ReservationError
from rezervacije.reporting import JsonReportWriter
from rezervacije.service import ReservationService
from rezervacije.sources import CsvReservationSource, JsonReservationSource


def test_csv_i_json_daju_isti_izvjestaj(tmp_path, sample_rows):
    json_path = tmp_path / "rezervacije.json"
    csv_path = tmp_path / "rezervacije.csv"
    json_path.write_text(json.dumps(sample_rows), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(sample_rows[0]))
        writer.writeheader()
        writer.writerows(sample_rows)
    json_report = ReservationService(JsonReservationSource(json_path)).generate_report()
    csv_report = ReservationService(CsvReservationSource(csv_path)).generate_report()
    assert json_report.to_dict() == csv_report.to_dict()


def test_writer_kreira_json(tmp_path, sample_rows):
    class FakeSource:
        def read(self):
            return sample_rows

    report = ReservationService(FakeSource()).generate_report()
    dest = tmp_path / "output" / "report.json"
    JsonReportWriter().write(report, dest)
    data = json.loads(dest.read_text(encoding="utf-8"))
    assert data["net_revenue"] == "180.00"
    assert data["canceled"] == 1


def test_pogresna_json_struktura(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text('{"not": "a list"}', encoding="utf-8")
    with pytest.raises(ReservationError, match="lista objekata"):
        JsonReservationSource(path).read()


def test_nepostojece_datoteke(tmp_path):
    with pytest.raises(ReservationError):
        CsvReservationSource(tmp_path / "missing.csv").read()


def test_cent_zaokruzivanje(sample_rows):
    class FakeSource:
        def read(self):
            return [{**sample_rows[0], "nights": 1, "price_per_night": "0.05",
                     "discount_percent": 10}]

    report = ReservationService(FakeSource()).generate_report()
    assert report.discounts == Decimal("0.01")
    assert report.net_revenue == Decimal("0.04")
