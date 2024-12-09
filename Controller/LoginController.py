from flask import Blueprint, json
from flask import request
from flask import jsonify
from flask import abort, redirect
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_jwt_extended import jwt_required
from Utils.EntityHandler import EntityHandler
from Utils.MyConnectPro import MyConnectPro
from flask_jwt_extended import get_jwt_identity
from Service.Models import *
from flask_jwt_extended import jwt_required
import os
from Variable import *

user = os.environ.get('USER_NAME')
password_db = os.environ.get('PASSWORD')
database = os.environ.get('DATABASE')
host = os.environ.get('HOST')
port = os.environ.get('PORT')
secret_key=os.environ.get('SECRET_KEY')
admin=os.environ.get('ADMIN')


db_manager = MyConnectPro(user= user,password=password_db,database= database,host= host,port=port)
db_manager.connect()
session_db = db_manager.get_session()


login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/login', methods=['POST','GET'])
def login():
    # Lấy username và password từ request
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        response = jsonify({"msg": "Cần nhập tên đăng nhập và mật khẩu"})
        return response, 404

    try:
        # Kiểm tra xem người dùng có tồn tại trong cơ sở dữ liệu không
        client = session_db.query(ClientAccount).filter_by(username=username).one_or_none()

        # Nếu người dùng không tồn tại
        if not client:
            response = jsonify({"msg": "Tên đăng nhập hoặc mật khẩu không đúng"})
            return response, 404

        # Kiểm tra mật khẩu (so sánh trực tiếp với mật khẩu lưu trữ trong cơ sở dữ liệu)
        if client.password != password:
            response = jsonify({"msg": "Tên đăng nhập hoặc mật khẩu không đúng"})
            return response, 404
        
        if client.password == password and client.id == int(admin):
            idenInfo = {
                "role": admin,  # Gán role là admin nếu là tài khoản admin
                "userID": client.id, 
                "username": client.ten
            }
        else:
            # Nếu không phải admin
            idenInfo = {
                "role": user,  # Gán role là user cho các tài khoản khác
                "userID": client.id,
                "username": client.ten
            }
        idenInfoStr = json.dumps(idenInfo, ensure_ascii=False)
        accessToken = create_access_token(identity=idenInfoStr, fresh=True)
        print(f"Generated identity: {idenInfo}")
        print(f"Generated token: {accessToken}")
        # Trả về các token trong response
        response = jsonify({
            "msg": "Đăng nhập thành công",
            "token": accessToken
        })
        return response, 200

    except NoResultFound:
        response = jsonify({"msg": "Người dùng không tồn tại"})
        return response, 404
    except Exception as e:
        # Xử lý các lỗi khác
        response = jsonify({"msg": str(e)})
        return response, 500
    

@login_blueprint.route('/doctor', methods=['POST','GET'])
def loginDoctor():
    # Lấy username và password từ request
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        response = jsonify({"msg": "Cần nhập tên đăng nhập và mật khẩu"})
        return response, 400

    
    try:
        # Kiểm tra xem người dùng có tồn tại trong cơ sở dữ liệu không
        client = session_db.query(BacSi).filter_by(username=username).one_or_none()

        # Nếu người dùng không tồn tại
        if not client:
            response = jsonify({"msg": "Tên đăng nhập hoặc mật khẩu không đúng"})
            return response, 404

        # Kiểm tra mật khẩu (so sánh trực tiếp với mật khẩu lưu trữ trong cơ sở dữ liệu)
        if client.password != password:
            response = jsonify({"msg": "Tên đăng nhập hoặc mật khẩu không đúng"})
            return response, 404
        
        if client.password == password:
            idenInfo = {
                "role": doctor,  # Gán role là admin nếu là tài khoản admin
                "userID": client.id,
                "username": client.ten
            }

        accessToken = create_access_token(identity=idenInfo, fresh=True)

        # Trả về các token trong response
        response = jsonify({
            "msg": "Đăng nhập thành công",  
            "token": accessToken
        })
        return response, 200

    except NoResultFound:
        response = jsonify({"msg": "Người dùng không tồn tại"})
        return response, 404
    except Exception as e:
        # Xử lý các lỗi khác
        response = jsonify({"msg": str(e)})
        return response, 500
