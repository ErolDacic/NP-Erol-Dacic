from decimal import Decimal

import pytest

from prosjecna_cijena import ReservationError, prosjecna_cijena


def test_prosjecna_cijena_osnovni_slucaj():
    assert prosjecna_cijena([10, 20, 30]) == Decimal("20.00")


def test_prosjecna_cijena_preciznost_i_zaokruzivanje():
    assert prosjecna_cijena(["0.10", "0.20"]) == Decimal("0.15")
    assert prosjecna_cijena(["1.00", "1.01"]) == Decimal("1.01")


@pytest.mark.parametrize("prices", [[], [-1], ["x"], ["NaN"], [float("inf")], [True]])
def test_prosjecna_cijena_neispravni_ulazi(prices):
    with pytest.raises(ReservationError):
        prosjecna_cijena(prices)
