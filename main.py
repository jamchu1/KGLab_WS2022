from KGLab_WS2022.database_utils import DatabaseUtils
from KGLab_WS2022.event_predictor import EventPredictor
from KGLab_WS2022.ui import Globals, initUI
from KGLab_WS2022.generator_analyser import GenAnalyser

print("extracting from DB")
Globals.table = DatabaseUtils.extract_events()

# start generator analysis
ga = GenAnalyser()
ga.analyse(Globals.table)

print("initializing Predictor")
Globals.eventPredictor = EventPredictor()

# start the ui
initUI()
