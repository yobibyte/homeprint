from flask import Flask
import os

FILES_FOLDER = './files'

if not os.path.exists(FILES_FOLDER):
  os.makedirs(FILES_FOLDER) 

app = Flask(__name__)

@app.route("/")
def hello_world():
  return "<p>Hello, World!</p>"
