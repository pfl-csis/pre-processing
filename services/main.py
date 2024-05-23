from services.alert.alert import Alert
from services.alert.incident import Incident
from services.sentinel.api import SentinelAPI
# from services.alertEnrichment.dande_query import enrich_iocs
# from services.alertEnrichment.vt_query import enrich_iocs_vt

import json

def main(alert_ids) -> list[Alert]:
    api = SentinelAPI()
    alerts = api.fetchAlerts(alert_ids)
    incident = Incident(alerts)

    # # Enrichment 
    # enriched_iocs = enrich_iocs(incident.iocs)
    # incident.enrichedIocs = enriched_iocs
    
    # # VT Enrichment
    # vt_enriched_iocs = enrich_iocs_vt(incident.iocs)
    # incident.update_vt_enriched_iocs(vt_enriched_iocs)

    with open(f"outputs/incident{incident.id}.json", "w") as f:
        json.dump(incident.toDict(), f, indent=4)
    print("All alerts processed")

    return alerts


if __name__ == "__main__":
    main()
