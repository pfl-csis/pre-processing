"""
Tag: Mapper module
File: api/mapper/map.py

Summary: File is intended to keep a mapper function that converts a json object to a dataclass object.
This file is used to convert the json object fetched from the API to a dataclass objects, which is used in the application.

Notes:
The function json_to_dataclass_recursive is a recursive function that converts a json object to a dataclass object.
I had to solve a recurrence relation to calculate the time complexity of this function. The recurrence relation is explained in the function.

Took a sh*t ton of time to write this function, but it's worth it.

The reason why we don't want to use raw json objects in the application is because it's not as readable as dataclasses.


Author(s): 
    Daniel Brenet  | dab@csis.com
    Paulo Lima     | pfl@csis.com
Date: 09/07/2023
Version: 1.0
"""

# Dependency Imports
from dataclasses import is_dataclass
from typing import Any, List
import json


"""
This is a recursive function that converts a json object to a dataclass object. It will also convert any nested dataclasses.


This code is somewhat tricky to optimize, I even had to solve a recurrence relation to calculate the time complexity of this function.

Recurence relation:
(*) n as the total number of basic data fields in the JSON object,
(*) d as the maximum depth of dataclasses (how many dataclasses are nested within each other),
(*) b as the maximum branching factor (the maximum number of fields in a dataclass),
(*) l as the maximum length of a list of dataclasses.

If we look at a level of recursion where the function is processing a dataclass (and not a list), the function does b work (it has to process b fields), 
and it makes b recursive calls (one for each field), each operating on a problem of size n/b (assuming each field contains roughly the same amount of data). 
This gives us the following recurrence relation:

T(n) = b*T(n/b) + b

However, if the function is processing a list of dataclasses, the situation is a bit different. The function does n work (it has to process n items), 
and it makes n recursive calls (one for each item), each operating on a problem of size roughly 1 (assuming each item is a dataclass with no nested dataclasses). 
This gives us the following recurrence relation:

T(n) = n*T(1) + n = 2n

So, the final complexity is dominated by the maximum of these two complexities as we recurse. In the worst case, 
we could assume that we alternate between processing a dataclass and processing a list of dataclasses at each level of recursion. 
In this case, the overall complexity would be O(b^d * n * l), 
because we have to process each of b^d fields of each of n basic data fields for each of l items in lists.

Best case: O(n)
Average case: O((b/2)^(d/2) * n * (l/2))
Worst case: O(b^d * n * l) We're screwed if this happens. But that's assuming we have json objects that are nested to the maximum depth xD

Since we don't have that much data in our API, we can assume that the Best case is the average case, which is O(n). Since we have a max of level 1 nesting.



Sorry for ranting, I just wanted to explain the complexity of this function.
- Daniel Brenet.
"""
def json_to_dataclass_recursive(json_obj: Any, dataclass_obj) -> Any:
    """ Convert JSON to dataclass object with nested dataclasses"""
    if is_dataclass(dataclass_obj):
        
        # If it's a dataclass, iterate over each field to check if any field needs recursive conversion
        for field in dataclass_obj.__dataclass_fields__.values():
            field_name = field.name
            field_type = field.type

            if isinstance(field_type, type) and is_dataclass(field_type) and field_name in json_obj:
                # If field is a dataclass, convert it
                json_obj[field_name] = json_to_dataclass_recursive(json_obj[field_name], field_type)

            elif (isinstance(field_type, List) and len(field_type.__args__) > 0 and 
                  isinstance(field_type.__args__[0], type) and is_dataclass(field_type.__args__[0]) and 
                  field_name in json_obj):
                # If field is a list of dataclasses, convert it
                json_obj[field_name] = [json_to_dataclass_recursive(item, field_type.__args__[0]) 
                                       for item in json_obj[field_name]]

        # Convert to dataclass object after converting all fields
        return dataclass_obj(**json_obj)
    else:
        return json_obj



# Unable to automatically map the json object to a dataclass that contains a list of dataclasses.
def json_to_dataclass(json_obj: json, dataclass_obj):
    """ Converts a json object to a dataclass object """
    if isinstance(json_obj, list):
        return [dataclass_obj(**item) for item in json_obj]
    elif isinstance(json_obj, dict):
        return dataclass_obj(**json_obj)
    

# Kind of a hacky way to merge json objects, but it works, sometimes xD.
def merge_json_objects(*json_objects: json):
    """ Merges multiple json objects into one """
    merged_dict = {} # Create an empty dict


    # Loop through each json object and merge it into the merged_dict
    # This will overwrite any duplicate keys, so it's important to keep the order of the json objects
    # It needs to be refactored but yeah it works for now.
    for json_obj in json_objects:
        merged_dict.update(json_obj)

    return merged_dict

