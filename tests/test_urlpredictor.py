from tests.basetest import Basetest
from KGLab_WS2022.url_predictor import URLPredictor
from KGLab_WS2022.past_event import PastEvent
from KGLab_WS2022.series import Series

class URLPredictorTest(Basetest):
    """
    test the URL Predictorwikidata search
    """
    
    def test_check_homepage(self):
        # empty url        
        self.assertEqual(
            URLPredictor.check_homepage(self, ""),
            False
        )

        # invalid url
        self.assertEqual(
            URLPredictor.check_homepage(self, "bananabread"),
            False
        )

        # valid but nonexistant url
        self.assertEqual(
            URLPredictor.check_homepage(self, "bananabread.tv"),
            False
        )

        # valid and existant url
        self.assertEqual(
            URLPredictor.check_homepage(self, "https:///google.com/"),
            False        
        )

        pass

    def test_create_potential_homepages(self):
        # year exists and is contained in url
        url_predictor = URLPredictor()

        pred_homepages = url_predictor.create_potential_homepages("https://iceis.scitevents.org/ICEIS2008/", 2008)
        self.assertEqual(pred_homepages, ["https://iceis.scitevents.org/ICEIS2009/", "https://iceis.scitevents.org/ICEIS2010/", "https://iceis.scitevents.org/ICEIS2011/", "https://iceis.scitevents.org/ICEIS2012/", "https://iceis.scitevents.org/ICEIS2013/"])

        # year is None
        pred_homepages = url_predictor.create_potential_homepages("https://iceis.scitevents.org/ICEIS2008/", None)
        self.assertEqual(pred_homepages, [])

        # year exists but is not contained in url
        pred_homepages = url_predictor.create_potential_homepages("https://iceis.scitevents.org/ICEIS2007/", 2008)
        self.assertEqual(pred_homepages, [])

        pred_homepages = url_predictor.create_potential_homepages("https://aaai.org/Conferences/AAAI-23/", 2023)
        self.assertEqual(pred_homepages, ["https://aaai.org/Conferences/AAAI-24/", "https://aaai.org/Conferences/AAAI-25/", "https://aaai.org/Conferences/AAAI-26/", "https://aaai.org/Conferences/AAAI-27/", "https://aaai.org/Conferences/AAAI-28/"])

    def test_create_pred_event(self):
        #TODO
        self.assertEqual(1,1)

    def test_get_latest_event(self):
        #TODO
        self.assertEqual(1,1)

    def test_predict(self):
        mock_past_event = PastEvent(
            eventTitle = "10th International Conference on Enterprise Information Systems",
            country = "Spain",
            startDate = "2008-06-12 00:00:00",
            endDate = "2008-06-16 00:00:00",
            year = 2008,
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
        self.assertEqual(pred_event.year, 2009)
        
