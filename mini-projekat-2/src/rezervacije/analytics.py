"""Jednostavna funkcija za obavezni zadatak pripreme okruženja."""
from collections.abc import Iterable
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from .errors import ReservationError

CENT = Decimal("0.01")


def prosjecna_cijena(cijene: Iterable[int | float | str | Decimal]) -> Decimal:
    """Vrati aritmetičku sredinu nenegativnih cijena, zaokruženu na cent.

    Decimal(str(x)) sprječava tipičnu nepreciznost binarnih floatova.
    Prazan ulaz, negativne, NaN, beskonačne i nenumeričke vrijednosti
    odbijaju se jasnom greškom. Funkcija ne mijenja ulazni niz.
    """
    brojevi: list[Decimal] = []
    for vrijednost in cijene:
        if isinstance(vrijednost, bool):
            raise ReservationError("Logička vrijednost nije cijena.")
        try:
            broj = Decimal(str(vrijednost))
        except (InvalidOperation, ValueError) as exc:
            raise ReservationError(f"Neispravna cijena: {vrijednost!r}") from exc
        if not broj.is_finite() or broj < 0:
            raise ReservationError("Cijene moraju biti konačne i nenegativne.")
        brojevi.append(broj)
    if not brojevi:
        raise ReservationError("Lista cijena ne smije biti prazna.")
    return (sum(brojevi) / len(brojevi)).quantize(CENT, rounding=ROUND_HALF_UP)
