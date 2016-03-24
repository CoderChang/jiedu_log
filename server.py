import os
import json
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import make_response
from flask import jsonify

LOGS_FOLDER = 'logs'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['json'])

app = Flask(__name__)

def allowed_file(filename):
    #print filename
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_all_logjson():
    result = {}
    for data_folder in os.listdir("logs/"):
        data_path = os.path.join(LOGS_FOLDER, data_folder)
        if not os.path.isdir(data_path):
            continue
        result[data_folder] = {}
        for file_or_dir in os.listdir(data_path):
            tmp_path = os.path.join(data_path, file_or_dir)
            if os.path.isfile(tmp_path) and tmp_path.endswith(".json"):
                domain_name = file_or_dir[0:-5]
                result[data_folder][domain_name] = tmp_path
    return result

@app.route('/')
def show():
    return render_template('index.html')

@app.route('/showjson')
def showjson():
    return render_template('showjson.html')

@app.route('/hehehe')
def hehehe():
    return render_template('hehehe.html')

@app.route('/test')
def test():
    result = get_all_logjson()
    resultjson = json.dumps(obj = result, ensure_ascii = False)
    return render_template('test_iframe.html', resultjson = resultjson)

@app.route('/showlog')
def showlog():
    return render_template('showlog.html')

@app.route('/getlogjson', methods=['POST'])
def getlogjson():
    logfile = request.form['log_file']
    catalog_name = request.form['catalog_name']
    logpath = os.path.join(LOGS_FOLDER, catalog_name, logfile)
    with open(logpath) as fff:
        logjson = json.load(fff)
        logjson = json.dumps(obj = logjson, ensure_ascii = False)
        return logjson
    return "open file failed!"


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            f.save(os.path.join(LOGS_FOLDER, UPLOAD_FOLDER, 'tree.json'))
            return make_response(jsonify({'catalog_name': UPLOAD_FOLDER, 'domain_name': 'tree'}))
        else:
            return "file not supported!"

@app.route('/gettree', methods=['GET'])
def gettree():
    if request.method == 'GET':
        domain_name = request.args.get('domain_name', '')
        catalog_name = request.args.get('catalog_name', '')
        if not domain_name.endswith(".json"):
            domain_name = domain_name + ".json"
        if os.path.exists(os.path.join(LOGS_FOLDER, catalog_name, domain_name)):
            return send_from_directory(os.path.join(LOGS_FOLDER, catalog_name), domain_name)
        else:
            return make_response("failed")
    else:
        return make_response("failed")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
