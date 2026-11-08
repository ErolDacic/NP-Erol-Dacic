import pytest

from rezervacije.errors import ReservationError
from rezervacije.validation import parse_reservation


@pytest.mark.parametrize("field,value", [
    ("nights", 0), ("nights", 1.5), ("price_per_night", -1),
    ("discount_percent", 101), ("discount_percent", -1),
    ("status", "ceka"), ("guest", " "),
])
def test_neispravna_rezervacija(sample_rows, field, value):
    record = {**sample_rows[0], field: value}
    with pytest.raises(ReservationError):
        parse_reservation(record)


def test_nedostajuce_polje(sample_rows):
    record = dict(sample_rows[0])
    del record["nights"]
    with pytest.raises(ReservationError, match="Nedostaju polja"):
        parse_reservation(record)


def test_ispravna_rezervacija(sample_rows):
    assert parse_reservation(sample_rows[0]).nights == 2
