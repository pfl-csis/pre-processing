from dataclasses import dataclass
from services.incident.entities import Entities as Entities_
from services.incident.iocExtractor import IocExtractor


@dataclass
class Alert:

    TimeGenerated: str = None
    AlertName: str = None
    AlertSeverity: str = None
    SystemAlertId: str = None
    ProductName: str = None
    Entities: Entities_ = None
    Tactics: str = None
    Techniques: str = None
    TenantId: str = None
    AlertLink: str = None
    Description: str = None
    CustomerName: str = None

    def __init__(self, response_dict: str) -> None:
        for key, value in response_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def setEntities(self, entities: dict):
        self.Entities = Entities_(entities).entities

        
    def setIOCs(self):
        extractor = IocExtractor()
        self.iocs = extractor.extract_iocs_from_alert(self)
