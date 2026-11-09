"""Domenski izuzeci umjesto generičkog hvatanja svih grešaka."""
class ReservationError(ValueError):
    """Ulazni podaci rezervacije nijesu ispravni."""
