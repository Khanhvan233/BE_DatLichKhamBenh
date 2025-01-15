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
from sqlalchemy.orm import joinedload

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

        if identity["role"] != 'admin':  # Chỉ admin mới được phép thêm tài khoản
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
        session_db = db_manager.get_session()
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

        if identity["role"] != 'admin':  # Chỉ admin mới được phép thêm tài khoản
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
        session_db = db_manager.get_session()
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

        if identity["role"] != 'admin':  # Chỉ admin mới có quyền xem thông tin người dùng
            return jsonify({"msg": "Bạn không có quyền thực hiện thao tác này"}), 403
        
        session_db = db_manager.get_session()
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

        if identity["role"] != 'admin':  # Chỉ admin mới có quyền xem danh sách người dùng
            return jsonify({"msg": "Bạn không có quyền thực hiện thao tác này"}), 403
        
        session_db = db_manager.get_session()
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
        if not identity or "role" not in identity or identity["role"] != 'admin':
            return jsonify({"msg": "Bạn không có quyền thực hiện thao tác này"}), 403
        
        session_db = db_manager.get_session()
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
        if not identity or "role" not in identity or identity["role"] != 'admin':
            return jsonify({"msg": "Bạn không có quyền thực hiện thao tác này"}), 403

        session_db = db_manager.get_session()
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
        if not identity or "role" not in identity or identity["role"] != 'admin':
            return jsonify({"msg": "Bạn không có quyền thực hiện thao tác này"}), 403

        session_db = db_manager.get_session()
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
        if not identity or "role" not in identity or identity["role"] != 'admin':
            return jsonify({"msg": "Bạn không có quyền thực hiện thao tác này"}), 403

        session_db = db_manager.get_session()
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
    
# @auth_blueprint.route('/getAllAppointments', methods=['GET'])
# @jwt_required()
# def get_all_appointments():
#     try:
#         # Kiểm tra quyền admin từ token
#         identity = get_jwt_identity()

#         if not identity or "role" not in identity:
#             return jsonify({"msg": "Token không hợp lệ"}), 400

#         # Chỉ admin mới có quyền xem tất cả các lịch hẹn
#         if identity["role"] != 'admin':
#             return jsonify({"msg": "Bạn không có quyền truy cập danh sách lịch hẹn này"}), 403

#         session_db = db_manager.get_session()
#         # Lấy tất cả các lịch hẹn từ cơ sở dữ liệu và sắp xếp theo ngày giờ đặt gần nhất
#         appointments = session_db.query(DatHen).order_by(DatHen.ngay_gio_dat.desc()).all()

#         if not appointments:
#             return jsonify({"msg": "Không có lịch hẹn nào"}), 404

#         # Chuẩn bị dữ liệu trả về
#         appointments_list = []
#         for appointment in appointments:
#             appointments_list.append({
#                 "id": appointment.id,
#                 "user_account_id": appointment.user_account_id,
#                 "gio_hen": appointment.gio_hen.strftime("%Y-%m-%d %H:%M:%S") if appointment.gio_hen else None,
#                 "trang_thai": appointment.trang_thai,
#                 "ngay_gio_dat": appointment.ngay_gio_dat.strftime("%Y-%m-%d %H:%M:%S") if appointment.ngay_gio_dat else None,
#                 "kieu_dat": appointment.kieu_dat,
#                 "vanphong_id": appointment.vanphong_id
#             })

#         return jsonify({"appointments": appointments_list}), 200

@auth_blueprint.route('/getAllAppointments', methods=['GET'])
@jwt_required()
def get_all_appointments():
    try:
        identity = get_jwt_identity()
        if not identity or "role" not in identity:
            return jsonify({"msg": "Token không hợp lệ"}), 400

        if identity["role"] != 'admin':
            return jsonify({"msg": "Bạn không có quyền truy cập danh sách lịch hẹn này"}), 403

        session_db = db_manager.get_session()
        # Lấy tất cả lịch hẹn cùng với thông tin kiểu đặt
        appointments = (
            session_db.query(DatHen, KieuDat.ten_loai_dat)
            .join(KieuDat, DatHen.kieu_dat == KieuDat.id)
            .order_by(DatHen.ngay_gio_dat.desc())
            .all()
        )

        if not appointments:
            return jsonify({"msg": "Không có lịch hẹn nào"}), 404

        appointments_list = []
        for appointment, ten_loai_dat in appointments:
            appointments_list.append({
                "id": appointment.id,
                "user_account_id": appointment.user_account_id,
                "gio_hen": appointment.gio_hen.strftime("%Y-%m-%d %H:%M:%S") if appointment.gio_hen else None,
                "trang_thai": appointment.trang_thai,
                "ngay_gio_dat": appointment.ngay_gio_dat.strftime("%Y-%m-%d %H:%M:%S") if appointment.ngay_gio_dat else None,
                "kieu_dat": ten_loai_dat,  # Thêm tên kiểu đặt
                "vanphong_id": appointment.vanphong_id
            })

        return jsonify({"appointments": appointments_list}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500


    except Exception as e:
        return jsonify({"msg": str(e)}), 500

    
@auth_blueprint.route('/updateAppointmentStatus/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def update_appointment_status(appointment_id):
    try:
        # Lấy user ID từ token JWT
        user_identity = get_jwt_identity()

        # Kiểm tra xem user có phải là admin hay không
        if user_identity["role"] != 'admin':
            return jsonify({"msg": "Bạn không có quyền thay đổi trạng thái lịch hẹn"}), 403

        session_db = db_manager.get_session()
        # Lấy lịch hẹn từ cơ sở dữ liệu theo appointment_id
        appointment = session_db.query(DatHen).filter_by(id=appointment_id).first()

        if not appointment:
            return jsonify({"msg": "Lịch hẹn không tồn tại"}), 404

        # Kiểm tra trạng thái hiện tại
        if appointment.trang_thai == 0:
            # Chỉ chuyển từ 0 (đã đặt) thành 1 (thành công)
            appointment.trang_thai = 1
            session_db.commit()
            return jsonify({"msg": "Cập nhật trạng thái lịch hẹn thành công"}), 200
        else:
            return jsonify({"msg": "Trạng thái này không thể thay đổi"}), 400

    except Exception as e:
        return jsonify({"msg": str(e)}), 500
    
@auth_blueprint.route('/getBookingTypes', methods=['GET'])
@jwt_required()
def get_booking_types():
    try:
        # Kiểm tra quyền admin từ token
        identity = get_jwt_identity()

        if not identity or "role" not in identity:
            return jsonify({"msg": "Token không hợp lệ"}), 400

        # Chỉ admin mới có quyền truy cập
        if identity["role"] != 'admin':
            return jsonify({"msg": "Bạn không có quyền truy cập thông tin này"}), 403

        session_db = db_manager.get_session()
        # Lấy tất cả kiểu đặt từ cơ sở dữ liệu
        booking_types = session_db.query(KieuDat).all()

        if not booking_types:
            return jsonify({"msg": "Không có kiểu đặt nào"}), 404

        # Chuẩn bị dữ liệu trả về
        booking_types_list = []
        for booking_type in booking_types:
            booking_types_list.append({
                "id": booking_type.id,
                "ten_loai_dat": booking_type.ten_loai_dat
            })

        return jsonify({"booking_types": booking_types_list}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500
    
@auth_blueprint.route('/getOfficeDetails/<int:office_id>', methods=['GET'])
@jwt_required()
def get_office_details(office_id):
    try:
        # Kiểm tra quyền truy cập từ token
        identity = get_jwt_identity()
        if not identity or "role" not in identity:
            return jsonify({"msg": "Token không hợp lệ"}), 400

        session_db = db_manager.get_session()

        # Lấy thông tin văn phòng dựa trên office_id
        office = session_db.query(VanPhong).filter_by(id=office_id).first()

        if not office:
            return jsonify({"msg": "Không tìm thấy văn phòng"}), 404

        # Chuẩn bị dữ liệu trả về
        office_details = {
            "bac_si_id": office.bac_si_id,
            "lienketbenhvien_id": office.lienketbenhvien_id,
            "thoi_luong_kham": office.thoi_luong_kham,
            "phi_gap_dau": office.phi_gap_dau,
            "phi_gap_sau": office.phi_gap_sau,
            "dia_chi": office.dia_chi,
            "bac_si_ten": f"{office.bac_si.hoc_ham} {office.bac_si.ho} {office.bac_si.ten}" if office.bac_si else None,
            "benh_vien": office.lienketbenhvien.ten_benh_vien if office.lienketbenhvien else None
        }

        return jsonify({"office": office_details}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@auth_blueprint.route('/getAllDepartments', methods=['GET'])
@jwt_required()
def get_all_departments():
    try:
        # Kiểm tra quyền truy cập từ token
        identity = get_jwt_identity()
        if not identity or "role" not in identity:
            return jsonify({"msg": "Token không hợp lệ"}), 400

        session_db = db_manager.get_session()

        # Lấy danh sách các khoa
        departments = session_db.query(Khoa).all()

        if not departments:
            return jsonify({"msg": "Không có khoa nào được tìm thấy"}), 404

        # Chuẩn bị dữ liệu trả về
        department_list = []
        for department in departments:
            department_list.append({
                "id": department.id,
                "ten_khoa": department.ten_khoa
            })

        return jsonify({"departments": department_list}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@auth_blueprint.route('/addDepartment', methods=['POST'])
@jwt_required()
def add_department():
    try:
        identity = get_jwt_identity()
        if not identity or "role" not in identity:
            return jsonify({"msg": "Token không hợp lệ"}), 400

        data = request.get_json()
        ten_khoa = data.get("ten_khoa")

        if not ten_khoa:
            return jsonify({"msg": "Tên khoa không được để trống"}), 400

        session_db = db_manager.get_session()

        # Kiểm tra trùng tên khoa
        existing_department = session_db.query(Khoa).filter_by(ten_khoa=ten_khoa).first()
        if existing_department:
            return jsonify({"msg": "Tên khoa đã tồn tại"}), 400

        # Thêm khoa mới
        new_department = Khoa(ten_khoa=ten_khoa)
        session_db.add(new_department)
        session_db.commit()

        return jsonify({"msg": "Thêm khoa mới thành công", "id": new_department.id}), 201

    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@auth_blueprint.route('/editDepartment/<int:department_id>', methods=['PUT'])
@jwt_required()
def edit_department(department_id):
    try:
        identity = get_jwt_identity()
        if not identity or "role" not in identity:
            return jsonify({"msg": "Token không hợp lệ"}), 400

        data = request.get_json()
        ten_khoa = data.get("ten_khoa")

        if not ten_khoa:
            return jsonify({"msg": "Tên khoa không được để trống"}), 400

        session_db = db_manager.get_session()

        # Kiểm tra khoa có tồn tại hay không
        department = session_db.query(Khoa).filter_by(id=department_id).first()
        if not department:
            return jsonify({"msg": "Không tìm thấy khoa"}), 404

        # Kiểm tra trùng tên khoa
        existing_department = session_db.query(Khoa).filter(Khoa.ten_khoa == ten_khoa, Khoa.id != department_id).first()
        if existing_department:
            return jsonify({"msg": "Tên khoa đã tồn tại"}), 400

        # Cập nhật tên khoa
        department.ten_khoa = ten_khoa
        session_db.commit()

        return jsonify({"msg": "Cập nhật khoa thành công"}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@auth_blueprint.route('/deleteDepartment/<int:department_id>', methods=['DELETE'])
@jwt_required()
def delete_department(department_id):
    try:
        identity = get_jwt_identity()
        if not identity or "role" not in identity:
            return jsonify({"msg": "Token không hợp lệ"}), 400

        session_db = db_manager.get_session()

        # Kiểm tra khoa có tồn tại hay không
        department = session_db.query(Khoa).filter_by(id=department_id).first()
        if not department:
            return jsonify({"msg": "Không tìm thấy khoa"}), 404

        # Kiểm tra xem có bác sĩ nào liên kết với khoa không
        linked_doctors = session_db.query(CTKhoa).filter_by(khoa_id=department_id).count()
        if linked_doctors > 0:
            return jsonify({"msg": "Không thể xóa khoa vì có bác sĩ liên kết"}), 400

        # Xóa khoa
        session_db.delete(department)
        session_db.commit()

        return jsonify({"msg": "Xóa khoa thành công"}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@auth_blueprint.route('/ct_khoa', methods=['GET'])
@jwt_required()
def get_ct_khoa():
    try:
        # Kiểm tra quyền truy cập từ token
        identity = get_jwt_identity()
        if not identity or "role" not in identity:
            return jsonify({"msg": "Token không hợp lệ"}), 400

        # Chỉ cho phép admin truy cập
        if identity["role"] != "admin":
            return jsonify({"msg": "Bạn không có quyền truy cập"}), 403

        session_db = db_manager.get_session()

        # Lấy tất cả các bản ghi từ bảng CTKhoa và sắp xếp theo bacsi_id
        ct_khoa_records = session_db.query(CTKhoa).order_by(CTKhoa.bacsi_id).all()

        # Chuẩn bị dữ liệu trả về
        ct_khoa_list = []
        for record in ct_khoa_records:
            ct_khoa_list.append({
                "id": record.id,
                "bacsi_id": record.bacsi_id,
                "bacsi_ho": record.bacsi.ho if record.bacsi else None,
                "bacsi_ten": record.bacsi.ten if record.bacsi else None,
                "khoa_id": record.khoa_id,
                "khoa_ten": record.khoa.ten_khoa if record.khoa else None
            })

        return jsonify({"ct_khoa": ct_khoa_list}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500
    
@auth_blueprint.route('/ct_khoa/add', methods=['POST'])
@jwt_required()
def add_ct_khoa():
    """
    Thêm mới một bản ghi vào bảng CTKhoa.
    """
    try:
        identity = get_jwt_identity()
        if not identity or "role" not in identity or identity["role"] != "admin":
            return jsonify({"msg": "Bạn không có quyền truy cập"}), 403

        data = request.get_json()
        bacsi_id = data.get('bacsi_id')
        khoa_id = data.get('khoa_id')

        if not bacsi_id:
            return jsonify({"msg": "Thiếu thông tin bacsi_id"}), 400

        session_db = db_manager.get_session()

        new_ct_khoa = CTKhoa(bacsi_id=bacsi_id, khoa_id=khoa_id)
        session_db.add(new_ct_khoa)
        session_db.commit()

        return jsonify({"msg": "Thêm CT Khoa thành công"}), 201

    except Exception as e:
        return jsonify({"msg": str(e)}), 500
@auth_blueprint.route('/ct_khoa/edit/<int:id>', methods=['PUT'])
@jwt_required()
def update_ct_khoa(id):
    """
    Sửa một bản ghi trong bảng CTKhoa.
    """
    try:
        identity = get_jwt_identity()
        if not identity or "role" not in identity or identity["role"] != "admin":
            return jsonify({"msg": "Bạn không có quyền truy cập"}), 403

        data = request.get_json()
        khoa_id = data.get('khoa_id')

        session_db = db_manager.get_session()
        ct_khoa = session_db.query(CTKhoa).filter(CTKhoa.id == id).first()

        if not ct_khoa:
            return jsonify({"msg": "Không tìm thấy bản ghi"}), 404

        # Cập nhật thông tin
        if khoa_id is not None:
            ct_khoa.khoa_id = khoa_id

        session_db.commit()
        return jsonify({"msg": "Cập nhật CT Khoa thành công"}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500
@auth_blueprint.route('/ct_khoa/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_ct_khoa(id):
    """
    Xóa một bản ghi trong bảng CTKhoa.
    """
    try:
        identity = get_jwt_identity()
        if not identity or "role" not in identity or identity["role"] != "admin":
            return jsonify({"msg": "Bạn không có quyền truy cập"}), 403

        session_db = db_manager.get_session()
        ct_khoa = session_db.query(CTKhoa).filter(CTKhoa.id == id).first()

        if not ct_khoa:
            return jsonify({"msg": "Không tìm thấy bản ghi"}), 404

        session_db.delete(ct_khoa)
        session_db.commit()
        return jsonify({"msg": "Xóa CT Khoa thành công"}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500
    
    
@auth_blueprint.route('/bacsi', methods=['GET'])
@jwt_required()
def get_all_bacsi():
    """
    Lấy danh sách tất cả các bác sĩ.
    """
    try:
        identity = get_jwt_identity()
        if not identity or "role" not in identity:
            return jsonify({"msg": "Token không hợp lệ"}), 400

        session_db = db_manager.get_session()
        bacsi_records = session_db.query(BacSi).all()

        bacsi_list = [
            {
                "id": bacsi.id,
                "ho": bacsi.ho,
                "ten": bacsi.ten,
            }
            for bacsi in bacsi_records
        ]

        return jsonify({"bacsi_list": bacsi_list}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@auth_blueprint.route('/bacsi/<int:id>', methods=['GET'])
@jwt_required()
def get_doctor_by_id(id):
    """
    Lấy thông tin chi tiết của một bác sĩ theo ID.
    """
    try:
        identity = get_jwt_identity()
        if not identity or "role" not in identity:
            return jsonify({"msg": "Token không hợp lệ"}), 400

        session_db = db_manager.get_session()

        # Lấy bác sĩ và các thông tin liên quan
        doctor = session_db.query(BacSi).options(
            joinedload(BacSi.lienketbenhvien),
            joinedload(BacSi.bangcap_chungchi),
            joinedload(BacSi.vanphongs).joinedload(VanPhong.lichtrinhs)
        ).filter(BacSi.id == id).first()

        if not doctor:
            return jsonify({"msg": "Không tìm thấy bác sĩ với ID được cung cấp."}), 404

        # Chuẩn bị dữ liệu phản hồi
        response_data = {
            "id": doctor.id,
            "hoc_ham": doctor.hoc_ham,
            "ho": doctor.ho,
            "ten": doctor.ten,
            "hinh_anh": doctor.hinh_anh,
            "mo_ta": doctor.mo_ta,
            "ngay_bd_hanh_y": doctor.ngay_bd_hanh_y.isoformat() if doctor.ngay_bd_hanh_y else None,
            "username": doctor.username,
            "lienketbenhvien": [
                {
                    "id": bv.id,
                    "ten_benh_vien": bv.ten_benh_vien,
                    "dia_chi": bv.dia_chi,
                    "ngay_db": bv.ngay_db.isoformat(),
                    "ngay_kt": bv.ngay_kt.isoformat() if bv.ngay_kt else None
                } for bv in doctor.lienketbenhvien
            ],
            "bangcap_chungchi": [
                {
                    "id": bc.id,
                    "ten_bangcap": bc.ten_bangcap,
                    "co_quan_cap": bc.co_quan_cap,
                    "ngay_cap": bc.ngay_cap.isoformat()
                } for bc in doctor.bangcap_chungchi
            ],
            "vanphongs": [
                {
                    "id": vp.id,
                    "dia_chi": vp.dia_chi,
                    "thoi_luong_kham": vp.thoi_luong_kham,
                    "phi_gap_dau": vp.phi_gap_dau,
                    "phi_gap_sau": vp.phi_gap_sau,
                    "lichtrinhs": [
                        {
                            "id": lt.id,
                            "day_of_week": lt.day_of_week,
                            "gio_bd": lt.gio_bd.isoformat(),
                            "gio_kt": lt.gio_kt.isoformat(),
                            "vang": lt.vang,
                            "ly_do": lt.ly_do
                        } for lt in vp.lichtrinhs
                    ]
                } for vp in doctor.vanphongs
            ]
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500