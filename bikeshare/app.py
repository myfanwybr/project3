#import dependencies
from flask import Flask, jsonify, render_template, redirect
from config import gcp_project, bigquery_uri
from google.oauth2 import service_account
import pandas as pd
import pandas_gbq
import json


##demo dictionary

my_dict={
    1: "catherine", 
    2: "myfanwy", 
    3: "rubal", 
    4: "manisha", 
    5: "sharanvika"

}

app=Flask(__name__)

credentials = service_account.Credentials.from_service_account_file('bikeshare-303620-f28d36859136.json')

##front end routes
@app.route("/")
def main():
    print(f'project is {gcp_project}')
    print(f'project is {bigquery_uri}')
    return render_template("index.html")

##service routes
@app.route("/api/prices")
def api_prices():

    sql_prices = '''select * from `bikeshare-303620.TripsDataset.Pricing` '''
    pricing_df = pd.read_gbq(sql_prices, project_id=gcp_project, credentials=credentials, dialect='standard')
    print(pricing_df)

    json_obj = pricing_df.to_json()

    return json_obj

#run app
if __name__=="__main__":
    app.run(debug=True)

