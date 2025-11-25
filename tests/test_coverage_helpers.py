from datetime import datetime
import pytest

from app import main, crud, schemas


def test_on_startup_and_get_db_generator():
    # Use the test DB engine/session so we don't try to connect to the Docker Postgres
    from tests import conftest as conf
    main.engine = conf.engine
    main.SessionLocal = conf.TestingSessionLocal

    # call startup handler (will create tables on the test engine)
    main.on_startup()
    gen = main.get_db()
    db = next(gen)
    # closing the generator should run the cleanup (db.close())
    gen.close()


def test_read_root_function():
    # cover the simple root handler
    assert main.read_root() == {"message": "Secure User App running"}


def test_calculationcreate_divide_by_zero_validator():
    from pydantic import ValidationError
    from app.schemas import CalculationCreate
    # Pydantic v2 deprecates v1-style validators; call the validator directly
    with pytest.raises(ValueError):
        # call the underlying function object (for classmethod) to exercise the raise branch
        fn = CalculationCreate.__dict__["validate_divisor"].__func__
        fn(None, 0, {"type": "Divide"})


def test_get_calculation_helper():
    # Ensure get_calculation returns the inserted calculation
    from tests import conftest as conf
    db = conf.TestingSessionLocal()
    try:
        calc_in = schemas.CalculationCreate(a=2, b=3, type="Add")
        created = crud.create_calculation(db, calc_in)
        fetched = crud.get_calculation(db, created.id)
        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.result == 5
    finally:
        db.close()


def test_schema_from_orm_objects():
    class Dummy:
        def __init__(self):
            self.id = 1
            self.a = 4
            self.b = 5
            self.type = "Add"
            self.result = 9
            self.created_at = datetime.utcnow()

    d = Dummy()
    # use Pydantic v2 style validation from attributes
    read = schemas.CalculationRead.model_validate(d, from_attributes=True)
    assert read.id == d.id
    assert read.result == d.result
