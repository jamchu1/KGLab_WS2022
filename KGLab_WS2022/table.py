from dataclasses import dataclass
from dataclasses import field
from KGLab_WS2022.series import Series

@dataclass
class Table:
    eventseriesList: list[Series] = field(default_factory=list)