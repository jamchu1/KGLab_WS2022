from dataclasses import dataclass
from dataclasses import field
from series import Series

@dataclass
class Table:
    eventseriesList: list[Series] = field(default_factory=list)