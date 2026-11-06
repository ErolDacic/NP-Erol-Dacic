# Zadatak 1 — Priprema radnog okruženja (3 boda)

**Predmet:** Napredno programiranje, UDG/FIST  
**Student:** [IME I PREZIME — dopuniti]

Ovo je **prva, samostalna predaja**. Zadatak 2 ima poseban folder i poseban ZIP, a prema slajdu profesora koristi se **isti GitHub repozitorijum** za sve mini-projekte. Preporuka: ovaj sadržaj staviti u direktorijum `zadatak-1/` zajedničkog repozitorijuma `np-ime-prezime`.

## Zahtjevi i gdje se nalaze

1. Python 3.12+ i VS Code: instalirati lokalno; projekat je podešen za Python 3.12+.
2. GitHub repozitorijum `np-ime-prezime` sa README-om: napraviti na sopstvenom GitHub nalogu.
3. Ruff + pytest: `requirements-dev.txt`, `pyproject.toml`, GitHub Actions provjera.
4. AI implementacija `prosjecna_cijena`: `prosjecna_cijena.py`; testovi u `tests/`.
5. AI upit i uočeni nedostaci: dokumentovani ispod.

## Pokretanje (Windows PowerShell)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check .
```

Ako komanda `py -3.12` nije dostupna, koristiti instalirani Python 3.12+ i `python -m venv .venv`. Ruff mora biti lokalno pokrenut prije predaje.

## Funkcija

`prosjecna_cijena([10, 20, 30])` vraća `Decimal('20.00')`. Za novac se koristi `Decimal` i zaokruživanje na dvije decimale. Prazna lista, negativna, nebrojčana ili beskonačna cijena izaziva `ReservationError`.

## AI asistencija — upiti i provjere

**Sažetak upita 1:** „Implementiraj funkciju `prosjecna_cijena` u Pythonu 3.12+, sa validacijom, ispravnim računanjem novca i pytest testovima.“

**Sažetak upita 2:** „Dodaj `ruff`, `pytest`, GitHub Actions i README sa jasnim komandama za pokretanje.“

**Uočeni rizici i ispravke:** (a) `sum(cijene)/len(cijene)` pada na praznoj listi — dodata provjera; (b) `float` može pogrešno predstaviti novac — korišćen `Decimal`; (c) negativne i `NaN` cijene nijesu validne — uvedena validacija; (d) obični `round` ne odgovara uvijek poslovnom zaokruživanju — korišćen `ROUND_HALF_UP`; (e) dodati testovi za normalne i rubne slučajeve.

Ovi upiti su sažeti opisi zahtjeva, ne doslovan kompletan dnevnik razgovora. Pročitaj rješenje i prilagodi opis stvarnim koracima koje si sam preduzeo.

## Predaja prve faze

Na GitHub-u napravi **jedan** repo `np-ime-prezime`, pa u njemu direktorijum `zadatak-1/` sa ovim fajlovima (ili ih postavi u korijen repozitorijuma). Predaj link na taj repo prema uputstvu profesora. Kasnije dodaj `zadatak-2/` u isti repo; prvu fazu nemoj brisati.

**Napomena:** Samo fajlovi ne potvrđuju da su Python/VS Code zaista instalirani na tvom računaru niti da je GitHub nalog kreiran.
