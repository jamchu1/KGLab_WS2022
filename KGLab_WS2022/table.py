from dataclasses import dataclass
from dataclasses import field
from series import Series
from typing import List

@dataclass
class Table:
    eventseriesList: List[Series]