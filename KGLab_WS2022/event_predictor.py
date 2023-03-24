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
            merged_data = []

            # nlp prediction is preferred:
            keys = ["eventTitle", "ordinal"]
            for key in keys:
                if hasattr(nlp_prediction, key):
                    merged_data.append(getattr(nlp_prediction, key))
                else:
                    merged_data.append(getattr(url_prediction, key))

            # url prediction is preferred:
            keys = ["year", "homepage"]
            for key in keys:
                if hasattr(url_prediction, key):
                    merged_data.append(getattr(url_prediction, key))
                else:
                    merged_data.append(getattr(nlp_prediction, key))
            
            return PredEvent(
                eventTitle=merged_data[0],
                country=nlp_prediction.country,
                year=merged_data[2],
                homepage=merged_data[3],
                ordinal=merged_data[1],
                location=nlp_prediction.location,
                startDate=nlp_prediction.startDate,
                endDate=nlp_prediction.endDate,
                language=nlp_prediction.language,
                sourceURL=f'{url_prediction.sourceURL}, {nlp_prediction.sourceURL}',
                series=url_prediction.series,
                generator=nlp_prediction.generator
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