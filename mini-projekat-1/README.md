# Mini projekat 1 — Refaktoring obrade rezervacija

**Univerzitet Donja Gorica (UDG), FIST**  
**Predmet:** Napredno programiranje  
**Student:** Erol Dacic  
**GitHub repozitorijum:** `np-Erol-Dacic`

## 1. Brzi početak (Windows PowerShell)

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pytest -q
python -m ruff check .
python -m rezervacije average 100 200 300
python -m rezervacije report data/rezervacije.json --output izvjestaj.json
```

Projekat zahtijeva Python 3.12 ili noviji. Komanda `py -3` koristi podrazumijevanu instaliranu verziju Pythona. Ako PowerShell blokira aktivaciju, izvršiti direktno `.\.venv\Scripts\python.exe -m pip install -e ".[dev]"` pa istim prefiksom ostale `python -m ...` komande. Za Linux/macOS aktivirati sa `source .venv/bin/activate`.

**Alternativa:** Google Colab može pokrenuti Python i testove, ali za GitHub i VS Code preporučen je lokalni rad. Za Colab je potrebno prvo prenijeti repo/datoteke.

## 2. Zahtjevi

### Ponovo korišćena osnova iz prvog zadatka

1. **Python 3.12+ i VS Code:** gore navedene komande i `pyproject.toml` definišu okruženje. Instalacija na studentov računar mora se uraditi lokalno.
2. **GitHub repozitorijum `np-Erol-Dacic`:** projekat je spreman za upload; nalog i repozitorijum mora kreirati student (nije moguće obaviti bez pristupa nalogu).
3. **Ruff + pytest:** konfigurisani u `pyproject.toml` i pokreću se navedenim komandama; automatska CI provjera je u `.github/workflows/python-tests.yml`.
4. **AI funkcija `prosjecna_cijena`:** implementacija u `src/rezervacije/analytics.py`, test u `tests/test_analytics.py`. Koristi `Decimal`, validira ulaze, obrađuje greške i ispravno zaokružuje.
5. **AI upiti i uočeni nedostaci:** dati u nastavku README-a.

### Zadatak 2: Mini projekat 1

1. **Vlastiti monolitni skript:** `legacy/monolit.py` je početni primjer (nije dio aktivnog koda).
2. **Refaktoring uz S i D:** implementiran u `src/rezervacije/`.
3. **Protocol za izvor podataka i izvještavanje:** `ReservationSource` u `sources.py` i `ReportWriter` u `reporting.py`.
4. **Najmanje tri pytest testa zamjene izvora:** projekat sadrži više od tri testa, uključujući upoređivanje CSV i JSON izvora i lažni izvor bez datoteke.
5. **AI upiti i ispravke:** opisani ispod.

## 3. Arhitektura projekta

```text
np-ime-prezime/
├── src/rezervacije/
│   ├── __init__.py
│   ├── __main__.py
│   ├── analytics.py     # prosjecna_cijena
│   ├── cli.py           # komandna linija
│   ├── errors.py        # domenski izuzeci
│   ├── models.py        # dataclass modeli
│   ├── pricing.py       # izračunavanje cijena
│   ├── reporting.py     # Protocol za izvještaje + JSON writer
│   ├── service.py       # poslovni tok
│   ├── sources.py       # Protocol + CSV/JSON izvori
│   └── validation.py    # validacija ulaznih redova
├── data/                # dva jednaka primjera u CSV i JSON formatu
├── tests/               # automatizovani testovi
├── legacy/monolit.py    # početni primjer prije refaktoringa
├── .github/workflows/  # automatska CI provjera na GitHub-u
├── pyproject.toml       # paket + test i ruff konfiguracija
└── README.md
```

### SOLID principi — S i D

**S — Single Responsibility Principle:** izvori samo učitavaju podatke, validator samo provjerava/mapira podatke, kalkulator samo obračunava cijene, servis upravlja tokom, a pisac samo čuva izvještaj. Svaka klasa ima jedan razlog za promjenu.

**D — Dependency Inversion Principle:** `ReservationService` zavisi od apstrakcije `ReservationSource` (Protocol), a ne od konkretne CSV/JSON klase. U testovima se lako zamjenjuje sa `InMemorySource`. Pisanje izvještaja ima zaseban `ReportWriter` Protocol; implementacija `JsonReportWriter` je zamjenjiva bez promjene poslovnog modela.

**Pravila obrade:** aktivne su samo rezervacije `potvrdjena`; otkazane se evidentiraju ali ne ulaze u prihod. Vrijednosti su u EUR. Svaka rezervacija mora imati jedinstven ID, pozitivan cijeli broj noćenja, nenegativnu cijenu, popust 0–100 i validan status. Novac se obračunava pomoću `Decimal`, na dvije decimale (`ROUND_HALF_UP`). Podaci su demonstracioni i nijesu preuzeti iz realnog sistema.

## 4. AI upiti korišćeni u pripremi

Radi transparentnosti navedeni su *sažeti sadržaji zadataka postavljenih AI asistentu tokom izrade ovog projekta*. Nijesu predstavljeni kao doslovan zapis svih internih koraka.

**Upit 1 — početni zadatak:** „Kreiraj Python 3.12+ projekat za obradu rezervacija, implementiraj funkciju `prosjecna_cijena`, podesi `ruff` i `pytest`, napiši testove i uputstvo za GitHub.“

**Upit 2 — refaktoring:** „Razdvoji monolitnu obradu rezervacija na učitavanje, validaciju, obračun i izvještavanje. Primijeni SOLID S i D i `typing.Protocol` za izvor podataka i izvještavanje.“

**Upit 3 — testiranje:** „Dodaj pytest testove koji koriste zamjenski izvor podataka, upoređuju CSV i JSON, odbijaju negativne cijene, duplirane ID-jeve, neispravan popust i provjeravaju preciznost novčanih vrijednosti.“

**Upit 4 — revizija:** „Provjeri rubne slučajeve, tipove, greške, logiku otkazanih rezervacija i dokumentuj šta je ispravljeno u odnosu na monolit.“

## 5. Uočeni nedostaci generisanog/početnog pristupa i ispravke

| Problem početnog monolita | Ispravka u završnoj verziji |
|---|---|
| Jedna funkcija radi I/O, validaciju, obračun i izvještavanje | Odvojeni `sources.py`, `validation.py`, `pricing.py`, `service.py`, `reporting.py` |
| Koristi `float` za novac (moguća greška preciznosti) | `Decimal` i eksplicitno zaokruživanje na 2 decimale |
| Bez provjere neispravnog broja noćenja i negativnih vrijednosti | Jasna validacija i `ReservationError` |
| Pristup fiksno vezan za JSON | `ReservationSource` Protocol + CSV i JSON implementacije |
| Nemoguće testiranje poslovne logike bez fajla | `InMemorySource` u testovima |
| Nema provjere dupliranih rezervacija | Provjera jedinstvenosti ID-ja |
| Nema dokumentacije ni testova | README, pytest, ruff i GitHub Actions |
| Pretpostavlja dostupnost ulazne datoteke | Kontrolisana poruka o grešci |

**Rezultati lokalne provjere:** Svih 26 pytest testova uspješno je prošlo (`26 passed`). Ruff provjera je uspješno završena (`All checks passed!`). Automatske provjere su pokrenute u lokalnom Python 3.13 okruženju.

**Lična provjera prije predaje:** pokrenuti `pytest -q` i `ruff check .`; pregledati rezultat i razumjeti rješenje jer profesor može tražiti usmeno objašnjenje.

## 6. Primjeri korišćenja i očekivani rezultat

```bash
python -m rezervacije average 12 24 36
# Prosječna cijena: 24.00 EUR

python -m rezervacije report data/rezervacije.csv --output izvjestaj.json
# Izvještaj: izvjestaj.json | Neto prihod: 500.40 EUR
```

Demo obračun: R001 = 216.00; R002 = 240.00; R003 otkazana; R004 = 44.40, ukupno **500.40 EUR**.

## GitHub repozitorijum i predaja

Mini projekat 1 nalazi se u folderu `mini-projekat-1` unutar zajedničkog GitHub repozitorijuma za predmet Napredno programiranje.

**GitHub repozitorijum:** https://github.com/ErolDacic/NP-Erol-Dacic

### Preuzimanje projekta

Za preuzimanje kompletnog repozitorijuma:

```powershell
git clone https://github.com/ErolDacic/NP-Erol-Dacic.git
cd NP-Erol-Dacic
cd mini-projekat-1
```

Za pokretanje projekta koristiti uputstva za instalaciju i testiranje navedena u prethodnim poglavljima ovog README dokumenta.

### Ažuriranje postojećeg repozitorijuma

Ako je repozitorijum već preuzet i potrebno je poslati nove izmjene, iz glavnog foldera `NP-Erol-Dacic` izvršiti:

```powershell
git status
git add mini-projekat-1
git commit -m "Update mini project 1 documentation"
git push origin main
```

Nije potrebno ponovo izvršavati `git init` ili kreirati novi GitHub repozitorijum.

Oba mini projekta i pripremni zadatak nalaze se u istom repozitorijumu, u skladu sa instrukcijama predmeta.
```
