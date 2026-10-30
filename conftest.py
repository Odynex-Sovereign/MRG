import pytest

@pytest.fixture
def mock_db_credentials():
    return {
        "db_user": "mrg_admin",
        "db_name": "mrg_simulation_grid",
        "engine_override": "ODYNEX_AXIS_LOGISTICS"
    }
