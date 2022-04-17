from src.infrastructure.repositories.yahoo_repository import YahooRepository


def test_get_history():
    results = YahooRepository().get_history('TSLA')

    assert results
