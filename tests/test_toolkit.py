import subprocess
import pytest
from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import (
    EmptyExpressionError, InvalidCharacterError, MissingOperandError,
    DivisionByZeroError, UnknownUnitError, IncompatibleUnitsError, AbsoluteZeroError
)

# --- Позитивные тесты ядра (8) ---
def test_calc_add(): assert calculate("2 + 3") == 5.0
def test_calc_precedence(): assert calculate("2 + 3 * 4") == 14.0
def test_calc_unary(): assert calculate("-5 + 3") == -2.0
def test_calc_spaces(): assert calculate("  10  /   2  ") == 5.0
def test_calc_float(): assert calculate("2.5 * 2") == 5.0
def test_calc_complex(): assert calculate("10 + -2 * 3") == 4.0
def test_convert_length(): assert convert(1000, "mm", "m") == 1.0
def test_convert_temp(): assert convert(0, "c", "f") == 32.0

# --- Негативные тесты ядра (7) ---
def test_calc_empty():
    with pytest.raises(EmptyExpressionError):
        calculate("")

def test_calc_invalid_char():
    with pytest.raises(InvalidCharacterError):
        calculate("2 + a")

def test_calc_missing_operand():
    with pytest.raises(MissingOperandError):
        calculate("2 + * 3")

def test_calc_div_by_zero():
    with pytest.raises(DivisionByZeroError):
        calculate("5 / 0")

def test_convert_incompatible():
    with pytest.raises(IncompatibleUnitsError):
        convert(1, "m", "kg")

def test_convert_absolute_zero():
    with pytest.raises(AbsoluteZeroError):
        convert(-300, "c", "k")

def test_convert_unknown_unit():
    with pytest.raises(UnknownUnitError):
        convert(1, "m", "miles")

# --- CLI тесты (2) ---
def test_cli_calc_success():
    res = subprocess.run(
        ["python", "-m", "toolkit", "calc", "2+2"],
        capture_output=True, text=True, cwd="src"
    )
    assert res.returncode == 0
    assert res.stdout.strip() == "4"

def test_cli_convert_error():
    res = subprocess.run(
        ["python", "-m", "toolkit", "convert", "1", "--from", "m", "--to", "kg"],
        capture_output=True, text=True, cwd="src"
    )
    assert res.returncode == 2
    assert "Error" in res.stderr or "несовместимые" in res.stderr.lower()