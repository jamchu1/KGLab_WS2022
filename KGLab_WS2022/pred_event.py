from dataclasses import dataclass
from event import Event
from series import Series

@dataclass
class PredEvent(Event):
    sourceURL: str
    series: Series