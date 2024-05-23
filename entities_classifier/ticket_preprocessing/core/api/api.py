"""
Tag: Main API class
File: api/api.py

Summary: This file is intended to be the main API class, 
         which will be used to interact with the API.

Notes:
    The reason why the code is split into multiple files is to make it easier to maintain and read.
    The handlers folder contains all the handlers for the API calls, and the api.py file contains the main API class.

    Furthermore keeping a high cohesion and low coupling design pattern is important, and this is achieved by splitting the code into multiple files
    This way we make sure that code is not split accross multiple files, and that each file has a single purpose. - Daniel Brenet

Author(s): 
    Daniel Brenet  | dab@csis.com
    Paulo Lima     | pfl@csis.com

Date: 07/07/2023
Version: 1.0
"""
# Dependency Imports
from os import environ
from .mapper.map import json_to_dataclass_recursive # Import the map module, which is used to map the API response to the object model

# Handler Imports
from .handlers.tickets import Tickets # Import the Tickets API handler

# Import Ticket object model
from models.ticket import Ticket

class API():
    def __init__(self) -> None:


        self.__apiKey   = environ["ECRIME_API_KEY"] # Get the API key from the environment variables (this is the recommended way to store sensitive data)
        self.__url      = environ["ECRIME_API_URL"] # Get the API URL; same as above - Daniel Brenet        # Should be in the form of https://api.csis.com/v1/ 

    def get_ticket(self, ticketId: str) -> Ticket:
        """Get the ticket from the API, and return it as a Ticket object"""

        # Object to Handler.
        handler = Tickets(self.__apiKey, self.__url)
        
        # Get the ticket content and comments this is super inefficient, but it's the only way to get all the data, 
        # since it's not apart of the ticket content for some reason.......???????????? - Daniel Brenet
        ticketContent = handler.get_ticket_content(ticketId)
        ticketContent["comments"] = handler.get_ticket_comments(ticketId)

        # Map the response to the object model
        ticket = json_to_dataclass_recursive(ticketContent, Ticket)

        # Return the ticket
        return ticket
        
