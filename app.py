#import dependencies
from flask import Flask, jsonify, render_template, redirect
from flask_pymongo import PyMongo
#from flask_sqlalchemy import SQLAlchemy

##demo dictionary

my_dict={
    1: "catherine", 
    2: "myfanwy", 
    3: "rubal", 
    4: "manisha", 
    5: "sharanvika"

}

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "bigquery://bikeshare-303620/TripsDataset"
db = SQLAlchemy(app)

##front end routes
@app.route("/")
def home():
    return render_template("index.html")

##service routes
@app.route("/api/prices")
def api_prices():
    return jsonify(my_dict)

#run app
#if __name__=="__main__":
app.run(debug=True)

