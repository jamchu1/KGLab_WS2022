from dataclasses import dataclass
from event import Event

@dataclass
class PastEvent(Event):
    wikidataId: str

@staticmethod
def fromDBEvent(event):
    return PastEvent(
        eventTitle=event["title"],
        country=event["country"],
        startDate=event["startDate"],
        endDate=event["endDate"],
        year=event["year"],
        homepage=event["homepage"],
        wikidataId=["eventseriesId"],
        # could be None
        location=event.get("location"),
        language=event.get("language"),
    )