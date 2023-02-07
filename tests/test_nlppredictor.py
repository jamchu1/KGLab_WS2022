from tests.basetest import Basetest
from KGLab_WS2022.past_event import PastEvent
from KGLab_WS2022.series import Series
from KGLab_WS2022.nlp_predictor import NLPPredictor

class NLPPredictorTest(Basetest):

    def testPrediction(self):
        mockPastEvent = PastEvent(
            eventTitle = "",
            country = "Spain",
            startDate = "2008-06-12 00:00:00",
            endDate = "2008-06-16 00:00:00",
            year = "2008",
            homepage = "http://www.percom.org/Previous/ST2016/",
            ordinal = "10",
            location = "Barcelona",
            language = None,
            wikidataId = "Q110502192"
        )
        
        mockSeries = Series(
            acronym="PERCOM",
            title="IEEE International Conference on Pervasive Computing and Communications",
            homepage="https://www.percom.org/",
            eventList=[mockPastEvent]
        )

        nlp = NLPPredictor()
        predEvent = nlp.predict(mockSeries)
        
        print(predEvent)
        self.assertEqual(predEvent.year, '2023')

        
