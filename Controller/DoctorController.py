
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort, redirect
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
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
        session_db = db_manager.get_session()
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
        
        session_db = db_manager.get_session()
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
        print(doctor_list)
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
        
        session_db = db_manager.get_session()
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
#nên thêm họ
def search_doctor():
    try:
        # Lấy từ khóa tìm kiếm từ JSON body request
        data = request.get_json()
        search_query = data.get('name')

        if not search_query:
            return jsonify({"msg": "Cần truyền từ khóa tìm kiếm"}), 400

        session_db = db_manager.get_session()
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


# @doctor_blueprint.route('/appointments', methods=['GET'])
# @jwt_required()
# def get_appointments():
#     """
#     API để lấy danh sách lịch hẹn của văn phòng mà bác sĩ hiện tại quản lý.
#     """
#     try:
#         # Lấy thông tin người dùng từ token
#         identity = get_jwt_identity()
#         if not identity or "role" not in identity or identity["role"] != "doctor":
#             return jsonify({"msg": "Bạn không có quyền truy cập"}), 403

#         bac_si_id = identity.get("userID")
#         if not bac_si_id:
#             return jsonify({"msg": "Không xác định được bác sĩ"}), 400

#         # Lấy ID văn phòng từ query hoặc tất cả văn phòng của bác sĩ
#         vanphong_id = request.args.get('vanphong_id')

#         session_db = db_manager.get_session()

#         if vanphong_id:
#             # Lấy lịch hẹn của một văn phòng cụ thể
#             appointments = session_db.query(DatHen).filter(DatHen.vanphong_id == vanphong_id).all()
#         else:
#             # Lấy tất cả lịch hẹn của các văn phòng do bác sĩ quản lý
#             appointments = session_db.query(DatHen).join(VanPhong).filter(VanPhong.bac_si_id == bac_si_id).all()

#         # Chuyển đổi dữ liệu lịch hẹn thành JSON
#         appointment_list = []
#         for appointment in appointments:
#             appointment_list.append({
#                 "id": appointment.id,
#                 "user_account_id": appointment.user_account_id,
#                 "vanphong_id": appointment.vanphong_id,
#                 "gio_hen": appointment.gio_hen.isoformat(),
#                 "gio_ket_thuc": appointment.gio_ket_thuc.isoformat() if appointment.gio_ket_thuc else None,
#                 "trang_thai": appointment.trang_thai,
#                 "ngay_gio_dat": appointment.ngay_gio_dat.isoformat(),
#                 "kieu_dat": appointment.kieu_dat
#             })

#         return jsonify({"appointments": appointment_list}), 200

#     except NoResultFound:
#         return jsonify({"msg": "Không tìm thấy lịch hẹn"}), 404
#     except Exception as e:
#         return jsonify({"msg": str(e)}), 500

@doctor_blueprint.route('/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    """
    API để lấy danh sách lịch hẹn của văn phòng mà bác sĩ hiện tại quản lý.
    """
    try:
        # Lấy thông tin người dùng từ token
        identity = get_jwt_identity()
        if not identity or "role" not in identity or identity["role"] != "doctor":
            return jsonify({"msg": "Bạn không có quyền truy cập"}), 403

        bac_si_id = identity.get("userID")
        if not bac_si_id:
            return jsonify({"msg": "Không xác định được bác sĩ"}), 400

        # Lấy ID văn phòng từ query hoặc tất cả văn phòng của bác sĩ
        vanphong_id = request.args.get('vanphong_id')

        session_db = db_manager.get_session()

        if vanphong_id:
            # Lấy lịch hẹn của một văn phòng cụ thể và thông tin địa chỉ
            appointments = (
                session_db.query(DatHen, VanPhong.dia_chi)
                .join(VanPhong, DatHen.vanphong_id == VanPhong.id)
                .filter(DatHen.vanphong_id == vanphong_id)
                .all()
            )
        else:
            # Lấy tất cả lịch hẹn của các văn phòng do bác sĩ quản lý và thông tin địa chỉ
            appointments = (
                session_db.query(DatHen, VanPhong.dia_chi)
                .join(VanPhong, DatHen.vanphong_id == VanPhong.id)
                .filter(VanPhong.bac_si_id == bac_si_id)
                .all()
            )

        # Chuyển đổi dữ liệu lịch hẹn thành JSON
        appointment_list = []
        for appointment, dia_chi in appointments:
            appointment_list.append({
                "id": appointment.id,
                "user_account_id": appointment.user_account_id,
                "vanphong_id": appointment.vanphong_id,
                "gio_hen": appointment.gio_hen.isoformat(),
                "gio_ket_thuc": appointment.gio_ket_thuc.isoformat() if appointment.gio_ket_thuc else None,
                "trang_thai": appointment.trang_thai,
                "ngay_gio_dat": appointment.ngay_gio_dat.isoformat(),
                "kieu_dat": appointment.kieu_dat,
                "dia_chi": dia_chi  # Thêm địa chỉ văn phòng
            })

        return jsonify({"appointments": appointment_list}), 200

    except NoResultFound:
        return jsonify({"msg": "Không tìm thấy lịch hẹn"}), 404
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

    
@doctor_blueprint.route('/appointments/<int:appointment_id>/update_status', methods=['PUT'])
@jwt_required()
def update_appointment_status(appointment_id):
    """
    Cập nhật trạng thái lịch hẹn.
    """
    try:
        identity = get_jwt_identity()
        if not identity or "role" not in identity or identity["role"] not in ["admin", "doctor"]:
            return jsonify({"msg": "Bạn không có quyền truy cập"}), 403

        data = request.get_json()
        new_status = data.get('trang_thai')

        if new_status not in ["0", "1", "2"]:
            return jsonify({"msg": "Trạng thái không hợp lệ"}), 400

        session_db = db_manager.get_session()
        appointment = session_db.query(DatHen).filter_by(id=appointment_id).one_or_none()

        if not appointment:
            return jsonify({"msg": "Lịch hẹn không tồn tại"}), 404

        # Cập nhật trạng thái
        appointment.trang_thai = new_status
        session_db.commit()

        return jsonify({"msg": "Cập nhật trạng thái thành công"}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500
