from dataclasses import dataclass
from KGLab_WS2022.event import Event

@dataclass
class PastEvent(Event):
    wikidataId: str

def fromDBEvent(event):
    year = event["year"]
    if year is not None and type(year) is not int:
        year = int(year)
    ordinal = event.get("ordinal")
    if ordinal is not None and type(ordinal) is not int:
        ordinal = int(ordinal)
    return PastEvent(
        eventTitle=event["title"],
        country=event["country"],
        startDate=event["startDate"],
        endDate=event["endDate"],
        year=year,
        homepage=event["homepage"],
        ordinal=ordinal,
        wikidataId=event.get("eventseriesId"),
        location=event.get("location"),
        language=event.get("language"),
    )