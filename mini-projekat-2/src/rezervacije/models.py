"""Tipizirani domenski modeli, bez zavisnosti od formata podataka."""
from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import Literal

Status = Literal["potvrdjena", "otkazana"]


@dataclass(frozen=True, slots=True)
class Reservation:
    reservation_id: str
    guest: str
    nights: int
    price_per_night: Decimal
    discount_percent: Decimal
    status: Status


@dataclass(frozen=True, slots=True)
class BookingItem:
    reservation_id: str
    guest: str
    nights: int
    subtotal: Decimal
    discount: Decimal
    total: Decimal

    def to_dict(self) -> dict[str, object]:
        return {key: (str(val) if isinstance(val, Decimal) else val)
                for key, val in asdict(self).items()}


@dataclass(frozen=True, slots=True)
class BookingReport:
    total_input: int
    confirmed: int
    canceled: int
    gross_revenue: Decimal
    discounts: Decimal
    net_revenue: Decimal
    bookings: tuple[BookingItem, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "total_input": self.total_input,
            "confirmed": self.confirmed,
            "canceled": self.canceled,
            "gross_revenue": str(self.gross_revenue),
            "discounts": str(self.discounts),
            "net_revenue": str(self.net_revenue),
            "bookings": [item.to_dict() for item in self.bookings],
        }
