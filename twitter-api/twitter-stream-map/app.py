from flask import Flask
from flask import render_template, jsonify
from info import data
from stream_code import main
import threading


class Thread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        main()


# create application
app = Flask(__name__)
prev_list = list()


@app.route('/')
def index():
    t = Thread()
    t.start()
    return render_template('index.html')


@app.route('/data')
def stream_data():
    new_data = []
    for item in data:
        temp_data = {}
        temp_data['geometry'] = {}
        temp_data['properties'] = {}
        temp_data['type'] = 'Feature'
        temp_data['geometry']['type'] = 'Point'
        temp_data['geometry']['coordinates'] = item['coordinates']['coordinates']
        temp_data['properties']['name'] = item['text']
        new_data.append(temp_data)
    global prev_list
    if prev_list == []:
        prev_list = new_data[:]
        print(jsonify(new_data))
        return jsonify(new_data)
    else:
        d = []
        for item in new_data:
            if item not in prev_list:
                d.append(item)
        prev_list = new_data[:]
        print(jsonify(d))
        return jsonify(d)

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host="0.0.0.0")
