import re


class KQLQuery:

    query: str
    startTime: str
    endTime: str

    @classmethod
    def __init__(
        self, query: str, startTime: str, endTime: str, timeKey="timestamp"
    ) -> None:
        self.query = query
        self.startTime = startTime
        self.endTime = endTime
        self.timeFrameSentinel()

    @classmethod
    def timeFrameSentinel(self) -> None:

        timeFrame = f"| where TimeGenerated between (todatetime('{self.startTime}')..todatetime('{self.endTime}'))"

        # Search for the first Table name pattern in the KQL query
        regex = r"\|"
        match = re.search(regex, self.query)

        if match:
            insert_pos = match.start()
            self.query = self.query[:insert_pos] + timeFrame + self.query[insert_pos:]

        else:
            raise Exception(
                f"Could not find Table name in the Event query:\n {self.query}\n"
            )

    @staticmethod
    def findTimeKey(query):
        pass

    @classmethod
    def __str__(self) -> str:
        return str(self.query)
