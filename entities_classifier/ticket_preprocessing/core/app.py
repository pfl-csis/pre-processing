from datetime import datetime
from api.api import API
import dash_bootstrap_components as dbc

alerts = None
tickets = None 
api = API()

def fetch_data(startTime:str,
         endTime:str = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
         targetAlerters = None,
         additionalFilters = None):
    
    
    
    t = api.get_ticket("658562237")
    print(t.description)

    return t
    
ticket = fetch_data("2023-09-13")

