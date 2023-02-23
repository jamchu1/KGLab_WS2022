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

class GenAnalyser:

    def gatherData(self, table: Table):
        print("gathering generator data")
        dict = {}
        count = 0
        
        for series in table.eventseriesList:
            for event in series.eventList:
                count += 1
                if count % 100 == 0:
                    print(count) 
                try:
                    if not event.homepage:
                        continue
                    #html = session.get(event.homepage, timeout=0.25)
                    html = requests.get(event.homepage, timeout=0.7)
                    if not html:
                        continue
                    beautifulSoup = BeautifulSoup(html.text, features="lxml")
                    generator = beautifulSoup.find("meta", {"name":"generator"})
                    if not generator:
                        continue
                    content = generator['content']
                    if not content in dict:
                        dict[content] = [series.acronym]
                    else:
                        dict[content].append(series.acronym)
                except:
                    pass
        
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

    def plotData(self, file_name: str):

        dictionary = json.load(open(file_name, 'r'))
        yAxis = []
        for item in dictionary:
            if math.log10(item['count']) not in yAxis:
                yAxis.append(math.log10(item['count']))
        
        xAxis = range(len(yAxis))
        
        #plt.grid(True)

        slope, intercept, r, p, std_err = stats.linregress(xAxis, yAxis)
        def myfunc(x):
            return slope * x + intercept

        mymodel = list(map(myfunc, xAxis))

        plt.scatter(xAxis,yAxis)
        plt.plot(xAxis, mymodel)
        #plt.plot(xAxis,yAxis, color='maroon', marker='o')
        plt.xlabel('generator')
        plt.ylabel('log(count)')

        plt.savefig('./KGLab_WS2022/analysis/plot.png')