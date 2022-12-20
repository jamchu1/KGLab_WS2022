from tests.basetest import Basetest
from KGLab_WS2022.url_predictor import URLPredictor
from KGLab_WS2022.past_event import PastEvent
from KGLab_WS2022.series import Series

class URLPredictorTest(Basetest):
    """
    test the URL Predictorwikidata search
    """
    
    def test_check_homepage(self):
        # empty/invalid url        
        self.assertEqual(
            URLPredictor.check_homepage(self, ""),
            False
        )

        # valid url
        self.assertEqual(
            URLPredictor.check_homepage(self, "https:///google.com/"),
            False        
        )

        pass

    '''
    I couldn't find an example event yet, where the ordinal number appears in the homepage-url. Maybe this is not necessary?
    def test_predict_ordinal(self):
        
    '''

    def test_predict_year(self):
        mock_past_event = PastEvent(
            eventTitle = "10th International Conference on Enterprise Information Systems",
            country = "Spain",
            startDate = "2008-06-12 00:00:00",
            endDate = "2008-06-16 00:00:00",
            year = "2008",
            homepage = "https://iceis.scitevents.org/ICEIS2008/",
            ordinal = "10",
            location = "Barcelona",
            language = None,
            wikidataId = "Q110502192"
        )
        
        mock_series = Series(acronym="WebIST", title="Web Information Systems and Technologies", homepage="http://www.webist.org/", eventList=[mock_past_event])

        url_predictor = URLPredictor()
        pred_event = url_predictor.predict(mock_series)
        
        self.assertEqual(pred_event.eventTitle, mock_past_event.eventTitle)
        self.assertEqual(pred_event.sourceURL, "https://iceis.scitevents.org/ICEIS2008/")
        self.assertEqual(pred_event.homepage, "https://iceis.scitevents.org/ICEIS2009/")
        self.assertEqual(pred_event.year, "2009")
        
