"""
    Make API call from local machine.
"""
from main import main as local_main
import requests
import flask
TRIGGER_URL = 'https://europe-west2-lbghack2021team14.cloudfunctions.net/fpl-predictor'

from flask import jsonify

def make_local_request(payload):
    """
        Call local function. Testing purposes.
    """
    print("Sending request to Local")    
    r = requests.post('http://127.0.0.1:5000/', json=payload)
    print(r.text)
    
    return

def make_gcp_request(payload):
    """
        Call Cloud Function API
    """
    print("Sending request to GCP")
    r = requests.post(TRIGGER_URL,  json=payload)
    print(r.text)
   
    return

def main(local):

    # payload = {"a":10, "b":2}
    payload = {'existing_team':['Auba', 'Laca'], 'free_transfers':2}




    if local:
        make_local_request()
    else:
        make_gcp_request()


if __name__ == '__main__':
    main(local = True)