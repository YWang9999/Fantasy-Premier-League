from main import main as local_main
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def add():
    # data = request.get_json(force=True)
    
    # return jsonify({'sum': data['a'] + data['b']})
    return local_main(request)


if __name__ == '__main__':
    app.run(debug=True)


