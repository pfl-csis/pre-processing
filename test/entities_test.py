from services.alertEnrichment.dande_query import enrich_iocs
from testSettings import *

class EntitiesTest(unittest.TestCase, TestSettings):

    alert = None
    entities = None

    def setUp(self):
        alert_ids = [
            "ec8b7f48-2019-20cc-4532-5053d5a904dd",
            "95c2f1fe-db81-e3c0-4caa-45484a7aa72d",
            "de194a8a-9f98-c720-3638-1510f3837434",
            "a9456705-940b-27af-519b-1ab4491807f8",
            "e9b8c1e7-d9da-3d27-891f-4021d3685330",
            "a80c1056-704f-9aff-81f0-d57781fe54e0",
        ]
        if TestSettings.profiling:
            self.alert = self.profile_main(main, alert_ids)[0]
        else:
            self.alert = main(alert_ids)[0]
        
        # Enrichment to iocs
        enrich_iocs(self.alert.iocs)

        self.entities = self.alert.Entities
        print(f"Loaded Alert: {self.alert.AlertName}")

    def tearDown(self) -> None:
        self.alert = None
        self.entities = None
        return super().tearDown()


    def test_Entities(self):
        # Verify string vals
        self.assertEqual(
            self.entities["TimeGenerated"], r"2024-02-16T11:45:49.4669277Z"
        )

        # Verify int vals:
        self.assertEqual(self.entities["EventCount"], 1)
        target_key_amount = 28 + 1
        self.assertEqual(len(self.entities), target_key_amount)

    def test_keys(self):
        pass
        # Check if all entities were loaded


if __name__ == "__main__":
    unittest.main()
