
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


doctor_blueprint = Blueprint('doctor', __name__)

@doctor_blueprint.route('/getDoctor/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    try:
        # Tìm bác sĩ theo ID
        doctor = session_db.query(BacSi).filter_by(id=doctor_id).one_or_none()

        if not doctor:
            return jsonify({"msg": "Bác sĩ không tồn tại"}), 404

        # Trả về thông tin bác sĩ
        return jsonify({
            "id": doctor.id,
            "hoc_ham": doctor.hoc_ham,
            "ho": doctor.ho,
            "ten": doctor.ten,
            "hinh_anh": doctor.hinh_anh,
            "mo_ta": doctor.mo_ta,
            "ngay_bd_hanh_y": str(doctor.ngay_bd_hanh_y),
            "username": doctor.username
        }), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@doctor_blueprint.route('/getAllDoctors', methods=['GET'])
def get_all_doctors():
    try:
        
        # Lấy danh sách tất cả bác sĩ
        doctors = session_db.query(BacSi).all()
        doctor_list = [{
            "id": doctor.id,
            "hoc_ham": doctor.hoc_ham,
            "ho": doctor.ho,
            "ten": doctor.ten,
            "hinh_anh": doctor.hinh_anh,
            "mo_ta": doctor.mo_ta,
            "ngay_bd_hanh_y": str(doctor.ngay_bd_hanh_y),
            "username": doctor.username
        } for doctor in doctors]

        return jsonify(doctor_list), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500
@doctor_blueprint.route('/getDoctorsByKhoa', methods=['GET'])
def get_doctors_by_khoa():
    try:
        # Nhận tên khoa từ body JSON
        data = request.get_json()
        ten_khoa = data.get('ten_khoa')

        if not ten_khoa:
            return jsonify({"error": "Tên khoa không được để trống"}), 400

        # Tìm kiếm khoa
        khoa = session_db.query(Khoa).filter(Khoa.ten_khoa == ten_khoa).first()
        if not khoa:
            return jsonify({"error": "Khoa not found"}), 404

        # Tìm các bác sĩ liên kết với khoa
        ct_khoa_records = session_db.query(CTKhoa).filter(CTKhoa.khoa_id == khoa.id).all()
        if not ct_khoa_records:
            return jsonify({"error": "No doctors found in the specified khoa"}), 404

        # Lấy danh sách bác sĩ
        doctor_list = []
        for record in ct_khoa_records:
            doctor = session_db.query(BacSi).filter(BacSi.id == record.bacsi_id).first()
            if doctor:
                doctor_list.append({
                    "id": doctor.id,
                    "hoc_ham": doctor.hoc_ham,
                    "ho": doctor.ho,
                    "ten": doctor.ten,
                    "hinh_anh": doctor.hinh_anh,
                    "mo_ta": doctor.mo_ta,
                    "ngay_bd_hanh_y": str(doctor.ngay_bd_hanh_y),
                    "username": doctor.username
                })

        return jsonify(doctor_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@doctor_blueprint.route('/searchDoctor', methods=['GET'])
def search_doctor():
    try:
        # Lấy từ khóa tìm kiếm từ JSON body request
        data = request.get_json()
        search_query = data.get('name')

        if not search_query:
            return jsonify({"msg": "Cần truyền từ khóa tìm kiếm"}), 400

        # Tìm bác sĩ theo tên chứa từ khóa (case-insensitive)
        doctors = session_db.query(BacSi).filter(
            BacSi.ten.ilike(f"%{search_query}%")
        ).all()

        if not doctors:
            return jsonify({"msg": "Không tìm thấy bác sĩ phù hợp!"}), 404

        # Trả về danh sách bác sĩ phù hợp
        result = [{
            "id": doctor.id,
            "hoc_ham": doctor.hoc_ham,
            "ho": doctor.ho,
            "ten": doctor.ten,
            "hinh_anh": doctor.hinh_anh,
            "mo_ta": doctor.mo_ta,
            "ngay_bd_hanh_y": str(doctor.ngay_bd_hanh_y),
            "username": doctor.username
        } for doctor in doctors]

        return jsonify(result), 200

    except SQLAlchemyError as e:
        return jsonify({"msg": "Lỗi cơ sở dữ liệu!", "error": str(e)}), 500

    except Exception as e:
        return jsonify({"msg": "Hệ thống lỗi!", "error": str(e)}), 500
