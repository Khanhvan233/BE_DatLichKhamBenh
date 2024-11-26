import config

from flask import Flask
from flask import jsonify
from flask_cors import CORS

import os



app = Flask(__name__)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
CORS(app)


@app.route('/')
def index():
    response = jsonify({"msg": "Test successfully"})
    return response, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=7777)