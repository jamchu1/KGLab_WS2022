from tests.basetest import Basetest
from KGLab_WS2022.database_utils import DatabaseUtils

class TestTest(Basetest):
    """
    test the wikidata search
    """
    
    def test_readDB(self):
        events = DatabaseUtils.readDB()

        self.assertGreater(len(events), 0)
        pass
    