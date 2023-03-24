from tests.basetest import Basetest
from KGLab_WS2022.url_predictor import URLPredictor
from KGLab_WS2022.past_event import PastEvent
from KGLab_WS2022.series import Series

class URLPredictorTest(Basetest):

    '''
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
    '''

    '''
    self.assertEqual(pred_event.eventTitle, mock_past_event.eventTitle)
    self.assertEqual(pred_event.sourceURL, "https://iceis.scitevents.org/ICEIS2008/")
    self.assertEqual(pred_event.homepage, "https://iceis.scitevents.org/ICEIS2009/")
    self.assertEqual(pred_event.year, 2009)        
    '''

    test_data = [
        {
            "mock_series": Series(acronym="WebIST", title="Web Information Systems and Technologies", homepage="http://www.webist.org/", eventList=
                [PastEvent(
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
                )]
            ),
            "expected_result": {
                "eventTitle": "10th International Conference on Enterprise Information Systems",
                "country": None,
                "startDate": None,
                "endDate": None,
                "year": 2009,
                "homepage": "https://iceis.scitevents.org/ICEIS2009/",
                "ordinal": 11,
                "location": None,
                "language": None
            }
        },
        {
            "mock_series": Series(
                acronym="OAT",
                title="Open-Access-Tage",
                homepage="https://open-access.net/community/open-access-tage",
                eventList=
                [PastEvent(
                    eventTitle = "Open-Access-Tage 2021",
                    country = None,
                    startDate = "2021-09-27 00:00:00",
                    endDate = "2021-09-29 00:00:00",
                    year = 2021,
                    homepage = "https://open-access.net/community/open-access-tage-2021-online",
                    ordinal = 15,
                    location = None,
                    language = None,
                    wikidataId = "Q107487087"
                ),
                PastEvent(
                    eventTitle = "Open-Access-Tage 2019",
                    country = None,
                    startDate = "2019-09-30 00:00:00",
                    endDate = "2019-10-02 00:00:00",
                    year = 2019,
                    homepage = "https://open-access.net/community/open-access-tage/open-access-tage-2019",
                    ordinal = 13,
                    location = "Hanover",
                    language = None,
                    wikidataId = "Q97613875"
                ),
                PastEvent(
                    eventTitle = "Open-Access-Tage 2018",
                    country = "Austria",
                    startDate = "2018-09-24 00:00:00",
                    endDate = "2018-09-26 00:00:00",
                    year = 2018,
                    homepage = "https://open-access.net/community/open-access-tage/open-access-tage-2018-graz",
                    ordinal = 12,
                    location = "Graz",
                    language = None,
                    wikidataId = "Q97613949"
                )]
            ),
            "expected_result": {
                "eventTitle": "Open-Access-Tage 2021",
                "country": None,
                "startDate": None,
                "endDate": None,
                "year": 2022,
                "homepage": "https://open-access.net/community/open-access-tage-2022-online",
                "ordinal": 16,
                "location": None,
                "language": None
            }
        },
        {
            "mock_series": Series(
                acronym="ES",
                title="Empty Series",
                homepage=None,
                eventList=[]
            ),
            "expected_result": None
        }
    ]
    
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

        # year exists but is only contained in the url in shortened form
        pred_homepages = url_predictor.create_potential_homepages("https://aaai.org/Conferences/AAAI-23/", 2023)
        self.assertEqual(pred_homepages, ["https://aaai.org/Conferences/AAAI-24/", "https://aaai.org/Conferences/AAAI-25/", "https://aaai.org/Conferences/AAAI-26/", "https://aaai.org/Conferences/AAAI-27/", "https://aaai.org/Conferences/AAAI-28/"])

    def test_predict(self):
        url_predictor = URLPredictor()

        for case in self.test_data:
            pred_event = url_predictor.predict(case['mock_series'])
            if pred_event:
                for k, v in case['expected_result'].items():
                    self.assertEqual(pred_event.__dict__[k], v)
            else:
                self.assertEqual(case['expected_result'], None)
