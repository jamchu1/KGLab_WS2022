from KGLab_WS2022.url_predictor import URLPredictor
from KGLab_WS2022.nlp_predictor import NLPPredictor
from KGLab_WS2022.table import Table
import json

class PredAnalyser:

    def count_predictions(self, table: Table):
        dict = {}

        url_predictor = URLPredictor()
        nlp_predictor = NLPPredictor()

        prediction_made_url = 0
        latest_event_has_homepage = 0
        prediction_made_nlp = 0
        generator_found = 0
        # how many attributes (without generator) were predicted by nlp
        amount_pred_attr = 0
        amount_pred_attr_generator = 0
        series_has_homepage = 0
        pred_made_total = 0
        total = 0

        for series in table.eventseriesList:
            pred_made_by_either_method = False

            pred_event_url = url_predictor.predict(series)
            if pred_event_url:
                pred_made_by_either_method = True
                prediction_made_url += 1
            latest_event = url_predictor.get_latest_event(series)
            if latest_event and latest_event.homepage:
                latest_event_has_homepage += 1

            pred_event_nlp = nlp_predictor.predict(series)
            if pred_event_nlp:
                pred_made_by_either_method = True
                prediction_made_nlp += 1
                attributes = [pred_event_nlp.country, pred_event_nlp.location, pred_event_nlp.ordinal, pred_event_nlp.year]
                count = sum(x is not None for x in attributes)
                amount_pred_attr += count
                if pred_event_nlp.generator is not None:
                    generator_found += 1
                    amount_pred_attr_generator += count

            if series.homepage:
                series_has_homepage += 1
            
            if pred_made_by_either_method:
                pred_made_total += 1

            #dict[series.title] = [pred_event_url.to_JSON() if pred_event_url else None, pred_event_nlp.to_JSON() if pred_event_nlp else None]

            url_res = None
            if pred_event_url:
                url_res = pred_event_url.__dict__ 
                del url_res["series"]

            nlp_res = None
            if pred_event_nlp:
                nlp_res = pred_event_nlp.__dict__ 
                del nlp_res["series"]

            pred_event_nlp.__dict__ if pred_event_nlp else None
            dict[series.title] = {
                "urlPrediction": url_res,
                "nlpPrediction": nlp_res
            }

            total += 1
            if total % 10 == 0:
                print(total)
        
        print(f'In total predictions have been made for {pred_made_total}/{total} = {pred_made_total/total} of the series')
        print(f'The URLPredictor made predictions for {prediction_made_url}/{total} = {prediction_made_url/total} of the series')
        print(f'The NLPPredictor made predictions for {prediction_made_nlp}/{total} = {prediction_made_nlp/total} of the series')
        print(f'{latest_event_has_homepage}/{total} = {latest_event_has_homepage/total} of the latest events of the series have a homepage associated with it')
        # series ohne homepage wurden vorher aussortiert
        #print(f'{series_has_homepage}/{total} = {series_has_homepage/total} of the series have a homepage associated with it')
        print(f'The mean amount of attributes predicted for a series was {amount_pred_attr}/{total} = {amount_pred_attr/total}')
        print(f'The mean amount of attributes predicted for a series with a successful nlp prediction was {amount_pred_attr}/{prediction_made_nlp} = {amount_pred_attr/prediction_made_nlp}')
        print(f'The mean amount of attributes predicted for a series with a found generator was {amount_pred_attr_generator}/{generator_found} = {amount_pred_attr/generator_found}')

        json_object = json.dumps(dict, indent=4)
        
        with open("KGLab_WS2022/analysis/predictions2.json", "w") as outfile:
            outfile.write(json_object)