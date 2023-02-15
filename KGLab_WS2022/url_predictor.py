from series import Series
from pred_event import PredEvent
import requests
from operator import attrgetter

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

    def create_potential_homepages(self, homepage, year):
        pred_homepages = []

        if year and homepage and str(year) in homepage:
        
            for i in range(1,6):
                pred_homepages.append(homepage.replace(str(year), str(int(year) + i)))
        
        return pred_homepages
    
    def create_pred_event(self, series, last_event, homepage, year_offset):
        try:
            pred_ordinal = str(int(last_event.ordinal)+1)
        except:
            pred_ordinal = None
        return PredEvent(
            eventTitle=last_event.eventTitle,
            country=None,
            year=str(int(last_event.year) + year_offset),
            homepage=homepage,
            ordinal=pred_ordinal,
            location=None,
            startDate=None,
            endDate=None,
            language=None,
            sourceURL=last_event.homepage,
            series=series
        )

    def get_latest_event(self, series):
        if series.eventList:
            last_event = series.eventList[0]
            if last_event.year:
                last_year = int(last_event.year)
            else:
                last_year = 0
            for event in series.eventList:
                if event.year and int(event.year) > last_year:
                    last_event = event
                    last_year = int(event.year)
            return last_event
        else:
            return

    def predict(self, series: Series):
        last_event = self.get_latest_event(series)
        if not last_event:
            return

        last_homepage = last_event.homepage

        pred_homepages = self.create_potential_homepages(last_homepage, last_event.year)

        for year_offset, homepage in enumerate(pred_homepages,1):
            if self.check_homepage(homepage):
                return self.create_pred_event(series, last_event, homepage, year_offset)
        
        '''
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
        '''