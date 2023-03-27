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
    last = series.eventList[len(series.eventList) - 1]
    secondLast = series.eventList[len(series.eventList) - 2]
    if not last.homepage or not secondLast.homepage or not secondLast.year:
        continue
    predictedURLs = urlPredictor.create_potential_homepages(secondLast.homepage, secondLast.year)
    if last.homepage in predictedURLs:
        countSuccess += 1
    countTested += 1

print(f"tested {countTested} series by url prediction")
print(f"{countSuccess} of them were successfully predicted")