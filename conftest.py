import sys
import os
import pytest
from main import Base, engine

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
