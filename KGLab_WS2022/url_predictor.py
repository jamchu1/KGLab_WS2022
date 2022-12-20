from KGLab_WS2022.series import Series
from KGLab_WS2022.pred_event import PredEvent
import requests

class URLPredictor:
    def check_homepage(self, homepage: str):
        try:
            response = requests.get(homepage)
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            return False
    
    def predict(self, series: Series):
        last_event = series.eventList[len(series.eventList)-1]
        last_homepage = last_event.homepage
        
        #predict based on year, TODO: deal with the case, that eg 19 is used instead of 2019
        if last_event.year != None and last_event.year != "" and last_event.year in last_homepage:
            for i in range(1,6):
                pred_homepage = last_homepage.replace(last_event.year, str(int(last_event.year) + i))
                if self.check_homepage(pred_homepage):
                    try:
                        pred_ordinal = str(int(last_event.ordinal)+1)
                    except:
                        pred_ordinal = None
                    return PredEvent(
                        eventTitle=last_event.eventTitle,
                        country=None,
                        year=str(int(last_event.year) + i),
                        homepage=pred_homepage,
                        ordinal=pred_ordinal,
                        location=None,
                        startDate=None,
                        endDate=None,
                        language=None,
                        sourceURL=last_homepage,
                        series=series
                    )
        
        #predict based on ordinal number, TODO: find test case
        elif last_event.ordinal != None and last_event.ordinal != "" and last_event.ordinal in last_homepage:
            pred_homepage = last_homepage.replace(last_event.ordinal, str(int(last_event.ordinal)+1))
            if self.check_homepage(pred_homepage):
                return PredEvent(
                    eventTitle=last_event.eventTitle,
                    country=None,
                    year=None,
                    homepage=pred_homepage,
                    ordinal=str(int(last_event.ordinal)+1),
                    location=None,
                    startDate=None,
                    endDate=None,
                    language=None,
                    sourceURL=last_homepage,
                    series=series
                )