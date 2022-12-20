from KGLab_WS2022.database_utils import DatabaseUtils
from lodstorage.sparql import SPARQL

table = DatabaseUtils.extract_events()
for series in table.eventseriesList:
    print(str(series.acronym) + " " + str(series.title) + " " + str(series.homepage))
    for event in series.eventList:
        print(event)
    print()
print()
    