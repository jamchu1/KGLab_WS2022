from dataclasses import dataclass
from KGLab_WS2022.event import Event
from KGLab_WS2022.series import Series
import json

def _try(o):
    try:
        return o.__dict__
    except:
        return str(o)

@dataclass
class PredEvent(Event):
    sourceURL: str
    generator: str
    series: Series
    
    def to_JSON(self):
        return json.dumps(self, default=lambda o: _try(o), sort_keys=True, indent=0, separators=(',',':')).replace('\n', '')