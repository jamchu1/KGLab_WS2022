from tests.basetest import Basetest
from KGLab_WS2022.database_utils import DatabaseUtils
import os

class TestTest(Basetest):
    """
    test the wikidata search
    """
    
    def test_read_events_fromDB(self):
        events = DatabaseUtils.extract_events()
        debug=self.debug
        debug=True
        if debug:
            print(f"found {len(events)} events!")
        self.assertGreater(len(events), 0)
        pass
    