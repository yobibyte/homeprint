from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from werkzeug.utils import secure_filename

import os
import subprocess

# flask flash requires it set up
SECRET_KEY = os.getenv('SECRET_KEY', 'debug') 

FILES_FOLDER = './files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png'}

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
      file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
      # print file now
      pages_range = "-"
      page_from = request.form['page_from']
      if page_from.isnumeric():
        pages_range = page_from + pages_range
      page_to= request.form['page_to']
      if page_to.isnumeric():
        pages_range = pages_range + page_to
      print(pages_range)
      print_cmd = f"lp -n1 -o media=a4 -o fit-to-page -o sides=one-sided {file_path}"
      if len(pages_range) > 1:
        print_cmd+=f" -P {pages_range}"
      n_copies = request.form['copies']
      if not n_copies.isnumeric():
        n_copies = "1"
      print_cmd += f" -n {n_copies}"

      pps= request.form['pps']
      if not pps.isnumeric():
        pps = "1"
      print_cmd += f" -o number-up={pps}"
      
      print(print_cmd)
      process = subprocess.Popen(print_cmd.split(), stdout=subprocess.PIPE)
      output, error = process.communicate()
      print(output)

      return redirect(url_for('print_file', name=filename))
  return '''
  <!doctype html>
  <title>Upload new File</title>
  <h1>Hello! Upload a file to print...</h1>
  <form method=post enctype=multipart/form-data>
    <input type=file name=file>
    <p>Page from (including): <input name="page_from"></p>
    <p>Page to (including): <input name="page_to"></p>
    <p>Copies: <input name="copies" value="1"></p>
    <p>Pages per sheet (1,2,4,6,9,16): <input name="pps" value="1"></p>
    <input type=submit value=PRINT>
  </form>
  '''

