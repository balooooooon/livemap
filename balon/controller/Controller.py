# http://stackoverflow.com/questions/15231359/split-python-flask-app-into-multiple-files

# Controller for Web, FB, API

# import BalloonService

from balon import app

# BalloonService.app = app

def getBalloonLocation():

	location = None

	if app.config['NO_DB'] :
		lat = 48.789562
		lng = 19.773012
		timestamp = 1477866660

		location = {
			'type': "current",
			'point': {
				'time': timestamp,
				'lat': lat,
				'lng': lng
			}
		}

	return location

def getBalloonStart():

	location = None

	if app.config['NO_DB'] :
		timestamp = 1477866660

		location = {
			'type': "start",
			'point': {
				'time': timestamp,
				'lat': 48.649259,
				'lng': 19.358272
			}
		}

	return location

def getBalloonBurst():

	location = None

	if app.config['NO_DB']:
		timestamp = 1477866660

		location = {
			'type': "burst",
			'point': {
				'time': timestamp,
				'lat': 48.687088,
				'lng': 19.667122
			}
		}

	return location

def getBalloonPath():

	path = None

	if app.config['NO_DB']:
		timestamp = 1477866660

		path = {}
		path['type'] = 'path'
		path['data'] = {
			'points': [
			{	'time': timestamp,
				'lat': 48.649259,
				'lng': 19.358272
			},
			{	'time': timestamp,
				"lat": 48.755356,
				"lng": 19.581007
			},
			{	'time': timestamp,
				"lat": 48.687088,
				"lng": 19.667122
			},
			{	'time': timestamp,
				"lat": 48.789562,
				"lng": 19.773012
			}
			]
		}

	return path
