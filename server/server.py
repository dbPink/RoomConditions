#!flask/bin/python
from flask import Flask, jsonify
from random import random
from time import sleep
from datetime import datetime
import thread

measures = []
max_size = 10

app = Flask(__name__)

@app.route('/<version>/conditions/', defaults={'last_time': None}, methods=['GET'])
@app.route('/<version>/conditions/<last_time>', methods=['GET'])
def index(last_time, version):
	global measures
	return jsonify({'measures' : measures})

def colectData():
	global measures
	global max_size
	while True:
		try:
			value = {
		        'time': datetime.now().strftime("%a %b %d %H:%M:%S %Y"),
		        'humidity': random() * 20,
		        'temperature': random() * 100
		    }
			measures.append(value)
			if (len(measures) > max_size):
				measures.pop(0)
			sleep(5)

		except KeyboardInterrupt:
			break 


if __name__ == '__main__':
	thread.start_new_thread(colectData, ())
	app.run(debug=True)