from dataclasses import dataclass

@dataclass
class Event:
    eventTitle: str
    location: str
    country: str
    startDate: str
    endDate: str
    year: str
    language: str
    homepage: str
    ordinal: str