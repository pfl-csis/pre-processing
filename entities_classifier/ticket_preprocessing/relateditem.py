"""
Tag: RelatedItems model
File: models/relateditems.py

Summary: File is intended to keep a model for the ticket object, fetched from the API.
Keys are explciticly defined to allow foer easier lookup, if needed to be used in the future.

Notes:
setAttr could be used but it's not as readable as defining the keys explicitly. 

Author(s): 
    Daniel Brenet  | dab@csis.com
    Paulo Lima     | pfl@csis.com

Date: 07/07/2023
Version: 1.0
"""
from dataclasses import dataclass

@dataclass
class RelatedItem:
    """ RelatedItem object model """
    id: int
    title: str
    type: str



