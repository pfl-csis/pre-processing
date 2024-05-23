# Entities Heuristics

The goal of the module is to process all tickets and create a model that is able to generate a list of necessary Entities for an incident:


## Phase 1: Data Extraction

1. *Tickets* - Collection of tickets. Will be fetched from the api and likely stored as txt files.

2. *Ticket* - Object representing each individual ticket.


3. *processedTicket* - Compressed ticket object containing only relevant data.
   
    The processed ticket contains:
    - created -> used to calculate freshness 
    - owner -> discovered from *owners*
    - creator 
    - alerts -> discovered from *related_items*
    - severity -> converted to int
    - title -> might not be necessary
    - description -> see next item

4. *description* - Needs to be processed:
    ### Skeleton:
    ```
    Alert Name Section

    ## Entities
    ————————————————————————————
    Entities are started by the above delimiter or a variation of it
    Cases:

    key: val - val is delimited by '\n'

    key: val - multiline: harder to process. Can look for next 'key:' pattern. It's necessary to avoid reading words that contain ':' (IPs,etc) as keys. Using GPT here might be a solution

    logs/other data - This is case specific and will be ignored


    ## Investigation/Actions Performed:
    ————————————————————————————
    Text with analyst investigation.

    ## Conclusions/Recommendations:
    ————————————————————————————
    Text that can be used to weight the ticket.
    ```

    This can be converted to a simple dictionary containing the following key value pairs:

    "entities": Entities:set
    "conclusion": Conlusion:str
    For performance this can be further optimized into a tuple:
    
    description = (Entities: set,conclusion: str)
















```py


def model(Incident):

    incidentName:str = Incident["incidentName"]
    entities:dict = Incident["entities"]
    
    model_entities:dict = h(incidentName, entities)

    for key in entities:
        if key in model_entities:
            model_entities[key] = entities[key]

    return model_entities


def h(incidentName, entities):





```