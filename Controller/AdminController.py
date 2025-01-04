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


auth_blueprint = Blueprint('auth', __name__)

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
        mo_ta = data.get('mo_ta')
        ngay_bd_hanh_y = data.get('ngay_bd_hanh_y')
        password = data.get('password')
        username = data.get('username')
        image_base64 = data.get('hinh_anh')
        prefix, base64_data = image_base64.split(',', 1)
        
        image_data = base64.b64decode(base64_data)
        path = f"doctors/{username}_profile.png"
        # Cập nhật hình ảnh lên Firebase Storage
        url = FirebaseHandler().updateImagePublic(path, image_data, "image/png")

        # Kiểm tra các trường cần thiết
        if not hoc_ham or not ho or not ten or not ngay_bd_hanh_y or not password or not username:
            return jsonify({"msg": "Cần nhập đầy đủ thông tin"}), 400

        try:
            # Thêm tài khoản mới vào cơ sở dữ liệu
            new_doctor = BacSi(
                hoc_ham=hoc_ham,
                ho=ho,
                ten=ten,
                hinh_anh=url,
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
    

@auth_blueprint.route('/getUser/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    try:
        # Kiểm tra quyền admin từ token
        identity = get_jwt_identity()

        if not identity or not isinstance(identity, dict) or "role" not in identity:
            return jsonify({"msg": "Token không hợp lệ"}), 400

        if identity["role"] != admin:  # Chỉ admin mới có quyền xem thông tin người dùng
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


@auth_blueprint.route('/getAllUsers', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        # Kiểm tra quyền admin từ token
        identity = get_jwt_identity()

        if not identity or not isinstance(identity, dict) or "role" not in identity:
            return jsonify({"msg": "Token không hợp lệ"}), 400

        if identity["role"] != admin:  # Chỉ admin mới có quyền xem danh sách người dùng
            return jsonify({"msg": "Bạn không có quyền thực hiện thao tác này"}), 403

        # Lấy danh sách tất cả người dùng
        users = session_db.query(ClientAccount).all()
        user_list = [{
            "id": user.id,
            "username": user.username,
            "ho": user.ho,
            "ten": user.ten,
            "sdt": user.sdt,
            "email": user.email
        } for user in users]

        return jsonify(user_list), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@auth_blueprint.route('/deleteUser/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        # Kiểm tra quyền admin từ token
        identity = get_jwt_identity()
        if not identity or "role" not in identity or identity["role"] != admin:
            return jsonify({"msg": "Bạn không có quyền thực hiện thao tác này"}), 403

        # Kiểm tra xem user có tồn tại không
        user = session_db.query(ClientAccount).filter_by(id=user_id).one_or_none()
        if not user:
            return jsonify({"msg": "User không tồn tại"}), 404

        # Xóa user
        session_db.delete(user)
        session_db.commit()

        return jsonify({"msg": "Xóa user thành công"}), 200
    except Exception as e:
        session_db.rollback()
        return jsonify({"msg": str(e)}), 500

@auth_blueprint.route('/deleteDoctor/<int:doctor_id>', methods=['DELETE'])
@jwt_required()
def delete_doctor(doctor_id):
    try:
        # Kiểm tra quyền admin từ token
        identity = get_jwt_identity()
        if not identity or "role" not in identity or identity["role"] != admin:
            return jsonify({"msg": "Bạn không có quyền thực hiện thao tác này"}), 403

        # Kiểm tra xem doctor có tồn tại không
        doctor = session_db.query(BacSi).filter_by(id=doctor_id).one_or_none()
        if not doctor:
            return jsonify({"msg": "Doctor không tồn tại"}), 404

        # Xóa doctor
        session_db.delete(doctor)
        session_db.commit()

        return jsonify({"msg": "Xóa doctor thành công"}), 200
    except Exception as e:
        session_db.rollback()
        return jsonify({"msg": "Không thể xóa bác sĩ do vẫn còn lịch làm việc"}), 500


@auth_blueprint.route('/editUser/<int:user_id>', methods=['PUT'])
@jwt_required()
def edit_user(user_id):
    try:
        # Kiểm tra quyền admin từ token
        identity = get_jwt_identity()
        if not identity or "role" not in identity or identity["role"] != admin:
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


@auth_blueprint.route('/editDoctor/<int:doctor_id>', methods=['PUT'])
@jwt_required()
def edit_doctor(doctor_id):
    try:
        # Kiểm tra quyền admin từ token
        identity = get_jwt_identity()
        if not identity or "role" not in identity or identity["role"] != admin:
            return jsonify({"msg": "Bạn không có quyền thực hiện thao tác này"}), 403

        # Kiểm tra xem doctor có tồn tại không
        doctor = session_db.query(BacSi).filter_by(id=doctor_id).one_or_none()
        if not doctor:
            return jsonify({"msg": "Doctor không tồn tại"}), 404

        # Lấy dữ liệu từ request
        data = request.json
        doctor.hoc_ham = data.get('hoc_ham', doctor.hoc_ham)
        doctor.ho = data.get('ho', doctor.ho)
        doctor.ten = data.get('ten', doctor.ten)
        doctor.hinh_anh = data.get('hinh_anh', doctor.hinh_anh)
        doctor.mo_ta = data.get('mo_ta', doctor.mo_ta)
        doctor.ngay_bd_hanh_y = data.get('ngay_bd_hanh_y', doctor.ngay_bd_hanh_y)
        doctor.password = data.get('password', doctor.password)
        doctor.username = data.get('username', doctor.username)

        # Lưu thay đổi vào database
        session_db.commit()
        return jsonify({"msg": "Chỉnh sửa doctor thành công"}), 200

    except IntegrityError:
        session_db.rollback()
        return jsonify({"msg": "Tên đăng nhập đã tồn tại"}), 400
    except Exception as e:
        session_db.rollback()
        return jsonify({"msg": str(e)}), 500
