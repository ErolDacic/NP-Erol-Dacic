"""Demonstracioni monolit (NAMJERNO nije produkciona implementacija).

Prikazuje početni pristup 'sve u jednoj funkciji'. Ne koristi ga aplikacija.
Njegova ograničenja objašnjena su u README-u.
"""
import json


def obradi_rezervacije(ulaz, izlaz):
    with open(ulaz, encoding="utf-8") as f:
        rezervacije = json.load(f)
    ukupno = 0
    for r in rezervacije:
        if r["status"] == "potvrdjena":
            cijena = float(r["price_per_night"]) * int(r["nights"])
            ukupno += cijena * (1 - float(r["discount_percent"]) / 100)
    with open(izlaz, "w", encoding="utf-8") as f:
        json.dump({"ukupno": ukupno}, f)
    return ukupno
