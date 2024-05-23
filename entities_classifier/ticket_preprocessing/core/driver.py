"""
Main Driver

Reserved for the future.
"""

import api.api as api
from datetime import datetime

def main(startTime:str,
         endTime:str = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
         targetAlerters = None,
         additionalFilters = None):
    
    
    
    t = api.API().get_ticket("658562237")
    print(t.description)
      
if __name__ == "__main__":
    main("2023-09-01")