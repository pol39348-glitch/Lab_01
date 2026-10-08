from .errors import UnknownUnitError, IncompatibleUnitsError, AbsoluteZeroError


def get_group(unit: str) -> str | None:
    u = unit.lower()
    if u in ('mm', 'cm', 'm', 'km'):
        return 'length'
    if u in ('g', 'kg'):
        return 'mass'
    if u in ('c', 'f', 'k'):
        return 'temp'
    return None


def convert_temp(value: float, from_u: str, to_u: str) -> float:
    # Приведение к Кельвинам
    if from_u == 'c':
        k = value + 273.15
    elif from_u == 'f':
        k = (value - 32) * 5 / 9 + 273.15
    elif from_u == 'k':
        k = value
    else:
        raise UnknownUnitError()

    if k < 0:
        raise AbsoluteZeroError("Температура ниже абсолютного нуля")

    # Конвертация из Кельвинов
    if to_u == 'c':
        return k - 273.15
    elif to_u == 'f':
        return (k - 273.15) * 9 / 5 + 32
    elif to_u == 'k':
        return k

    raise UnknownUnitError()


def convert(value: float, from_unit: str, to_unit: str) -> float:
    from_u = from_unit.lower()
    to_u = to_unit.lower()

    group_from = get_group(from_u)
    group_to = get_group(to_u)

    if not group_from or not group_to:
        raise UnknownUnitError("Неизвестная единица измерения")

    if group_from != group_to:
        raise IncompatibleUnitsError("Несовместимые единицы измерения")

    if group_from == 'temp':
        return convert_temp(value, from_u, to_u)

    multipliers = {
        'length': {'mm': 0.001, 'cm': 0.01, 'm': 1.0, 'km': 1000.0},
        'mass': {'g': 0.001, 'kg': 1.0}
    }

    base_value = value * multipliers[group_from][from_u]
    return base_value / multipliers[group_to][to_u]