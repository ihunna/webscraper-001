from flask import Flask, send_file, abort
import os
from os import listdir
from os.path import isfile
from datetime import datetime


app = Flask(__name__)

@app.route(f'/get_image/<image_folder>/<image>')
def get_image(image_folder,image): 
    if isfile(os.path.abspath(f'./image_files/{image_folder}/{image}')):
        filename  = os.path.abspath(f'./image_files/{image_folder}/{image}')
        return send_file(filename, mimetype='image/jpeg')
    else:
        return abort(404)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)