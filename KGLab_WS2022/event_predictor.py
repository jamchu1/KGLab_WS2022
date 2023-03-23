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
        if not url_prediction and not nlp_prediction:
            return
        else:
            if not nlp_prediction:
                return url_prediction
            if not url_prediction:
                return nlp_prediction
            # get dict and filter out None value
            filteredDict = {key:value for (key,value) in url_prediction.__dict__.items() if value}
            # merge predictions
            nlp_prediction.__dict__.update(filteredDict)
            return nlp_prediction

    def predict(self, series: Series):
        url_prediction = self.url_predictor.predict(series)
        nlp_prediction = self.nlp_predictor.predict(series)

        return self.combine_results(url_prediction, nlp_prediction)