import justpy as jp

class Globals:
    table = None
    eventPredictor = None


def btn_click(self, msg):
    input = self.source.value
    targetSeries = None

    # find series by acronym
    for series in Globals.table.eventseriesList:
        if series.acronym == input:
            targetSeries = series
            break

    if targetSeries is None:
        self.target[0].text = 'no series found for given acronym'
    else:
        # predict this series
        
        event = Globals.eventPredictor.predict(targetSeries)
        if event is None:
            self.target[0].text = 'could not predict'
        else:
            self.target[0].text = str(event)


def buildPage():
    btn_classes = jp.Styles.button_outline + ' m-2'
    input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"

    wp = jp.WebPage()
    input = jp.Input(a=wp, classes=input_classes, placeholder='input series acronym here')
    textView=[]
    jp.Button(text='Button',
        a=wp,
        source=input,
        target=textView,
        classes=btn_classes,
        click=btn_click
    )
    textView.append(jp.Div(text='', a=wp, classes='italic'))

    return wp

def initUI():
    jp.justpy(buildPage)