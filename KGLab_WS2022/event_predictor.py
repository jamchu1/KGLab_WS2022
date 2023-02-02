from KGLab_WS2022.series import Series
from KGLab_WS2022.pred_event import PredEvent
from KGLab_WS2022.url_predictor import URLPredictor
from KGLab_WS2022.nlp_predictor import NLPPredictor

class EventPredictor:
    def combine_results(self, url_prediction, nlp_prediction):
        if url_prediction:
            return url_prediction
        elif nlp_prediction:
            return nlp_prediction
        else:
            return

    def predict(self, series: Series):
        url_predictor = URLPredictor()
        nlp_predictor = NLPPredictor()

        url_prediction = url_predictor.predict(series)
        nlp_prediction = nlp_predictor.predict(series)

        return self.combine_results(url_prediction, nlp_prediction)