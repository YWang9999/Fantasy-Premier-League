"""
    File to be exectuted by Cloud Function.
"""
from flask import Flask, request, jsonify

def main(request):
    """
        Entry point - Do not change name of this function.
    """
    data = request.get_json(force=True)
    
    return jsonify({'sum': data['a'] + data['b']})