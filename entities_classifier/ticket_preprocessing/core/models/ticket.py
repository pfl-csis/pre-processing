"""
Tag: Ticket model
File: models/ticket.py

Summary: File is intended to keep a model for the ticket object, fetched from the API.
Keys are explicitly defined to allow for easier lookup, if needed to be used in the future.

Notes:
setAttr could be used but it's not as readable as defining the keys explicitly. 

Author(s): 
    Daniel Brenet  | dab@csis.com
    Paulo Lima     | pfl@csis.com
Date: 07/07/2023
Version: 1.0
"""
from dataclasses import dataclass 
from typing import List, Optional

# Import models used in ticket.py
from .comment import Comment
from .relateditem import RelatedItem


@dataclass
class Ticket:
    """ Ticket object model """
    cirk_reference: Optional[str]
    closed: Optional[str]
    created: str
    creator: str
    customer_reference: str
    description: str
    id: int
    infection_vector_id: int
    owners: List[str]
    parent_id: Optional[int]
    related_items: List[RelatedItem]
    severity: str
    status: str
    title: str
    type: str
    comments: List[Comment]



