from tests.basetest import Basetest
from KGLab_WS2022.past_event import PastEvent
from KGLab_WS2022.pred_event import PredEvent
from KGLab_WS2022.event_predictor import EventPredictor

class EventPredictorTest(Basetest):
    
    def test_combine_results(self):
        mock_url_pred = PredEvent(
            eventTitle="title 1",
            country=None,
            year=2023,
            homepage="homepage",
            ordinal=None,
            location=None,
            startDate=None,
            endDate=None,
            language=None,
            sourceURL="sourceURL 1",
            series="series"
        )

        mock_nlp_pred = PredEvent(
            eventTitle="title 2",
            country=None,
            year=None,
            homepage=None,
            ordinal=17,
            location=None,
            startDate=None,
            endDate=None,
            language=None,
            sourceURL="sourceURL 2",
            series="series"
        )

        expected_combined_pred = PredEvent(
            eventTitle="title 2",
            country=None,
            year=2023,
            homepage="homepage",
            ordinal=17,
            location=None,
            startDate=None,
            endDate=None,
            language=None,
            sourceURL="sourceURL 1, sourceURL 2",
            series="series"
        )
     
        self.assertEqual(
            EventPredictor.combine_results(self, None, None),
            None
        )

        self.assertEqual(
            EventPredictor.combine_results(self, mock_url_pred, None),
            mock_url_pred
        )

        self.assertEqual(
            EventPredictor.combine_results(self, None, mock_nlp_pred),
            mock_nlp_pred
        )

        print(EventPredictor.combine_results(self, mock_url_pred, mock_nlp_pred))

        self.assertEqual(
            EventPredictor.combine_results(self, mock_url_pred, mock_nlp_pred),
            expected_combined_pred
        )

        pass