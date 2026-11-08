from decimal import Decimal

import pytest

from rezervacije.errors import ReservationError
from rezervacije.service import ReservationService


class InMemorySource:
    """Zamjenski izvor podataka: testira se bez stvarne datoteke (DIP)."""

    def __init__(self, rows):
        self.rows = rows

    def read(self):
        return self.rows


def test_izvjestaj_preskace_otkazane(sample_rows):
    result = ReservationService(InMemorySource(sample_rows)).generate_report()
    assert (result.total_input, result.confirmed, result.canceled) == (2, 1, 1)
    assert result.net_revenue == Decimal("180.00")
    assert result.gross_revenue == Decimal("200.00")
    assert result.discounts == Decimal("20.00")


def test_duplirani_id_se_odbijaju(sample_rows):
    duplicated = [{**sample_rows[0]}, {**sample_rows[0]}]
    with pytest.raises(ReservationError, match="jedinstven"):
        ReservationService(InMemorySource(duplicated)).generate_report()


def test_prazan_ulaz_daje_nulte_sume():
    result = ReservationService(InMemorySource([])).generate_report()
    assert result.net_revenue == Decimal("0.00")
    assert result.total_input == 0


def test_popust_100_procenata(sample_rows):
    record = {**sample_rows[0], "discount_percent": 100}
    result = ReservationService(InMemorySource([record])).generate_report()
    assert result.net_revenue == Decimal("0.00")
