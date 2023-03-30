import justpy as jp

class Globals:
    table = None
    eventPredictor = None


#function compares two strings disregarding case or special characters 
def xcompare(strin1, strin2):
    
    str1 = strin1
    str1 = str1.lower()
    str1 = str1.replace(" ", "")
    str1 = str1.replace(".", "")
    str1 = str1.replace(",", "")
    str1 = str1.replace("-", "")
    str1 = str1.replace("@", "")
    str1 = str1.replace("#", "")
    str1 = str1.replace("'", "")

    str2 = strin2
    str2 = str2.lower()
    str2 = str2.replace(" ", "")
    str2 = str2.replace(".", "")
    str2 = str2.replace(",", "")
    str2 = str2.replace("-", "")
    str2 = str2.replace("@", "")
    str2 = str2.replace("#", "")
    str2 = str2.replace("'", "")

    return str1 == str2



#button click handler
def btn_click(self, msg):
    #user input of event name acronym
    input = self.source.value
    targetSeries = None

    #searching for scientific event series matching input
    for series in Globals.table.eventseriesList:
        if xcompare(series.title, input):
            targetSeries = series
            break
        elif xcompare(series.acronym, input):
            targetSeries = series
            break

    if targetSeries is None:
        #input does not match with an event series
        self.target[0].text = 'Error: No series was found for your input: "' + input + '".'
    else:
        #input matches with an event series
        event = Globals.eventPredictor.predict(targetSeries)
        
        if event is None:
            #failure to predict next installment
            self.target[0].text = 'Failure: Could not predict next event of the series:' + series.title
        else:
            #success in predicting next installment
            self.target[0].text = 'Success! For your Input "' +  input  + '" the Prediction gathered the following metadata: ' \
            + '     | Event Title: ' + str(event.eventTitle) \
            + '     | Series Title: ' + str(series.title) \
            + '     | Ordinal: ' + str(event.ordinal) \
            + '     | Country: ' + str(event.country) \
            + '     | Location: ' + str(event.location) \
            + '     | Year: ' + str(event.year) \
            + '     | Event Homepage: ' + str(event.homepage) \
            + '     | Series Homepage: ' + str(series.homepage)



#webpage creator
def buildPage():
    btn_classes = jp.Styles.button_outline + ' m-2'
    input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"

    wp = jp.WebPage()
    
    #website header
    d = jp.Div(text='Scientific Event and Conference Predictor', a=wp, classes='w-480 text-xl m-2 p-1 bg-blue-500 text-white rounded')
    jp.I(text='Below you can check for any event series titles or acronyms and whether a prediction can be made for them:', a=wp)
    jp.Br(a=wp)
    
    #input field
    input = jp.Input(a=wp, classes=input_classes, placeholder='your input...')
    
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
    textView.append(jp.Div(text=' The results will be shown here.', a=wp, classes='strong'))

    return wp


def initUI():
    jp.justpy(buildPage)