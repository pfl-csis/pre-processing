"""
Tag: Handler for ticket API calls
File: handlers/ticket.py

Summary: File is intended to keep everything related to the ticket API calls.
This naturally includes the ticket object model, as well as the API call itself.

Notes:
This file only returns the json encoded data, and does NOT return the entire Ticket, as 2 requests are needed to get all the information.
That's why it's discouraged to use this file directly, and instead use the api/api.py file, which will return the entire Ticket object.

Author(s): 
    Daniel Brenet  | dab@csis.com
    Paulo Lima     | pfl@csis.com

Date: 07/07/2023
Version: 1.0
"""

# Imports
from requests import get # Only import the needed function from the requests module, to avoid namespace pollution
import json 

# This is a shitty way to do this, but it's the only way I could think of to make separate the handlers from the main API class.
class Tickets():

    # Constructor
    def __init__(self, apiKey: str, url: str):
        self.apiKey = apiKey
        self.url = url


    def get_ticket_content(self, ticketId: str) -> json:
        """Get the ticket content from the API, and return it as a json object"""

        
        # Make sure the API Key and Ticket ID are provided, otherwise raise an error
        if self.apiKey is None or ticketId is None or self.url is None:
            raise ValueError("[ FATAL ] API Key, Ticket ID and URL must be provided. - handlers/ticket.py/__get_ticket_content__")
        
        # Check that the URL ends with a slash, otherwise add it
        if self.url[-1] != "/":
            self.url += "/"

        # Get the ticket content
        resp = get(self.url + "tickets/" + ticketId, headers={
            "Accept": "application/json",
            "Authorization": "Token " + self.apiKey # Non-standard API Auth?!?!?
        })

        # Check if the request was successful
        if resp.status_code != 200:
            raise ConnectionError("[ FATAL ] Could not get ticket content. - handlers/ticket.py/__get_ticket_content__")
        
        # Return the ticket content as a json object
        return resp.json()
    
    def get_ticket_comments(self, ticketId: str) -> json:
        """Get the ticket comments from the API, and return it as a json object"""

        # Make sure the API Key and Ticket ID are provided, otherwise raise an error
        if self.apiKey is None or ticketId is None or self.url is None:
            raise ValueError("[ FATAL ] API Key, Ticket ID and URL must be provided. - handlers/ticket.py/__get_ticket_comments__")
        
        # Check that the URL ends with a slash, otherwise add it
        if self.url[-1] != "/":
            self.url += "/"

        # Get the ticket content
        resp = get(self.url + "tickets/" + ticketId + "/thread", headers={
            "Accept": "application/json",
            "Authorization": "Token " + self.apiKey # Non-standard API Auth?!?!? 
        })

        # Check if the request was successful
        if resp.status_code != 200:
            raise ConnectionError("[ FATAL ] Could not get ticket comments. - handlers/ticket.py/__get_ticket_comments__")
        
        # Return the ticket content as a json object
        return resp.json()


    


