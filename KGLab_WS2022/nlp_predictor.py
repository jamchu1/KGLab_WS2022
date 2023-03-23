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
        generator = None
        generatorTag = beautifulSoup.find("meta", {"name":"generator"})
        if generatorTag:
            generator = generatorTag['content']
        pageText = beautifulSoup.get_text()[:700]
            
        tokenSequence = self.eParser.parse(eventReference=pageText, eventContext=None, show=False)
        cityMatches = tokenSequence.getTokenOfCategory("city")
        yearMatches = tokenSequence.getTokenOfCategory("year")
        ordinalMatches = tokenSequence.getTokenOfCategory("Ordinal")
        countryMatches = tokenSequence.getTokenOfCategory("country")
        
        country=self.getFirst(countryMatches)
        location=self.getFirst(cityMatches)
        ordinal=self.getFirst(ordinalMatches)
        year=self.getFirst(yearMatches)

        # return None if nothing was predicted
        if all(val is None for val in [country, location, ordinal, year, generator]):
            return

        return PredEvent(
            country=country,
            endDate=None,
            eventTitle=None,
            homepage=None,
            language=None,
            location=location,
            ordinal=ordinal,
            series=series,
            sourceURL=series.homepage,
            startDate=None,
            year=year,
            generator=generator
        )
    
    def getFirst(self, tokenList):
        if len(tokenList) == 0:
            return None
        else:
            return tokenList[0].tokenStr
