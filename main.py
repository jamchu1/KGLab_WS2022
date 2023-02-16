from KGLab_WS2022.database_utils import DatabaseUtils
from KGLab_WS2022.event_predictor import EventPredictor
from KGLab_WS2022.ui import Globals, initUI

print("extracting from DB")
Globals.table = DatabaseUtils.extract_events()
print("initializing Predictor")
Globals.eventPredictor = EventPredictor()
# start the ui
initUI()
