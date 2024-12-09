import config
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
from Controller.LoginController import login_blueprint
from Controller.AdminController import auth_blueprint
from Controller.CenterController import center_blueprint
from Controller.DoctorController import doctor_blueprint


app = Flask(__name__)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
CORS(app)

app.register_blueprint(auth_blueprint)
app.register_blueprint(doctor_blueprint)
app.register_blueprint(center_blueprint)
app.register_blueprint(login_blueprint)


secret_key = os.environ.get('SECRET_KEY')

app.config["JWT_SECRET_KEY"] = secret_key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)


jwt = JWTManager(app)


@app.route('/')
def index():
    response = jsonify({"msg": "Test successfully"})
    return response, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=7777)  