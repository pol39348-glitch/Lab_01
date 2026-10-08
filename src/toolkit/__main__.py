import sys
import argparse
from .calculator import calculate
from .converter import convert
from .errors import ToolkitError, InvalidNumericValueError


def main():
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="Консольный набор утилит: калькулятор и конвертер"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Калькулятор
    calc_parser = subparsers.add_parser("calc", help="Вычислить математическое выражение")
    calc_parser.add_argument("expression", type=str, help="Выражение в кавычках, например '2 + 2 * 2'")

    # Конвертер
    conv_parser = subparsers.add_parser("convert", help="Конвертировать величины")
    conv_parser.add_argument("value", type=str, help="Числовое значение")
    conv_parser.add_argument("--from", dest="from_unit", required=True,
                             help="Исходная единица (mm, cm, m, km, g, kg, c, f, k)")
    conv_parser.add_argument("--to", dest="to_unit", required=True, help="Целевая единица")

    try:
        args = parser.parse_args()

        if args.command == "calc":
            result = calculate(args.expression)
            if result.is_integer():
                print(int(result))
            else:
                print(result)

        elif args.command == "convert":
            try:
                val = float(args.value)
            except ValueError:
                raise InvalidNumericValueError("Неверное числовое значение")

            result = convert(val, args.from_unit, args.to_unit)
            print(result)

    except ToolkitError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
