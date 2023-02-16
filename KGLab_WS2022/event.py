from dataclasses import dataclass

@dataclass
class Event:
    eventTitle: str
    location: str
    country: str
    startDate: str
    endDate: str
    year: int
    language: str
    homepage: str
    ordinal: int