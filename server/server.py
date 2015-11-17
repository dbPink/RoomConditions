#!flask/bin/python
from flask import Flask, jsonify, send_from_directory
from random import random
from time import sleep
from datetime import datetime
import thread
import threading

measures = []
max_size = 40

lock = threading.Lock()
app = Flask(__name__)

@app.route('/view/<path:path>')
def send_js(path):
    return send_from_directory('view', path)

@app.route('/<version>/conditions/', defaults={'last_time': None}, methods=['GET'])
@app.route('/<version>/conditions/<last_time>', methods=['GET'])
def index(last_time, version):
	global measures
	global lock
	with lock:
		if (last_time):
			for i in range(len(measures)-1, -1, -1):
				if (measures[i].get('time') == last_time):
					return jsonify({'measures' : measures[i:]})
		return jsonify({'measures' : measures})

def colectData():
	global lock
	global measures
	global max_size
	while True:
		try:
			value = {
		        'time': datetime.now().strftime("%H:%M:%S"),
		        'humidity': random() * 20,
		        'temperature': random() * 100
			}
			with lock:
				measures.append(value)
				if (len(measures) > max_size):
					measures.pop(0)
			sleep(5)

		except KeyboardInterrupt:
			break 


if __name__ == '__main__':
	thread.start_new_thread(colectData, ())
	app.run(debug=True)