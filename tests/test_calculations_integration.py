from app import crud, schemas
import tests.conftest as conf


def test_create_calculation_in_db():
    # Use the TestingSessionLocal from conftest to get a session bound to TEST_DB
    db = conf.TestingSessionLocal()
    try:
        calc_in = schemas.CalculationCreate(a=6, b=7, type="Multiply")
        calc = crud.create_calculation(db, calc_in)
        assert calc.id is not None
        assert calc.result == 42
        assert calc.type == "Multiply"
    finally:
        db.close()
