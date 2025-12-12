# app/calculations.py
from __future__ import annotations
from typing import Protocol

class Operation(Protocol):
    def compute(self, a: float, b: float) -> float: ...


class Add:
    def compute(self, a: float, b: float) -> float:
        return a + b


class Sub:
    def compute(self, a: float, b: float) -> float:
        return a - b


class Multiply:
    def compute(self, a: float, b: float) -> float:
        return a * b


class Divide:
    def compute(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        return a / b


class Power:
    def compute(self, a: float, b: float) -> float:
        # exponentiation (a ** b). allow negative/float exponents.
        return a ** b


def get_operation(op_type: str) -> Operation:
    mapping = {
        "Add": Add,
        "Sub": Sub,
        "Multiply": Multiply,
        "Divide": Divide,
        "Power": Power,
    }
    cls = mapping.get(op_type)
    if cls is None:
        raise ValueError(f"Unknown operation type: {op_type}")
    return cls()


def perform_calculation(op_type: str, a: float, b: float) -> float:
    op = get_operation(op_type)
    return op.compute(a, b)
