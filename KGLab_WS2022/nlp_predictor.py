from KGLab_WS2022.series import Series
from KGLab_WS2022.pred_event import PredEvent
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from plp import eventrefparser

class NLPPredictor:
    def predict(self, series: Series):

        # TODO check if homepage exists
        session = HTMLSession()
        html = session.get(series.homepage).text
        beautifulSoup = BeautifulSoup(html, features="lxml")
        pageText = beautifulSoup.get_text()

        print(pageText)

        eParser = eventrefparser.EventReferenceParser()
        tokenSequence = eParser.parse(eventReference=pageText, eventContext=None, show=False)
        #acronymMatches = tokenSequence.getTokenOfCategory("acronym")
        #cityPrefixMatches = tokenSequence.getTokenOfCategory("cityPrefix")
        cityMatches = tokenSequence.getTokenOfCategory("city")
        yearMatches = tokenSequence.getTokenOfCategory("year")
        ordinalMatches = tokenSequence.getTokenOfCategory("Ordinal")
        countryMatches = tokenSequence.getTokenOfCategory("country")
        #monthMatches = tokenSequence.getTokenOfCategory("month")

        return PredEvent(
            country=self.getFirst(countryMatches),
            endDate="",
            eventTitle="",
            homepage="",
            language="",
            location=self.getFirst(cityMatches),
            ordinal=self.getFirst(ordinalMatches),
            series="",
            sourceURL="",
            startDate="",
            year=self.getFirst(yearMatches)
        )
    
    def getFirst(self, tokenList):
        if len(tokenList) == 0:
            return None
        return tokenList[0].tokenStr
