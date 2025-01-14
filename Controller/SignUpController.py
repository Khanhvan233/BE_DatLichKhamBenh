
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

signup_blueprint = Blueprint('signup', __name__)


@signup_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    ho = data.get('ho')     # Họ
    ten = data.get('ten')    # Tên
    email = data.get('email')
    sdt = data.get('sdt')   # Số điện thoại
    # cccd = data.get('cccd')
    # Validate input fields
    if not username or not password or not ho or not ten or not sdt:
        return jsonify({"msg": "Cần nhập đầy đủ username, password, họ, tên và số điện thoại"}), 400

    try:
        session_db = db_manager.get_session()
        # Kiểm tra username đã tồn tại trong database
        existing_user = session_db.query(ClientAccount).filter_by(username=username).one_or_none()

        if existing_user:
            return jsonify({"msg": "Username đã tồn tại"}), 409

        # Gán dữ liệu mới vào database
        new_user = ClientAccount(
            username=username,
            password=password,
            ho=ho,
            ten=ten,
            email=email,
            sdt=sdt,
            # cccd=cccd
        )
        session_db.add(new_user)
        session_db.commit()

        return jsonify({"msg": "Đăng ký thành công"}), 201

    except IntegrityError:
        session_db.rollback()
        return jsonify({"msg": "Conflict - Integrity Error"}), 409

    except Exception as e:
        session_db.rollback()
        return jsonify({"msg": str(e)}), 500
