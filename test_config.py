"""Configuration tests."""

from mrg.config import Settings


def test_defaults():
    s = Settings(_env_file=None, port=8000, environment="development")
    assert s.port == 8000
    assert s.environment == "development"
    assert s.has_database is False


def test_cors_parse():
    s = Settings(cors_origins="https://a.com, https://b.com", _env_file=None)
    assert s.cors_origins == ["https://a.com", "https://b.com"]
