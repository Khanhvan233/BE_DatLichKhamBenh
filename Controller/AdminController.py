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
from datetime import datetime
import unicodedata

def remove_vietnamese_accents(text):
    """
    Loại bỏ dấu tiếng Việt khỏi chuỗi.
    """
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

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

        # Xử lý chuỗi họ + tên không dấu cho username
        if not ho or not ten:
            return jsonify({"msg": "Họ và Tên là bắt buộc"}), 400
        username = remove_vietnamese_accents(f"{ho} {ten}").replace(" ", "").lower()

        # Xử lý mật khẩu từ ngày bắt đầu hành nghề
        if not ngay_bd_hanh_y:
            return jsonify({"msg": "Ngày bắt đầu hành nghề là bắt buộc"}), 400
        try:
            formatted_date = datetime.strptime(ngay_bd_hanh_y, "%Y-%m-%d")
            password = formatted_date.strftime("%d%m%Y")
        except ValueError:
            return jsonify({"msg": "Định dạng ngày không hợp lệ"}), 400

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


# @auth_blueprint.route('/editDoctor/<int:doctor_id>', methods=['PUT'])
# @jwt_required()
# def edit_doctor(doctor_id):
#     try:
#         # Kiểm tra quyền admin từ token
#         identity = get_jwt_identity()
#         if not identity or "role" not in identity or identity["role"] not in ["admin", "doctor"]:
#             return jsonify({"msg": "Bạn không có quyền thực hiện thao tác này"}), 403

#         session_db = db_manager.get_session()
#         # Kiểm tra xem doctor có tồn tại không
#         doctor = session_db.query(BacSi).filter_by(id=doctor_id).one_or_none()
#         if not doctor:
#             return jsonify({"msg": "Doctor không tồn tại"}), 404

#         # Lấy dữ liệu từ request
#         data = request.json
#         doctor.hoc_ham = data.get('hoc_ham', doctor.hoc_ham)
#         doctor.ho = data.get('ho', doctor.ho)
#         doctor.ten = data.get('ten', doctor.ten)
        
#         doctor.mo_ta = data.get('mo_ta', doctor.mo_ta)
#         doctor.ngay_bd_hanh_y = data.get('ngay_bd_hanh_y', doctor.ngay_bd_hanh_y)
#         doctor.password = data.get('password', doctor.password)
#         doctor.username = data.get('username', doctor.username)
        
#         image_base64 = data.get('hinh_anh')
#         if image_base64:
#             try:
#                 prefix, base64_data = image_base64.split(',', 1)
#                 image_data = base64.b64decode(base64_data)
#                 # Thêm timestamp vào tên tệp
#                 timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#                 path = f"doctors/{doctor.username}_profile_{timestamp}.png"
#                 # Cập nhật hình ảnh lên Firebase Storage
#                 url = FirebaseHandler().updateImagePublic(path, image_data, "image/png")
#                 doctor.hinh_anh = url
#             except Exception as e:
#                 return jsonify({"msg": f"Lỗi xử lý ảnh: {str(e)}"}), 400
#         else:
#             # Không thay đổi hình ảnh nếu không có ảnh mới
#             doctor.hinh_anh = doctor.hinh_anh
#         # Lưu thay đổi vào database
#         session_db.commit()
#         return jsonify({"msg": "Chỉnh sửa doctor thành công"}), 200

#     except IntegrityError:
#         session_db.rollback()
#         return jsonify({"msg": "Tên đăng nhập đã tồn tại"}), 400
#     except Exception as e:
#         session_db.rollback()
#         return jsonify({"msg": str(e)}), 500
@auth_blueprint.route('/editDoctor/<int:doctor_id>', methods=['PUT'])
@jwt_required()
def edit_doctor(doctor_id):
    try:
        # Kiểm tra quyền admin từ token
        identity = get_jwt_identity()
        if not identity or "role" not in identity or identity["role"] not in ["admin", "doctor"]:
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
@auth_blueprint.route('/vanphong', methods=['POST'])
@jwt_required()
def add_vanphong():
    """
    Thêm mới một văn phòng.
    """
    try:
        identity = get_jwt_identity()
        if not identity or "role" not in identity or identity["role"] not in ["admin", "doctor"]:
            return jsonify({"msg": "Bạn không có quyền truy cập"}), 403

        data = request.get_json()
        bac_si_id = data.get('bac_si_id')
        dia_chi = data.get('dia_chi')
        thoi_luong_kham = data.get('thoi_luong_kham')
        phi_gap_dau = data.get('phi_gap_dau')
        phi_gap_sau = data.get('phi_gap_sau')

        if not (bac_si_id and dia_chi and thoi_luong_kham and phi_gap_dau and phi_gap_sau):
            return jsonify({"msg": "Thiếu thông tin cần thiết"}), 400

        session_db = db_manager.get_session()
        new_vanphong = VanPhong(
            bac_si_id=bac_si_id,
            dia_chi=dia_chi,
            thoi_luong_kham=thoi_luong_kham,
            phi_gap_dau=phi_gap_dau,
            phi_gap_sau=phi_gap_sau,
        )
        session_db.add(new_vanphong)
        session_db.commit()

        return jsonify({"msg": "Thêm văn phòng thành công"}), 201

    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@auth_blueprint.route('/vanphong/<int:id>', methods=['PUT'])
@jwt_required()
def edit_vanphong(id):
    """
    Sửa thông tin một văn phòng.
    """
    try:
        identity = get_jwt_identity()
        if not identity or "role" not in identity or identity["role"] not in ["admin", "doctor"]:
            return jsonify({"msg": "Bạn không có quyền truy cập"}), 403

        data = request.get_json()
        session_db = db_manager.get_session()

        vanphong = session_db.query(VanPhong).filter(VanPhong.id == id).first()
        if not vanphong:
            return jsonify({"msg": "Không tìm thấy văn phòng"}), 404

        dia_chi = data.get('dia_chi')
        thoi_luong_kham = data.get('thoi_luong_kham')
        phi_gap_dau = data.get('phi_gap_dau')
        phi_gap_sau = data.get('phi_gap_sau')

        if dia_chi is not None:
            vanphong.dia_chi = dia_chi
        if thoi_luong_kham is not None:
            vanphong.thoi_luong_kham = thoi_luong_kham
        if phi_gap_dau is not None:
            vanphong.phi_gap_dau = phi_gap_dau
        if phi_gap_sau is not None:
            vanphong.phi_gap_sau = phi_gap_sau

        session_db.commit()
        return jsonify({"msg": "Cập nhật văn phòng thành công"}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500
@auth_blueprint.route('/vanphong/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_vanphong(id):
    """
    Xóa một văn phòng.
    """
    try:
        identity = get_jwt_identity()
        if not identity or "role" not in identity or identity["role"] not in ["admin", "doctor"]:
            return jsonify({"msg": "Bạn không có quyền truy cập"}), 403

        session_db = db_manager.get_session()
        vanphong = session_db.query(VanPhong).filter(VanPhong.id == id).first()
        if not vanphong:
            return jsonify({"msg": "Không tìm thấy văn phòng"}), 404

        session_db.delete(vanphong)
        session_db.commit()
        return jsonify({"msg": "Xóa văn phòng thành công"}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@auth_blueprint.route('/lienketbenhvien', methods=['POST'])
@jwt_required()
def add_lienketbenhvien():
    """
    Thêm mới một liên kết bệnh viện.
    """
    try:
        identity = get_jwt_identity()
        # Kiểm tra quyền admin hoặc bác sĩ
        if not identity or "role" not in identity or identity["role"] not in ["admin", "doctor"]:
            return jsonify({"msg": "Bạn không có quyền truy cập"}), 403

        data = request.get_json()
        bac_si_id = data.get('bac_si_id')
        ten_benh_vien = data.get('ten_benh_vien')
        dia_chi = data.get('dia_chi')
        ngay_db = data.get('ngay_db')
        ngay_kt = data.get('ngay_kt')

        if not (bac_si_id and ten_benh_vien and dia_chi and ngay_db):
            return jsonify({"msg": "Thiếu thông tin cần thiết"}), 400

        session_db = db_manager.get_session()
        if ngay_kt=="":
            ngay_kt = None
        new_lienketbenhvien = LienKetBenhVien(
            bac_si_id=bac_si_id,
            ten_benh_vien=ten_benh_vien,
            dia_chi=dia_chi,
            ngay_db=ngay_db,
            ngay_kt=ngay_kt
        )
        session_db.add(new_lienketbenhvien)
        session_db.commit()

        return jsonify({
            "id": new_lienketbenhvien.id,
            "bac_si_id": new_lienketbenhvien.bac_si_id,
            "ten_benh_vien": new_lienketbenhvien.ten_benh_vien,
            "dia_chi": new_lienketbenhvien.dia_chi,
            "ngay_db": new_lienketbenhvien.ngay_db.isoformat(),
            "ngay_kt": new_lienketbenhvien.ngay_kt.isoformat() if new_lienketbenhvien.ngay_kt else None
        }), 201

    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@auth_blueprint.route('/lienketbenhvien/<int:id>', methods=['PUT'])
@jwt_required()
def update_lienketbenhvien(id):
    """
    Cập nhật thông tin một liên kết bệnh viện.
    """
    try:
        identity = get_jwt_identity()
        if not identity or "role" not in identity or identity["role"] not in ["admin", "doctor"]:
            return jsonify({"msg": "Bạn không có quyền truy cập"}), 403

        data = request.get_json()
        session_db = db_manager.get_session()

        lienketbenhvien = session_db.query(LienKetBenhVien).filter(LienKetBenhVien.id == id).first()
        if not lienketbenhvien:
            return jsonify({"msg": "Không tìm thấy liên kết bệnh viện"}), 404

        ten_benh_vien = data.get('ten_benh_vien')
        dia_chi = data.get('dia_chi')
        ngay_db = data.get('ngay_db')
        ngay_kt = data.get('ngay_kt')

        if ten_benh_vien:
            lienketbenhvien.ten_benh_vien = ten_benh_vien
        if dia_chi:
            lienketbenhvien.dia_chi = dia_chi
        if ngay_db:
            lienketbenhvien.ngay_db = ngay_db
        if ngay_kt:
            lienketbenhvien.ngay_kt = ngay_kt

        session_db.commit()
        return jsonify({"msg": "Cập nhật thành công"}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@auth_blueprint.route('/lienketbenhvien/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_lienketbenhvien(id):
    """
    Xóa một liên kết bệnh viện.
    """
    try:
        identity = get_jwt_identity()
        if not identity or "role" not in identity or identity["role"] not in ["admin", "doctor"]:
            return jsonify({"msg": "Bạn không có quyền truy cập"}), 403

        session_db = db_manager.get_session()
        lienketbenhvien = session_db.query(LienKetBenhVien).filter(LienKetBenhVien.id == id).first()
        if not lienketbenhvien:
            return jsonify({"msg": "Không tìm thấy liên kết bệnh viện"}), 404

        session_db.delete(lienketbenhvien)
        session_db.commit()
        return jsonify({"msg": "Xóa thành công"}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@auth_blueprint.route('/bangcapchungchi', methods=['POST'])
@jwt_required()
def add_bangcapchungchi():
    """
    Thêm mới một bằng cấp/chứng chỉ.
    """
    try:
        identity = get_jwt_identity()
        # Kiểm tra quyền admin hoặc bác sĩ
        if not identity or "role" not in identity or identity["role"] not in ["admin", "doctor"]:
            return jsonify({"msg": "Bạn không có quyền truy cập"}), 403

        data = request.get_json()
        bacsi_id = data.get('bacsi_id')
        ten_bangcap = data.get('ten_bangcap')
        co_quan_cap = data.get('co_quan_cap')
        ngay_cap = data.get('ngay_cap')

        if not (bacsi_id and ten_bangcap and ngay_cap):
            return jsonify({"msg": "Thiếu thông tin cần thiết"}), 400

        session_db = db_manager.get_session()
        new_bangcap = BangCapChungChi(
            bacsi_id=bacsi_id,
            ten_bangcap=ten_bangcap,
            co_quan_cap=co_quan_cap,
            ngay_cap=ngay_cap
        )
        session_db.add(new_bangcap)
        session_db.commit()

        return jsonify({
            "id": new_bangcap.id,
            "bacsi_id": new_bangcap.bacsi_id,
            "ten_bangcap": new_bangcap.ten_bangcap,
            "co_quan_cap": new_bangcap.co_quan_cap,
            "ngay_cap": new_bangcap.ngay_cap.isoformat()
        }), 201

    except Exception as e:
        return jsonify({"msg": str(e)}), 500
@auth_blueprint.route('/bangcapchungchi/<int:id>', methods=['PUT'])
@jwt_required()
def update_bangcapchungchi(id):
    """
    Cập nhật thông tin một bằng cấp/chứng chỉ.
    """
    try:
        identity = get_jwt_identity()
        if not identity or "role" not in identity or identity["role"] not in ["admin", "doctor"]:
            return jsonify({"msg": "Bạn không có quyền truy cập"}), 403

        data = request.get_json()
        session_db = db_manager.get_session()

        bangcap = session_db.query(BangCapChungChi).filter(BangCapChungChi.id == id).first()
        if not bangcap:
            return jsonify({"msg": "Không tìm thấy bằng cấp/chứng chỉ"}), 404

        if data.get('ten_bangcap'):
            bangcap.ten_bangcap = data['ten_bangcap']
        if data.get('co_quan_cap'):
            bangcap.co_quan_cap = data['co_quan_cap']
        if data.get('ngay_cap'):
            bangcap.ngay_cap = data['ngay_cap']

        session_db.commit()
        return jsonify({"msg": "Cập nhật thành công"}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500
@auth_blueprint.route('/bangcapchungchi/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_bangcapchungchi(id):
    """
    Xóa một bằng cấp/chứng chỉ.
    """
    try:
        identity = get_jwt_identity()
        if not identity or "role" not in identity or identity["role"] not in ["admin", "doctor"]:
            return jsonify({"msg": "Bạn không có quyền truy cập"}), 403

        session_db = db_manager.get_session()
        bangcap = session_db.query(BangCapChungChi).filter(BangCapChungChi.id == id).first()
        if not bangcap:
            return jsonify({"msg": "Không tìm thấy bằng cấp/chứng chỉ"}), 404

        session_db.delete(bangcap)
        session_db.commit()
        return jsonify({"msg": "Xóa thành công"}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@auth_blueprint.route('/lichtrinh', methods=['POST'])
@jwt_required()
def add_lichtrinh():
    """
    Thêm mới một lịch trình.
    """
    try:
        identity = get_jwt_identity()
        # Kiểm tra quyền admin hoặc bác sĩ
        if not identity or "role" not in identity or identity["role"] not in ["admin", "doctor"]:
            return jsonify({"msg": "Bạn không có quyền truy cập"}), 403

        data = request.get_json()
        van_phong_id = data.get('vanPhong_id')
        day_of_week = data.get('day_of_week')
        gio_bd = data.get('gio_bd')
        gio_kt = data.get('gio_kt')
        vang = data.get('vang')
        ly_do = data.get('ly_do')

        if not (van_phong_id and day_of_week and gio_bd and gio_kt and vang is not None):
            return jsonify({"msg": "Thiếu thông tin cần thiết"}), 400

        session_db = db_manager.get_session()
        new_lichtrinh = LichTrinh(
            vanPhong_id=van_phong_id,
            day_of_week=day_of_week,
            gio_bd=gio_bd,
            gio_kt=gio_kt,
            vang=vang,
            ly_do=ly_do
        )
        session_db.add(new_lichtrinh)
        session_db.commit()

        return jsonify({
            "id": new_lichtrinh.id,
            "vanPhong_id": new_lichtrinh.vanPhong_id,
            "day_of_week": new_lichtrinh.day_of_week,
            "gio_bd": new_lichtrinh.gio_bd.isoformat(),
            "gio_kt": new_lichtrinh.gio_kt.isoformat(),
            "vang": new_lichtrinh.vang,
            "ly_do": new_lichtrinh.ly_do
        }), 201

    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@auth_blueprint.route('/lichtrinh/<int:id>', methods=['PUT'])
@jwt_required()
def update_lichtrinh(id):
    """
    Cập nhật thông tin một lịch trình.
    """
    try:
        identity = get_jwt_identity()
        if not identity or "role" not in identity or identity["role"] not in ["admin", "doctor"]:
            return jsonify({"msg": "Bạn không có quyền truy cập"}), 403

        data = request.get_json()
        session_db = db_manager.get_session()

        lichtrinh = session_db.query(LichTrinh).filter(LichTrinh.id == id).first()
        if not lichtrinh:
            return jsonify({"msg": "Không tìm thấy lịch trình"}), 404

        if data.get('day_of_week'):
            lichtrinh.day_of_week = data['day_of_week']
        if data.get('gio_bd'):
            lichtrinh.gio_bd = data['gio_bd']
        if data.get('gio_kt'):
            lichtrinh.gio_kt = data['gio_kt']
        if data.get('vang') is not None:
            lichtrinh.vang = data['vang']
        if data.get('ly_do'):
            lichtrinh.ly_do = data['ly_do']

        session_db.commit()
        return jsonify({"msg": "Cập nhật thành công"}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@auth_blueprint.route('/lichtrinh/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_lichtrinh(id):
    """
    Xóa một lịch trình.
    """
    try:
        identity = get_jwt_identity()
        if not identity or "role" not in identity or identity["role"] not in ["admin", "doctor"]:
            return jsonify({"msg": "Bạn không có quyền truy cập"}), 403

        session_db = db_manager.get_session()
        lichtrinh = session_db.query(LichTrinh).filter(LichTrinh.id == id).first()
        if not lichtrinh:
            return jsonify({"msg": "Không tìm thấy lịch trình"}), 404

        session_db.delete(lichtrinh)
        session_db.commit()
        return jsonify({"msg": "Xóa thành công"}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500
