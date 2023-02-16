from dataclasses import dataclass
from KGLab_WS2022.event import Event

@dataclass
class PastEvent(Event):
    wikidataId: str

def fromDBEvent(event):
    return PastEvent(
        eventTitle=event["title"],
        country=event["country"],
        startDate=event["startDate"],
        endDate=event["endDate"],
        year=event["year"],
        homepage=event["homepage"],
        # could be None
        ordinal=event.get("ordinal"),
        wikidataId=event.get("eventseriesId"),
        location=event.get("location"),
        language=event.get("language"),
    )