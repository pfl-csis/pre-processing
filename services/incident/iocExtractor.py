


class IocExtractor:
    
    @staticmethod
    def extract(cls, entities: dict[str, str]) -> dict[str, str]:
        """The IOC Extractor employs AI to identify and extract the relevant IOCs for the incident.

        Args:
            entities (dict[str, str]): All Entities, as processed by the Alert Fetcher

        Returns:
            iocs dict[str, str]: Entities dictionary, with non IOC entries pruned. 
        """
        
        