"""
Tag: Comments model
File: models/comments.py

Summary: File is intended to keep a model for the ticket object, fetched from thje API.
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
from typing import List, Optional

@dataclass
class Comment:
    """ Comment object model """
    attachments: List[str]
    comment: Optional[str]
    id: str
    type: str
    when: str
    who: Optional[str]
