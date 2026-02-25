import pytest
import requests

from unittest.mock import MagicMock
from challenge import FuelEfficiencyProcessor


def test_calculates_efficiency_correctly():
    mock_client = MagicMock()
    mock_client.fetch_data.return_value = {
        "id": "TP302",
        "start_fuel": 5000,
        "end_fuel": 1200,
        "distance": 800,
    }

    processor = FuelEfficiencyProcessor(mock_client)
    results = processor.process_flights(["TP302"])

    assert len(results) == 1
    assert results[0]["fuel_spent"] == 3800
    assert results[0]["consumption_rate"] == 4.75


def test_handles_zero_distance():
    mock_client = MagicMock()
    mock_client.fetch_data.return_value = {
        "id": "TP999",
        "start_fuel": 3000,
        "end_fuel": 1000,
        "distance": 0,
    }

    processor = FuelEfficiencyProcessor(mock_client)
    results = processor.process_flights(["TP999"])

    assert results[0]["consumption_rate"] == 0


def test_handles_http_error_gracefully():
    mock_client = MagicMock()
    mock_client.fetch_data.side_effect = requests.RequestException("API failure")

    processor = FuelEfficiencyProcessor(mock_client)
    results = processor.process_flights(["TP404"])

    assert results == []