from tests.basetest import Basetest
from KGLab_WS2022.database_utils import DatabaseUtils

class TestTest(Basetest):
    """
    test the wikidata search
    """
    
    def test_read_events_fromDB(self):
        dbfile="/Users/wf/.conferencecorpus/EventCorpus.db"
        events = DatabaseUtils.extract_events(dbfile)
        debug=self.debug
        debug=True
        if debug:
            print(f"found {len(events)} events!")
        self.assertGreater(len(events), 0)
        pass
    