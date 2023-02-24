from KGLab_WS2022.series import Series
from KGLab_WS2022.pred_event import PredEvent
from KGLab_WS2022.table import Table
import requests
from bs4 import BeautifulSoup
import json
from KGLab_WS2022.database_utils import Download 
import matplotlib.pyplot as plt
import math
from scipy import stats
from newspaper import Article
import seaborn as sns

class GenAnalyser:

    def yield_homepages(self, table: Table):
        count = 0
        for series in table.eventseriesList:
            for event in series.eventList:
                count += 1
                if count % 100 == 0:
                    print(count)
                if not event.homepage:
                    continue
                yield (event.homepage, series.acronym)

    def gather_pub_dates(self, table: Table):
            for homepage, acronym in self.yield_homepages(table):
                pd = ""
                keywords = []
                try:
                    article = Article(homepage)
                    article.download()
                    article.parse()
                    #article.nlp()
                    #keywords = article.keywords
                    pd = article.publish_date
                    title = article.title
                except:
                    keywords = []
                    pd = "error"
                print(f"{acronym} ({homepage}) {title}: {pd}")

    def gatherData(self, table: Table):
        print("gathering generator data")
        dict = {}
        
        for homepage, acronym in self.yield_homepages(table):
            html = requests.get(homepage, timeout=0.7)
            if not html:
                continue
            beautifulSoup = BeautifulSoup(html.text, features="lxml")
            generator = beautifulSoup.find("meta", {"name":"generator"})
            if not generator:
                continue
            content = generator['content']
            if not content in dict:
                dict[content] = [acronym]
            else:
                dict[content].append(acronym)
        
        # Serializing json
        json_object = json.dumps(dict, indent=4)
        
        # Writing to generators.json
        with open("KGLab_WS2022/analysis/generators.json", "w") as outfile:
            outfile.write(json_object)

    def analyse(self, table):
        if Download.isEmpty("KGLab_WS2022/analysis/generators.json"):       
            self.gatherData(table) 

        with open("KGLab_WS2022/analysis/generators.json", "r") as outfile:
            data = json.load(outfile)

            # create a list with generators and amount
            count = [{"generator": entry, "count": len(data[entry])} for entry in data]
            # sort the list with by amount descending
            count.sort(key=lambda e : -e["count"])
            # store in json file
            with open("KGLab_WS2022/analysis/results.json", "w") as targetfile:
                json_object = json.dumps(count, indent=4)
                targetfile.write(json_object)

    def plotData(self, file_name: str, confidence_interval=80):

        dictionary = json.load(open(file_name, 'r'))
        yAxis = []
        for item in dictionary:
            if math.log(item['count']) not in yAxis:
                yAxis.append(math.log(item['count']))
        
        xAxis = [*range(len(yAxis))]
        
        # calculate the linear regression manually to obtain the standard error and slope.
        slope, intercept, r, p, std_err = stats.linregress(xAxis, yAxis)
        '''
        def myfunc(x):
            return slope * x + intercept

        print(slope)
        print(std_err)
        
        mymodel = list(map(myfunc, xAxis))
        '''
        
        sns.regplot(x=xAxis, y=yAxis, ci=confidence_interval)

        plt.scatter(xAxis,yAxis)
        #plt.plot(xAxis, mymodel)
        #plt.plot(xAxis,yAxis, color='maroon', marker='o')
        plt.xlabel('generator')
        plt.ylabel('log(count)')
        plt.figtext(.65, .7, f"std_err = {round(std_err,5)}\nslope = {round(slope,5)}\nconf_interval = {confidence_interval}")

        plt.savefig('./KGLab_WS2022/analysis/plot.png')