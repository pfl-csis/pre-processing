import json
import requests

from services.queryGen.kql import KQLQuery
  # In prod should be using service principal account from AZ KEY VAULT.
from services.sentinel.getAccessToken import (
    get_access_token,
)  # Access token from auth.py
from services.apiInterface import API_interface
from services.incident.alert import Alert

from services.config.settings import MS_CLIENT_ID, MS_SECRET

CLIENT_ID = MS_CLIENT_ID
CLIENT_SECRET = MS_SECRET

class SentinelAPI(API_interface):

    def fetchAlerts(self, alert_ids: list[str]):
        customer, headers, data, url = self.generateRequest(alert_ids)
        customer, response = self.postRequest(customer, headers, data, url)
        alerts = self.processResponse(customer, response)
        incident = []
        for response_tuples in alerts:
            response_dict, hasEvent = self.responseParser(response_tuples)
            alert = Alert(response_dict)
            if hasEvent:
                alert.setEntities(
                    self.eventFetcher(response_dict, customer, headers, url)
                )
            alert.setIOCs()
            incident.append(alert)
        # hasEvent is True if event data was fetched at least once.
        return incident

    def generateRequest(self, alert_ids: list[str]):
        """Generates a request for a specific alert ID set

        Args:
            alert_ids (str): Alert ID set 

        Returns:
            customer, headers, data, url: Necessary parameters for the Post request.
        """        

        # Load the JSON configuration with customer details
        with open("./services/sentinel/config/customers.json", "r") as f:
            customers = json.load(f)

        for customer in customers:
            workspace_id = customer["WorkspaceId"]
            tenant_id = customer["TenantId"]
            access_token = get_access_token(
                CLIENT_ID,
                CLIENT_SECRET,
                tenant_id,
                scope="https://api.loganalytics.io/.default",
            )

            # Set headers for API request
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }
            alert_string = f'"{alert_ids[0]}"'
            for alert_id in alert_ids[1:]:
                alert_string += f',"{alert_id}"'
            # KQL Query
            data = {
                "query": f"""SecurityAlert
                    | summarize arg_max(TimeGenerated, *) by SystemAlertId
                    | where SystemAlertId in({alert_string})"""
            }
            # API Endpoint
            url = f"https://api.loganalytics.io/v1/workspaces/{workspace_id}/query"

            return customer, headers, data, url

    def postRequest(self, customer: dict, headers: dict, data: str, url: str):
        """Sends Post request to the Alerter

        Args:
            customer (_type_): _description_
            headers (_type_): _description_
            data (_type_): Json object containing KQL query
            url (_type_): _description_

        Returns:
            _type_: _description_
        """
        hasEventQuery: bool = False
        response = requests.post(url, headers=headers, json=data)

        # Check response status
        return customer, response

    def processResponse(self, customer: dict, response: requests.Response):
        """Receives the response from Sentinel's API and parses it to a workable data structure

        Args:
            customer (dict): Customer data dictionary
            response (requests.Response): Response from Sentinel to be parsed.

        Returns:
            alerts: List of tuples that can be parsed into a dictionary (Entity Name: Value) 
        """  
        if response.ok:
            # Parse the response data
            response_data = response.json()["tables"][0]

            alerts = []

            for row in response_data["rows"]:
                response_tuples = []
                for i in range(len(response_data["columns"])):

                    response_tuples.append(
                        list(response_data["columns"][i].items()) + [row[i]]
                    )

                # Generate each alert from the response tuples and append it to the list of alerts
                response_tuples = [
                    tup
                    for tup in response_tuples
                    if tup[2] != None and ((not type(tup[2]) == str) or (tup[2]) != "")
                ]
                response_tuples.append([("name", "CustomerName"), 0, customer["Name"]])
                alerts.append(response_tuples)
            print(
                f"Successfully fetched alerts for {customer['Name']} - Status code: {response.status_code}"
            )
            return alerts

        else:
            print(
                f"Failed to fetch alerts for {customer['Name']} - Status code: {response.status_code}"
            )
            try:
                # Parse error details
                error_details = response.json()
                print("Error details:", json.dumps(error_details, indent=4))
            except json.JSONDecodeError:
                # Handle non-JSON error responses
                print("Failed to decode error response as JSON")
                print("Raw response:", response.text)
                

    def responseParser(self, response_tuples: list):
        """Parses the response list into a dictionary of entities. Additionally, it sends a new query to Sentinel's API 
        when the original query is available, and there are missing entities from the original query in the response tuples

        Args:
            response_tuples (list): Sentinel's response processed by `SentinelAPI.processResponse`

        Returns:
            entities_dict: Dictionary of Key(Entity Name):Value(Entity)
        """        
        elements = {}
        hasEventQuery = False
        # print(f'{response_tuples=}')
        for elem in response_tuples:
            if len(elem) > 3:
                response_tuples = response_tuples[0]
        for name, _, value in response_tuples:

            if name[0] == "name":
                elements[name[1]] = value
        if "ExtendedProperties" in elements:
            elements["ExtendedProperties"] = json.loads(elements["ExtendedProperties"])
            hasEventQuery = "Query" in elements["ExtendedProperties"]
        return elements, hasEventQuery

    def eventFetcher(self, response_dict, customer, headers, url):
        print("Event data found! Fetching data...\n")
        # Get Original Query instead of Query, in case the key exists.
        if "OriginalQuery" in response_dict["ExtendedProperties"]:
            query = response_dict["ExtendedProperties"]["OriginalQuery"]
        else:
            query = response_dict["ExtendedProperties"]["Query"]

        startTime = response_dict["ExtendedProperties"]["Query Start Time UTC"]
        endTime = response_dict["ExtendedProperties"]["Query End Time UTC"]

        # KQL Query

        kqlQuery = KQLQuery(query, startTime, endTime)
        data = {"query": str(kqlQuery)}
        customer, response = self.postRequest(customer, headers, data, url)
        response_tuples = self.processResponse(customer, response)
        entities_dict, _ = self.responseParser(response_tuples)
        return entities_dict
