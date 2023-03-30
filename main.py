from KGLab_WS2022.database_utils import DatabaseUtils
from KGLab_WS2022.event_predictor import EventPredictor
from KGLab_WS2022.ui import Globals, initUI
from KGLab_WS2022.generator_analyser import GenAnalyser

print("extracting from DB")
Globals.table = DatabaseUtils.extract_events()

print("initializing Predictor")
Globals.eventPredictor = EventPredictor()

#Starts the UI
initUI()