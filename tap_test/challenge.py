from typing import List, Dict, Any
import requests
import logging

DEFAULT_TAP_API_URL = "https://api.tap.pt/v1/fuel-logs"

logger = logging.getLogger(__name__)


class FuelApiClient:
    """
    Client responsible for communication with the TAP Fuel API.
    """

    def __init__(self, base_url: str = DEFAULT_TAP_API_URL) -> None:
        self.base_url = base_url

    def fetch_data(self, flight_id: str) -> Dict[str, Any]:
        """
        Fetches fuel data for a specific flight.

        :param flight_id: Unique flight identifier.
        :return: Dictionary with API response data.
        :raises requests.RequestException: If HTTP request fails.
        """
        url = f"{self.base_url}/{flight_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()


class FuelEfficiencyProcessor:
    """
    Processes flight fuel data and calculates efficiency metrics.
    """

    def __init__(self, api_client: FuelApiClient) -> None:
        self.api_client = api_client

    def process_flights(self, flight_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Processes multiple flights and calculates fuel metrics.

        :param flight_ids: List of flight IDs.
        :return: List of processed flight data including calculated metrics.
        """
        results: List[Dict[str, Any]] = []

        for flight_id in flight_ids:
            try:
                data = self.api_client.fetch_data(flight_id)
                processed = self._calculate_metrics(data)
                results.append(processed)

            except requests.RequestException as exc:
                logger.error(
                    "HTTP error while fetching flight %s: %s",
                    flight_id,
                    exc
                )
            except KeyError as exc:
                logger.error(
                    "Missing expected field in flight %s: %s",
                    flight_id,
                    exc
                )

        return results

    def _calculate_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates fuel spent and consumption rate.

        :param data: Raw flight data from API.
        :return: New dictionary with calculated metrics included.
        """
        start_fuel = data["start_fuel"]
        end_fuel = data["end_fuel"]
        distance = data.get("distance", 0)

        fuel_spent = max(0, start_fuel - end_fuel)
        consumption_rate = (
            fuel_spent / distance if distance > 0 else 0
        )

        return {
            **data,
            "fuel_spent": fuel_spent,
            "consumption_rate": round(consumption_rate, 2),
        }