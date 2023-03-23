from KGLab_WS2022.series import Series
from KGLab_WS2022.pred_event import PredEvent
from KGLab_WS2022.event import Event
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

    def create_potential_homepages(self, homepage: str, year: int):
        pred_homepages = []

        if year and homepage:
            year_shortened = year % 100
            if str(year) in homepage:
                for i in range(1,6):
                    pred_homepages.append(homepage.replace(str(year), str(year + i)))
            elif str(year_shortened) in homepage:
                for i in range(1,6):
                    year_shortened_plus_i = (year_shortened + i) % 100
                    pred_homepages.append(homepage.replace(str(year_shortened), str(year_shortened_plus_i)))

        return pred_homepages
    
    def create_pred_event(self, series: Series, last_event: Event, homepage: str, year_offset: int):
        try:
            pred_ordinal = int(last_event.ordinal)+1
        except:
            pred_ordinal = None
        return PredEvent(
            eventTitle=last_event.eventTitle,
            country=None,
            year=int(last_event.year) + year_offset,
            homepage=homepage,
            ordinal=pred_ordinal,
            location=None,
            startDate=None,
            endDate=None,
            language=None,
            sourceURL=last_event.homepage,
            series=series,
            generator=None
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