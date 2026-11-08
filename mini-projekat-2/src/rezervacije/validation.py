"""Validacija i mapiranje neprovjerenog ulaza u domenske modele."""
from decimal import Decimal, InvalidOperation
from typing import cast

from .errors import ReservationError
from .models import Reservation, Status

FIELDS = ("reservation_id", "guest", "nights", "price_per_night", "discount_percent", "status")


def _decimal(value: object, name: str) -> Decimal:
    if isinstance(value, bool):
        raise ReservationError(f"{name}: logička vrijednost nije broj.")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ReservationError(f"{name}: očekivan broj, dobijeno {value!r}.") from exc
    if not result.is_finite():
        raise ReservationError(f"{name}: broj mora biti konačan.")
    return result


def parse_reservation(row: dict[str, object]) -> Reservation:
    missing = [field for field in FIELDS if field not in row or row[field] is None]
    if missing:
        raise ReservationError(f"Nedostaju polja: {', '.join(missing)}")
    rid, guest = str(row["reservation_id"]).strip(), str(row["guest"]).strip()
    if not rid or not guest:
        raise ReservationError("ID rezervacije i ime gosta ne smiju biti prazni.")
    nights = _decimal(row["nights"], "nights")
    if nights != nights.to_integral_value() or nights <= 0:
        raise ReservationError("Broj noćenja mora biti pozitivan cijeli broj.")
    price = _decimal(row["price_per_night"], "price_per_night")
    discount = _decimal(row["discount_percent"], "discount_percent")
    if price < 0:
        raise ReservationError("Cijena noćenja ne smije biti negativna.")
    if not Decimal("0") <= discount <= Decimal("100"):
        raise ReservationError("Popust mora biti između 0 i 100%.")
    status = str(row["status"]).strip().lower()
    if status not in ("potvrdjena", "otkazana"):
        raise ReservationError("Status mora biti 'potvrdjena' ili 'otkazana'.")
    return Reservation(rid, guest, int(nights), price, discount, cast(Status, status))
