from KGLab_WS2022.database_utils import DatabaseUtils
from KGLab_WS2022.event_predictor import EventPredictor
from KGLab_WS2022.ui import Globals, initUI
from KGLab_WS2022.generator_analyser import GenAnalyser
from KGLab_WS2022.prediction_analyzer import PredAnalyser
from KGLab_WS2022.series import Series
from KGLab_WS2022.url_predictor import URLPredictor

print("extracting from DB")
Globals.table = DatabaseUtils.extract_events()

urlPredictor = URLPredictor()

countTested = 0
countSuccess = 0
for series in Globals.table.eventseriesList:
    if len(series.eventList) < 2:
        continue

    last_event = series.eventList[0]
    if last_event.year:
        last_year = int(last_event.year)
    else:
        last_year = 0
    for event in series.eventList:
        if event.year and int(event.year) > last_year:
            last_event = event
            last_year = int(event.year)
    
    second_last_event = series.eventList[0]
    if second_last_event.year:
        second_last_year = int(second_last_event.year)
    else:
        second_last_year = 0
    for event in series.eventList:
        if event.year and int(event.year) > second_last_year and int(event.year) < last_year:
            second_last_event = event
            second_last_year = int(event.year)

    if not last_event.homepage or not second_last_event.homepage:
        continue
    predictedURLs = urlPredictor.create_potential_homepages(second_last_event.homepage, second_last_year)
    if last_event.homepage in predictedURLs:
        countSuccess += 1
    countTested += 1

print(f"tested {countTested} series by url prediction")
print(f"{countSuccess} of them were successfully predicted")