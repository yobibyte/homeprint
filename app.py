from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from werkzeug.utils import secure_filename

import os

# flask flash requires it set up
SECRET_KEY = os.getenv('SECRET_KEY', 'debug') 

FILES_FOLDER = './files'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

if not os.path.exists(FILES_FOLDER):
  os.makedirs(FILES_FOLDER) 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = FILES_FOLDER 
app.secret_key = SECRET_KEY

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def print_file():
  # copied from flask tutorial:
  # https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return redirect(url_for('print_file', name=filename))
  return '''
  <!doctype html>
  <title>Upload new File</title>
  <h1>Upload new File</h1>
  <form method=post enctype=multipart/form-data>
    <input type=file name=file>
    <input type=submit value=Upload>
  </form>
  '''

