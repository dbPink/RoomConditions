from flask import Flask, jsonify, send_from_directory
from random import random
from time import sleep
from datetime import datetime
import thread
import threading
from  reader import read_temp

measures = []
max_size = 120

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
                                    if (len(measures) <= i + 1):
                                        return jsonify({'measures' : []})
                                    else:
					return jsonify({'measures' : measures[i + 1:]})
		return jsonify({'measures' : measures})

def colectData():
	global lock
	global measures
	global max_size
	while True:
		try:
			value = {
		        'time': datetime.now().strftime("%H:%M:%S"),
		        'temperature': read_temp()
			}
			with lock:
				measures.append(value)
				if (len(measures) > max_size):
					measures.pop(0)
			sleep(300)

		except KeyboardInterrupt:
			break 


if __name__ == '__main__':
	thread.start_new_thread(colectData, ())
	app.run(host='0.0.0.0', port=80, debug=True)
