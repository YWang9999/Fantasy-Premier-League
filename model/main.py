"""
    File to be exectuted by Cloud Function.
"""
from flask import Flask, request, jsonify
from optimised_selector import optimumTeam, best_transfer

def main(request):
    """
        Entry point - Do not change name of this function.
        Should call the eventual squad_selector/optimiser file.
    """
    data = request.get_json(force=True)
    print("Data sent is ", data)

    data_existing_team = data['existing_team']
    data_free_transfers = data['free_transfers']
    data_budget = data['budget']


    results = optimumTeam(
        budget = data_budget,
        number_of_players=None,
        full_squad = True
    )
    results_json = results.to_json()
    print(results_json)   
    # return jsonify(data['existing_team'] , data['free_transfers'])
    return results_json