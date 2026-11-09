"""Poslovna logika obračuna cijena: samo jedan razlog za izmjenu."""
from decimal import ROUND_HALF_UP, Decimal

from .models import BookingItem, Reservation

CENT = Decimal("0.01")


class BookingCalculator:
    def calculate(self, reservation: Reservation) -> BookingItem:
        subtotal = (reservation.price_per_night * reservation.nights).quantize(
            CENT, rounding=ROUND_HALF_UP
        )
        discount = (subtotal * reservation.discount_percent / Decimal("100")).quantize(
            CENT, rounding=ROUND_HALF_UP
        )
        return BookingItem(
            reservation.reservation_id,
            reservation.guest,
            reservation.nights,
            subtotal,
            discount,
            subtotal - discount,
        )
