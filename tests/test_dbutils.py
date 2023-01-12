from tests.basetest import Basetest
from KGLab_WS2022.database_utils import DatabaseUtils
import os

class TestTest(Basetest):
    """
    test the wikidata search
    """
    
    def test_read_events_fromDB(self):
        table = DatabaseUtils.extract_events()
        debug=self.debug
        debug=True
        if debug:
            print(f"found {len(table.eventseriesList)} events!")
        
        self.assertGreater(len(table.eventseriesList), 0)
        pass
    