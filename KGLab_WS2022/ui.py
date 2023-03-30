import justpy as jp

class Globals:
    table = None
    eventPredictor = None


#button click handler
def btn_click(self, msg):
    #user input of acronym
    input = self.source.value
    targetSeries = None

    #searching for scientific event series matching acronym
    for series in Globals.table.eventseriesList:
        if series.acronym == input:
            targetSeries = series
            break

    if targetSeries is None:
        #acronym does not match with an event series
        self.target[0].text = 'No series was found for the given acronym.'
    else:
        #acronym matches with an event series
        event = Globals.eventPredictor.predict(targetSeries)
        
        if event is None:
            #failure to predict next installment
            self.target[0].text = 'Could not predict next event of the series:' + series.title
        else:
            #success in predicting next installment
            self.target[0].text = 'Predicted data of the next event of the "' +  str(series.title)  + '" Series: ' \
            + '     |       Event Title: ' + str(event.eventTitle) \
            + '     |       Country: ' + str(event.country) \
            + '     |       Location: ' + str(event.location) \
            + '     |       Year: ' + str(event.year) \
            + '     |       Start Date: ' + str(event.startDate) \
            + '     |       End Date: ' + str(event.endDate) \
            + '     |       Language: ' + str(event.language) \
            + '     |       homepage: ' + str(event.homepage)



#webpage creator
def buildPage():
    btn_classes = jp.Styles.button_outline + ' m-2'
    input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"

    wp = jp.WebPage()
    
    #website header
    d = jp.Div(text='Scientific Event Predictor', a=wp, classes='w-480 text-xl m-2 p-1 bg-blue-500 text-white rounded')
    
    #input field
    input = jp.Input(a=wp, classes=input_classes, placeholder='Input series acronym here')
    
    #search button
    textView=[]
    jp.Button(text='Attempt Prediction',
        a=wp,
        source=input,
        target=textView,
        classes=btn_classes,
        click=btn_click
    )
    
    #Description of website
    textView.append(jp.Div(text='  This website is a tool to predict data of upcoming events from scientific event series', a=wp, classes='strong'))

    return wp


def initUI():
    jp.justpy(buildPage)