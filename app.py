from flask import Flask, jsonify, render_template, redirect
from flask_pymongo import PyMongo

app=Flask(__name__)

##front end routes
@app.route("/main")
def home():
    return render_template("templates/index.html")

##service routes
if __name__="__main__":
    app.run(debug=True)

