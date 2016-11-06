from flask import Flask, render_template, request, url_for
from flask_socketio import SocketIO, emit
import random, json

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, async_mode=async_mode)

print("Start")

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/test/<userStr>')
def test(userStr):
	return render_template("test.html",userStr=userStr)

# SocketIO Test

@app.route('/socket/')
def socketPage():
	return render_template("socket.html")

@socketio.on('my_event', namespace='/socket/')
def sendMessage():
	emit('message', {'data':'my data'})

@socketio.on('connect', namespace='/socket/')
def test_connect():
	print("Connected.")
	emit('message', {'data': 'Connected to Socket'})
	print("Message sent.")

# API

@app.route('/api/update', methods=['GET','POST'])
def api_update():
	if request.method == 'POST':
		print("POST request")
		json_request = request.get_json(force=False,silent=False,cache=False)
		if json_request["type"] == "updateLocation":
			data = {}
			data["type"] = "baloonLocation"
			data["location"] = {}
			data["location"]["x"] = json_request["data"]["location"]["x"]
			data["location"]["y"] = json_request["data"]["location"]["y"]
			json_data = json.dumps(data)
			socketio.emit("baloon_update",json_data,namespace="/map")
			return "Data updated."
	else:
		print("GET request")
		print(request)


# Baloon Dashboard

thread = None

@app.route('/map')
def baloonDashboard():
	socketioURL = url_for('static',filename = 'socket.io-1.4.5.js')
	styleURL = url_for('static', filename='style.css')
	print styleURL
	print socketioURL
	return render_template("index.html",async_mode=socketio.async_mode, styleURL = styleURL, socketioURL = socketioURL)

@socketio.on('connect', namespace='/map')
def baloonUpdate():
	print("Client connected");
	emit('message', {'data':'Client connected'})
	global thread
	#if thread is None:
		#thread = socketio.start_background_task(target=background_thread)

messageType = ["baloonLocation","baloonStart","baloonBurst","baloonLanding","baloonPathUpdate"]

def background_thread():
    while True:
        socketio.sleep(5)
        i = random.randint(0,len(messageType)-1)
        print("Sending " + messageType[i])
        socketio.emit('baloon_update',{'type':messageType[i]}, namespace="/map")

if __name__ == '__main__':
	socketio.run(app)

if __name__ == "__main__":
    app.run()
