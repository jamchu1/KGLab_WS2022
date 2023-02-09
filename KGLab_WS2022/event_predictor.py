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
        if url_prediction:
            return url_prediction
        elif nlp_prediction:
            return nlp_prediction
        else:
            return

    def predict(self, series: Series):
        url_prediction = self.url_predictor.predict(series)
        nlp_prediction = self.nlp_predictor.predict(series)

        return self.combine_results(url_prediction, nlp_prediction)