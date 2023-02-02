from KGLab_WS2022.database_utils import DatabaseUtils
from KGLab_WS2022.event_predictor import EventPredictor
from lodstorage.sparql import SPARQL

table = DatabaseUtils.extract_events()

'''
for series in table.eventseriesList:
    print(str(series.acronym) + " " + str(series.title) + " " + str(series.homepage))
    for event in series.eventList:
        print(event)
    print()
print()
'''

event_predictor = EventPredictor()

for series in table.eventseriesList:
    pred_event = event_predictor.predict(series)
    series.eventList.append(pred_event)
    print(pred_event)

'''
for series in table.eventseriesList:
    print(str(series.acronym) + " " + str(series.title) + " " + str(series.homepage))
    for event in series.eventList:
        print(event)
    print()
print()
'''