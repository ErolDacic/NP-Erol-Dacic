"""Komandna linija za demonstraciju, uz ponovnu upotrebu poslovne logike."""
import argparse
from pathlib import Path

from .analytics import prosjecna_cijena
from .errors import ReservationError
from .reporting import JsonReportWriter
from .service import ReservationService
from .sources import CsvReservationSource, JsonReservationSource


def main() -> int:
    parser = argparse.ArgumentParser(description="Napredno programiranje: rezervacije")
    commands = parser.add_subparsers(dest="command", required=True)
    average = commands.add_parser("average", help="Izračunaj prosječnu cijenu")
    average.add_argument("prices", nargs="+", help="Cijene, npr. 12 15.5 20")
    report = commands.add_parser("report", help="Izvještaj o rezervacijama")
    report.add_argument("input", type=Path, help="Ulazni .csv ili .json")
    report.add_argument("--output", type=Path, default=Path("izvjestaj.json"))
    args = parser.parse_args()
    try:
        if args.command == "average":
            print(f"Prosječna cijena: {prosjecna_cijena(args.prices)} EUR")
        else:
            if args.input.suffix.lower() == ".csv":
                source = CsvReservationSource(args.input)
            elif args.input.suffix.lower() == ".json":
                source = JsonReservationSource(args.input)
            else:
                raise ReservationError("Ulaz mora biti .csv ili .json")
            result = ReservationService(source).generate_report()
            JsonReportWriter().write(result, args.output)
            print(f"Izvještaj: {args.output} | Neto prihod: {result.net_revenue} EUR")
    except (ReservationError, OSError) as exc:
        parser.exit(2, f"Greška: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
