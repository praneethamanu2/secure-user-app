from app import calculations


def test_power_operation():
    # 2^3 = 8
    assert calculations.perform_calculation("Power", 2, 3) == 8
    # fractional exponents
    assert calculations.perform_calculation("Power", 9, 0.5) == 3
    # negative exponent
    assert calculations.perform_calculation("Power", 2, -1) == 0.5
