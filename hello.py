import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import send_from_directory

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['json'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    print filename
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def show():
    return render_template('index.html')

@app.route('/showjson')
def test2():
    return render_template('showjson.html')

@app.route('/hehehe')
def test():
    return render_template('hehehe.html')

@app.route('/test')
def test_iframe():
    return render_template('test_iframe.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'tree.json'))
            return redirect(url_for('show'))
        else:
            return "file not supported!"


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
