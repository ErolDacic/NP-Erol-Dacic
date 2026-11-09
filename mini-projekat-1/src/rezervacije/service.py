"""Orkestracija obrade bez znanja o CSV-u, JSON-u ili fajl sistemu."""
from decimal import Decimal

from .errors import ReservationError
from .models import BookingReport
from .pricing import BookingCalculator
from .sources import ReservationSource
from .validation import parse_reservation


class ReservationService:
    def __init__(self, source: ReservationSource, calculator: BookingCalculator | None = None) -> None:
        self.source = source
        self.calculator = calculator or BookingCalculator()

    def generate_report(self) -> BookingReport:
        reservations = [parse_reservation(raw) for raw in self.source.read()]
        ids = [r.reservation_id for r in reservations]
        if len(ids) != len(set(ids)):
            raise ReservationError("ID rezervacije mora biti jedinstven.")
        active = [r for r in reservations if r.status == "potvrdjena"]
        items = tuple(self.calculator.calculate(r) for r in active)
        return BookingReport(
            total_input=len(reservations),
            confirmed=len(active),
            canceled=len(reservations) - len(active),
            gross_revenue=sum((r.subtotal for r in items), Decimal("0.00")),
            discounts=sum((r.discount for r in items), Decimal("0.00")),
            net_revenue=sum((r.total for r in items), Decimal("0.00")),
            bookings=items,
        )
