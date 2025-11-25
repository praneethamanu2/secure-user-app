import pytest
from pydantic import ValidationError

from app import calculations
from app.schemas import CalculationCreate


def test_add_operation():
    assert calculations.perform_calculation("Add", 1, 2) == 3


def test_sub_operation():
    assert calculations.perform_calculation("Sub", 5, 3) == 2


def test_multiply_operation():
    assert calculations.perform_calculation("Multiply", 3, 4) == 12


def test_divide_operation():
    assert calculations.perform_calculation("Divide", 10, 2) == 5


def test_unknown_operation_raises():
    with pytest.raises(ValueError):
        calculations.get_operation("Unknown")


def test_calc_create_validation_divide_by_zero():
    # division by zero should raise when performing the calculation
    with pytest.raises(ZeroDivisionError):
        calculations.perform_calculation("Divide", 1, 0)


def test_calc_create_invalid_type():
    with pytest.raises(ValidationError):
        CalculationCreate(a=1, b=2, type="Pow")
