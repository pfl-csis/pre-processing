from abc import ABCMeta, abstractmethod

from requests import Response
from services.alert.incident import Incident


class API_interface(metaclass=ABCMeta):

    @abstractmethod
    def fetchAlerts(self, alertIds: list[str]) -> tuple[Incident, bool]:
        """Fetches target Alert by alertID from the Alerter API.

        Args:
            alertId (str): Target alertID as a string.

        Returns:
            tuple[dict, bool]: Alert and boolean in case event was detected. To access entities: Alert.Entities
        """
        pass

    @abstractmethod
    def generateRequest(self, alertId: str) -> tuple[dict, dict[str, str], dict[str, str], str]:
        """_summary_

        Args:
            alertId (str): Target alertID as a string.

        Returns:
            tuple[dict, dict[str, str], dict[str, str], str]: (Customer data dictionary, API request headers, Alert Fetching Query, API Endpoint URL)
        """
        pass

    @abstractmethod
    def postRequest(
        self, customer: dict, headers: dict, data: str, url: str
    ) -> tuple[dict, Response]:
        pass

    @abstractmethod
    def processResponse(
        self, customer: dict, response: Response
    ) -> None | Exception | tuple[dict, bool]:
        pass
