from app import calculations


def test_monkeypatch_perform_calculation(monkeypatch):
    # Replace the calculation function temporarily and verify it's used
    monkeypatch.setattr(calculations, "perform_calculation", lambda op, a, b: 999)
    assert calculations.perform_calculation("Add", 1, 2) == 999
    assert calculations.perform_calculation("Divide", 10, 2) == 999
