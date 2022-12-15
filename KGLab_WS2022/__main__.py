from database_utils import DatabaseUtils
from event import Event
from past_event import PastEvent
from pred_event import PredEvent
from series import Series

from lodstorage.sparql import SPARQL



table = DatabaseUtils.extract_events()
for series in table.eventseriesList:
    print(str(series.acronym) + " " + str(series.title) + " " + str(series.homepage))
    for event in series.eventList:
        print(event)
    print()
print()
    