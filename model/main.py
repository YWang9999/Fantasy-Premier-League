"""
    File to be exectuted by Cloud Function.
"""
from flask import Flask, request, jsonify

def main(request):
    """
        Entry point - Do not change name of this function.
        Should call the eventual squad_selector/optimiser file.
    """
    data = request.get_json(force=True)
    print("Data sent is ", data)
   
    return jsonify(data['existing_team'] , data['free_transfers'])