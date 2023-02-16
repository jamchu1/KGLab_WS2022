from KGLab_WS2022.series import Series
from KGLab_WS2022.pred_event import PredEvent
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from plp import eventrefparser

class NLPPredictor:

    eParser = None

    def __init__(self):
        self.eParser = eventrefparser.EventReferenceParser()

    def predict(self, series: Series):
        session = HTMLSession()
        try:
            html = session.get(series.homepage).text
        except:
            return None
        beautifulSoup = BeautifulSoup(html, features="lxml")
        pageText = beautifulSoup.get_text()[:700]
            
        tokenSequence = self.eParser.parse(eventReference=pageText, eventContext=None, show=False)
        cityMatches = tokenSequence.getTokenOfCategory("city")
        yearMatches = tokenSequence.getTokenOfCategory("year")
        ordinalMatches = tokenSequence.getTokenOfCategory("Ordinal")
        countryMatches = tokenSequence.getTokenOfCategory("country")
        
        #acronymMatches = tokenSequence.getTokenOfCategory("acronym")
        #cityPrefixMatches = tokenSequence.getTokenOfCategory("cityPrefix")
        #monthMatches = tokenSequence.getTokenOfCategory("month")

        return PredEvent(
            country=self.getFirst(countryMatches),
            endDate="",
            eventTitle="",
            homepage="",
            language="",
            location=self.getFirst(cityMatches),
            ordinal=self.getFirst(ordinalMatches),
            series='',#series,
            sourceURL=series.homepage,
            startDate="",
            year=self.getFirst(yearMatches)
        )
    
    def getFirst(self, tokenList):
        if len(tokenList) == 0:
            return None
        return tokenList[0].tokenStr
