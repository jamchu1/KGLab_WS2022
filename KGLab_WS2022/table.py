from dataclasses import dataclass
from dataclasses import field
from KGLab_WS2022.series import Series
from typing import List

@dataclass
class Table:
    eventseriesList: List[Series]