import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/Users/prabeshikakoirala/Documents/'
UPLOADS_DEFAULT_URL = 'https://patw1h5276.execute-api.eu-west-1.amazonaws.com/beta/upload'
ALLOWED_EXTENSIONS = {'txt', 'csv', 'doc', 'pdf', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOADS_DEFAULT_URL'] = UPLOADS_DEFAULT_URL

# Limiting the file size to 1 MB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/index', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',filename=filename))
    return '''
    <!doctype html>
    <title>File Uploader</title>
    <h1>Select to upload a new file</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)