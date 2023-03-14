from KGLab_WS2022.series import Series
from KGLab_WS2022.pred_event import PredEvent
from KGLab_WS2022.url_predictor import URLPredictor
from KGLab_WS2022.nlp_predictor import NLPPredictor
from KGLab_WS2022.table import Table
import requests
from bs4 import BeautifulSoup
import json
from KGLab_WS2022.database_utils import Download 
import matplotlib.pyplot as plt
import math
from scipy import stats
from newspaper import Article
import seaborn as sns

class PredAnalyser:

    def count_predictions(self, table: Table):
        url_predictor = URLPredictor()
        nlp_predictor = NLPPredictor()

        prediction_made_url = 0
        latest_event_has_homepage = 0
        prediction_made_nlp = 0
        series_has_homepage = 0
        total = 0

        for series in table.eventseriesList:
            pred_event_url = url_predictor.predict(series)
            if pred_event_url:
                prediction_made_url += 1
            latest_event = url_predictor.get_latest_event(series)
            if latest_event and latest_event.homepage:
                latest_event_has_homepage += 1

            if nlp_predictor.predict(series):
                prediction_made_nlp += 1
            if series.homepage:
                series_has_homepage += 1
            total += 1
            if total % 10 == 0:
                print(total)
        
        print(f'The URLPredictor made predictions for {prediction_made_url}/{total} = {prediction_made_url/total} of the series')
        print(f'The NLPPredictor made predictions for {prediction_made_nlp}/{total} = {prediction_made_nlp/total} of the series')
        print(f'{latest_event_has_homepage}/{total} = {latest_event_has_homepage/total} of the latest events of the series have a homepage associated with it')
        print(f'{series_has_homepage}/{total} = {series_has_homepage/total} of the series have a homepage associated with it')