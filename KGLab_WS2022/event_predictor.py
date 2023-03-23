from KGLab_WS2022.series import Series
from KGLab_WS2022.pred_event import PredEvent
from KGLab_WS2022.url_predictor import URLPredictor
from KGLab_WS2022.nlp_predictor import NLPPredictor

class EventPredictor:

    url_predictor = None
    nlp_predictor = None

    def __init__(self):
        self.url_predictor = URLPredictor()
        self.nlp_predictor = NLPPredictor()

    def combine_results(self, url_prediction, nlp_prediction):
        if url_prediction and nlp_prediction:
            if nlp_prediction.eventTitle:
                pred_eventTitle = nlp_prediction.eventTitle
            else:
                pred_eventTitle = url_prediction.eventTitle

            if nlp_prediction.year:
                pred_year = nlp_prediction.year
            else:
                pred_year = url_prediction.year

            if nlp_prediction.year:
                pred_year = nlp_prediction.year
            else:
                pred_year = url_prediction.year

            if url_prediction.homepage:
                pred_homepage = url_prediction.homepage
            else:
                pred_homepage = nlp_prediction.homepage
            
            if nlp_prediction.ordinal:
                pred_ordinal = nlp_prediction.ordinal
            else:
                pred_ordinal = url_prediction.ordinal
            
            return PredEvent(
                eventTitle=pred_eventTitle,
                country=nlp_prediction.country,
                year=pred_year,
                homepage=pred_homepage,
                ordinal=pred_ordinal,
                location=nlp_prediction.location,
                startDate=nlp_prediction.startDate,
                endDate=nlp_prediction.endDate,
                language=nlp_prediction.language,
                sourceURL=f'{url_prediction.sourceURL}, {nlp_prediction.sourceURL}',
                series=url_prediction.series
            )
        elif url_prediction and not nlp_prediction:
            return url_prediction
        elif nlp_prediction and not url_prediction:
            return nlp_prediction
        else:
            return

    def predict(self, series: Series):
        url_prediction = self.url_predictor.predict(series)
        nlp_prediction = self.nlp_predictor.predict(series)

        return self.combine_results(url_prediction, nlp_prediction)