from flask import Blueprint
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
from werkzeug.security import check_password_hash
from Utils.MyConnectPro import MyConnectPro
from Service.Models import *

import os


user = os.environ.get('USER_NAME')
password_db = os.environ.get('PASSWORD')
database = os.environ.get('DATABASE')
host = os.environ.get('HOST')
port = os.environ.get('PORT')
secret_key=os.environ.get('SECRET_KEY')



db_manager = MyConnectPro(user= user,password=password_db,database= database,host= host,port=port)
db_manager.connect()
session_db = db_manager.get_session()


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['POST'])
def login():
    # Lấy username và password từ request
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        response = jsonify({"msg": "Cần nhập tên đăng nhập và mật khẩu"})
        return response, 400

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

        # Tạo access token và refresh token
        access_token = create_access_token(identity=client.id)
        refresh_token = create_refresh_token(identity=client.id)

        # Trả về các token trong response
        response = jsonify({
            "msg": "Đăng nhập thành công",
        })
        return response, 200

    except NoResultFound:
        response = jsonify({"msg": "Người dùng không tồn tại"})
        return response, 404
    except Exception as e:
        # Xử lý các lỗi khác
        response = jsonify({"msg": str(e)})
        return response, 500
    
