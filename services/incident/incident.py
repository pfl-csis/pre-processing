from dataclasses import dataclass
from services.incident.alert import Alert


@dataclass
class Incident():
    id = 0
    incidentName: str = None
    uuid: str = None
    highest_severity: str = None
    alerts: list[Alert] = None
    entities: dict = None
    iocs: dict = None
    CustomerName: str = None
    enrichedIocs: dict = None # Enriched IOCs
    VTEnrichedIocs: dict = None  # VirusTotal Enriched IOCs
    
    # Enrichment function
    def update_enriched_iocs(self):
        self.enrichedIocs = {}
        for alert in self.alerts:
            if hasattr(alert, 'enrichedIocs'):
                self.enrichedIocs.update(alert.enrichedIocs)
                
    def update_vt_enriched_iocs(self, vt_enriched_iocs):
        self.VTEnrichedIocs = vt_enriched_iocs
        for alert in self.alerts:
            if hasattr(alert, 'VTEnrichedIocs'):
                self.VTEnrichedIocs.update(alert.VTEnrichedIocs)

    def __init__(self, alerts: list[Alert]) -> None:
        Incident.id += 1
        self.alerts = alerts
        self.setName()
        self.setSeverity()
        self.setEntities()
        self.setCustomer()
        self.setIOCs()
        self.enrichedIocs = {}  # IInitialization of enriched IOCs
        self.VTEnrichedIocs = {}  # Initialization of VirusTotal enriched IOCs

    def setName(self):
        """Sets an incident name according to the alert name frequency"""
        alertNames = [alert.AlertName for alert in self.alerts]
        self.incidentName = max(set(alertNames), key=alertNames.count)

    def setSeverity(self):
        """Sets an incident severity according to the highest severity alert"""
        self.highest_severity = max([alert.AlertSeverity for alert in self.alerts])

    def setEntities(self):
        """Sets the incident entities from all alerts in the incident, removing duplicate entries."""
        entities = [alert.Entities for alert in self.alerts]
        self.entities = {}
        repeated_keys = []
        for alert_entities in entities:
            for key, value in alert_entities.items():
                # Dealing with repeated entity names but different entities values
                if key in self.entities and self.entities[key] != value:
                    repeated_keys.append(key)
                    new_key_name = f"{key}{repeated_keys.count(key)}"
                    self.entities[new_key_name] = value
                # Repeated entities don't need special handling
                else:
                    self.entities[key] = value
    
    def setIOCs(self):
        """Sets the incident IOCs from all alerts in the incident, removing duplicate entries."""
        iocs = [alert.iocs for alert in self.alerts]
        self.iocs = {}
        repeated_keys = []
        for alert_iocs in iocs:
            for key, value in alert_iocs.items():
                # Dealing with repeated entity names but different entities values
                if key in self.iocs and self.iocs[key] != value:
                    repeated_keys.append(key)
                    new_key_name = f"{key}{repeated_keys.count(key)}"
                    self.iocs[new_key_name] = value
                # Repeated entities don't need special handling
                else:
                    self.iocs[key] = value

    
    def setCustomer(self):
        CustomerName = self.alerts[0].CustomerName
        for alert in self.alerts:
            if CustomerName != alert.CustomerName:
                raise Exception

        self.CustomerName = CustomerName

    def toDict(self):
        # Define a nested function to handle the recursion
        def _toDict(obj):
            if isinstance(obj, dict):
                return {k: _toDict(v) for k, v in obj.items()}
            elif hasattr(obj, "__dict__"):
                # Use vars(obj) to get the __dict__ attribute more safely
                return {
                    k: _toDict(v) for k, v in vars(obj).items() if not k.startswith("_")
                }
            elif isinstance(obj, list):
                return [_toDict(v) for v in obj]
            else:
                return obj

        # Start the recursion with self
        return _toDict(self)
