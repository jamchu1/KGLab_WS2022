from dataclasses import dataclass
from dataclasses import field
from KGLab_WS2022.past_event import PastEvent
from typing import List

@dataclass
class Series:
    acronym: str
    title: str
    homepage: str
    eventList: List[PastEvent]

@staticmethod
def fromDBSeries(series):
    return Series(acronym=series["acronym"], title=series["title"], homepage=series["homepage"], eventList=[])