from dataclasses import dataclass
from KGLab_WS2022.event import Event
from KGLab_WS2022.series import Series

@dataclass
class PredEvent(Event):
    sourceURL: str
    generator: str
    series: Series