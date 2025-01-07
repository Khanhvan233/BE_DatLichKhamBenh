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
import base64
from Variable import *
from Service.FirebaseHandler import FirebaseHandler

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


acc_blueprint = Blueprint('acc', __name__)


@acc_blueprint.route('/myINFO/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    try:
        # Kiểm tra quyền admin từ token
        identity = get_jwt_identity()

        if not identity or not isinstance(identity, dict) or "role" not in identity:
            return jsonify({"msg": "Token không hợp lệ"}), 400

        if identity["role"] != client:  # Chỉ admin mới có quyền xem thông tin người dùng
            return jsonify({"msg": "Bạn không có quyền thực hiện thao tác này"}), 403

        # Tìm người dùng theo ID
        user = session_db.query(ClientAccount).filter_by(id=user_id).one_or_none()

        if not user:
            return jsonify({"msg": "Người dùng không tồn tại"}), 404

        # Trả về thông tin người dùng
        return jsonify({
            "id": user.id,
            "username": user.username,
            "ho": user.ho,
            "ten": user.ten,
            "sdt": user.sdt,
            "email": user.email
        }), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500
    


@acc_blueprint.route('/editMyInfo/<int:user_id>', methods=['PUT'])
@jwt_required()
def edit_user(user_id):
    try:
        # Kiểm tra quyền admin từ token
        identity = get_jwt_identity()
        if not identity or "role" not in identity or identity["role"] != client:
            return jsonify({"msg": "Bạn không có quyền thực hiện thao tác này"}), 403

        # Kiểm tra xem user có tồn tại không
        user = session_db.query(ClientAccount).filter_by(id=user_id).one_or_none()
        if not user:
            return jsonify({"msg": "User không tồn tại"}), 404

        # Lấy dữ liệu từ request
        data = request.json
        user.username = data.get('username', user.username)
        user.password = data.get('password', user.password)
        user.ho = data.get('ho', user.ho)
        user.ten = data.get('ten', user.ten)
        user.sdt = data.get('sdt', user.sdt)
        user.email = data.get('email', user.email)

        # Lưu thay đổi vào database
        session_db.commit()
        return jsonify({"msg": "Chỉnh sửa user thành công"}), 200

    except IntegrityError:
        session_db.rollback()
        return jsonify({"msg": "Tên đăng nhập đã tồn tại"}), 400
    except Exception as e:
        session_db.rollback()
        return jsonify({"msg": str(e)}), 500

