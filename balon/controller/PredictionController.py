from balon import app, LOG
import requests
import ast
import datetime

PREDICTION_URL = "http://predict.habhub.org/ajax.php?action=submitForm"
PREDICTION_URL_CSV = "http://predict.habhub.org/ajax.php?action=getCSV"

def getBalloonLanding(start):
    print start
    payload = {'launchsite':'Other', 
        'lat':start['point']['lat'], 
        'lon':start['point']['lng'],
        'initial_alt':157, #TODO
        'hour':start['point']['time'].hour, 
        'min':start['point']['time'].minute+1, 
        'second':start['point']['time'].second, 
        #'day':start['point']['time'].day, 
        'day':1, 
        #'month':start['point']['time'].month, 
        'month':4, 
        #'year':start['point']['time'].year,
        'year':2017,
        'ascent':2.33, #TODO
        'burst':33000, #TODO
        'drag':9.8, #TODO
        'submit':'Run+Prediction'}
    r = requests.post(PREDICTION_URL,data=payload)
    if r.status_code == requests.codes.ok:
        responseData = ast.literal_eval(r.text)
        if responseData['valid'] == "true":
            payload_csv = {'uuid':responseData['uuid']}
            r_csv = requests.post(PREDICTION_URL_CSV,params=payload_csv)
            if r_csv.status_code == requests.codes.ok:
                responseData_csv = ast.literal_eval(r_csv.text)
                if len(responseData_csv) > 1:
                    responseData_list = [x.split(",") for x in responseData_csv]
                    if responseData_list is not None:
                        predictedLandingValues = responseData_list[-2]
                        timestamp_last = datetime.datetime.fromtimestamp(int(predictedLandingValues[0]))
                        positionLast = {
                            'type': 'landing',
                            'point': {
                                'time': timestamp_last,
                                'lat': float(predictedLandingValues[1]),
                                'lng': float(predictedLandingValues[2])
                            }
                        }
                        pathPredicted = {
                            'type': "pathPredicted",
                            'data': {
                                'points': []
                                } 
                            }
                        for x in responseData_list:
                            if len(x) > 1:
                                jsonPoint = {
                                    'lat': float(x[1]),
                                    'lng': float(x[2]),
                                    'time': datetime.datetime.fromtimestamp(int(x[0]))
                                }
                                pathPredicted['data']['points'].append(jsonPoint)
                    return positionLast,pathPredicted
                else:
                    LOG.debug("Prediction server returned empty list")
    return None, None
