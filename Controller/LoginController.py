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


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['POST','GET'])
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
    

@auth_blueprint.route('/doctor', methods=['POST','GET'])
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
    
@auth_blueprint.route('/addUser', methods=['POST'])
@jwt_required()
def addUser():
    # Kiểm tra quyền admin từ token
    try:
        identity = get_jwt_identity()
        
        # Kiểm tra xem identity có phải là đối tượng hợp lệ và có trường 'role'
        if not identity or not isinstance(identity, dict) or "role" not in identity:
            return jsonify({"msg": "Token không hợp lệ"}), 400

        if identity["role"] != admin:  # Chỉ admin mới được phép thêm tài khoản
            return jsonify({"msg": "Bạn không có quyền truy cập"}), 403

        # Lấy dữ liệu từ request
        username = request.json.get('username')
        password = request.json.get('password')
        ho = request.json.get('ho')
        ten = request.json.get('ten')
        sdt = request.json.get('sdt')
        email = request.json.get('email')

        # Kiểm tra các trường cần thiết
        if not username or not password or not ho or not ten or not sdt or not email:
            return jsonify({"msg": "Cần nhập đầy đủ thông tin"}), 400

        try:
            # Thêm tài khoản mới vào cơ sở dữ liệu
            new_user = ClientAccount(
                username=username,
                password=password,
                ho=ho,
                ten=ten,
                sdt=sdt,
                email=email
            )
            session_db.add(new_user)
            session_db.commit()

            # Trả về thông báo thành công
            return jsonify({"msg": "Tài khoản đã được tạo thành công"}), 201

        except IntegrityError:
            session_db.rollback()
            return jsonify({"msg": "Tên đăng nhập đã tồn tại"}), 400
        except Exception as e:
            session_db.rollback()
            return jsonify({"msg": str(e)}), 500

    except Exception as e:
        return jsonify({"msg": str(e)}), 500


    
@auth_blueprint.route('/addDoctor', methods=['POST'])
@jwt_required()
def adddoctor():
    # Kiểm tra quyền admin từ token
    try:
        identity = get_jwt_identity()
        
        # Kiểm tra xem identity có phải là đối tượng hợp lệ và có trường 'role'
        if not identity or not isinstance(identity, dict) or "role" not in identity:
            return jsonify({"msg": "Token không hợp lệ"}), 400

        if identity["role"] != admin:  # Chỉ admin mới được phép thêm tài khoản
            return jsonify({"msg": "Bạn không có quyền truy cập"}), 403

        # Lấy dữ liệu từ request
        data = request.json
        hoc_ham = data.get('hoc_ham')
        ho = data.get('ho')
        ten = data.get('ten')
        hinh_anh = data.get('hinh_anh')
        mo_ta = data.get('mo_ta')
        ngay_bd_hanh_y = data.get('ngay_bd_hanh_y')
        password = data.get('password')
        username = data.get('username')
        # Kiểm tra các trường cần thiết
        if not hoc_ham or not ho or not ten or not ngay_bd_hanh_y or not password or not username:
            return jsonify({"msg": "Cần nhập đầy đủ thông tin"}), 400

        try:
            # Thêm tài khoản mới vào cơ sở dữ liệu
            new_doctor = BacSi(
                hoc_ham=hoc_ham,
                ho=ho,
                ten=ten,
                hinh_anh=hinh_anh,
                mo_ta=mo_ta,
                ngay_bd_hanh_y=ngay_bd_hanh_y,
                password=password,
                username=username
            )
            session_db.add(new_doctor)
            session_db.commit()

            # Trả về thông báo thành công
            return jsonify({"msg": "Tài khoản đã được tạo thành công"}), 201

        except IntegrityError:
            session_db.rollback()
            return jsonify({"msg": "Tên đăng nhập đã tồn tại"}), 400
        except Exception as e:
            session_db.rollback()
            return jsonify({"msg": str(e)}), 500

    except Exception as e:
        return jsonify({"msg": str(e)}), 500
