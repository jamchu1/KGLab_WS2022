from tests.basetest import Basetest
from KGLab_WS2022.database_utils import DatabaseUtils

class TestWikidataSearch(Basetest):
    """
    test the wikidata search
    """
    
    def test_mock(self):
        data = DatabaseUtils.readDB()
        self.assertGreater(len(data), 0)
        pass
    