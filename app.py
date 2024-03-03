from flask import Flask, render_template, request, redirect, url_for
from markupsafe import Markup
from random_forest_test import acc

import numpy as np
import os
import pickle
import json
import plotly
import pandas as pd
import numpy as np

app = Flask(__name__)

# CSS fix by adding modified timestamp
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

# load model
model_RF = pickle.load(open('model_RF.pkl','rb'))



@app.route('/')
@app.route('/first')
def first():
    return render_template('first.html')
@app.route('/login')
def login():
    return render_template('login.html')
def home():
	return render_template('home.html')
@app.route('/upload')
def upload():
    return render_template('upload.html')  
@app.route('/preview',methods=["POST"])
def preview():
    if request.method == 'POST':
        dataset = request.files['datasetfile']
        df = pd.read_csv(dataset,encoding = 'unicode_escape')
        df.set_index('Id', inplace=True)
        return render_template("preview.html",df_view = df) 


@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/detect")
def detect():
    return render_template('detect.html')

@app.route("/result", methods=['POST','GET'])
def result():
    int_features = [int(x) for x in  request.form.values()]
    final = [np.array(int_features)]
    predict = model_RF.prediction(final)
    print(int_features)
    print(final)
    print(predict)
    
    if predict == 1:
        return render_template('result.html', pred='SAFE')
    return render_template('result.html', pred='Phishing')

@app.route('/chart')
def chart():
    return render_template('chart.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")



if __name__ == "__main__":
    app.run(debug=True)